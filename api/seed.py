import asyncio
import logging
from passlib.context import CryptContext

from app.database import engine, AsyncSessionLocal, Base
from app.models import User, Role # Assuming models are accessible like this
# from app.users.models import User, Role # More specific import if preferred

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def seed_data():
    async with engine.begin() as conn:
        # In a real scenario, you might want to drop tables only in dev
        # For now, we assume a clean DB or that this is run once.
        # await conn.run_sync(Base.metadata.drop_all) # Careful with this in prod!
        await conn.run_sync(Base.metadata.create_all) # Creates tables if they don't exist

    async with AsyncSessionLocal() as db:
        try:
            logger.info("Starting data seeding...")

            # --- Seed Roles ---
            roles_to_create = [
                {"name": "Admin", "description": "Administrator with full access"},
                {"name": "Supplier", "description": "Supplier user with access to product and order management"},
                {"name": "Support", "description": "Support staff with access to customer service tools"},
                {"name": "User", "description": "Regular user/customer"}, # Added a general user role
            ]

            created_roles = {}
            for role_data in roles_to_create:
                existing_role = await db.execute(
                    Role.__table__.select().where(Role.name == role_data["name"])
                )
                role = existing_role.scalar_one_or_none()
                if not role:
                    role = Role(**role_data)
                    db.add(role)
                    await db.flush() # Flush to get ID for relationship
                    logger.info(f"Created role: {role.name}")
                else:
                    logger.info(f"Role already exists: {role.name}")
                created_roles[role.name] = role

            await db.commit() # Commit roles before assigning to users

            # --- Seed Admin User ---
            admin_username = "admin"
            admin_email = "admin@example.com"
            admin_password = "adminpassword" # Change this in a real environment

            existing_admin = await db.execute(
                User.__table__.select().where(User.username == admin_username)
            )
            admin_user = existing_admin.scalar_one_or_none()

            if not admin_user:
                hashed_admin_password = await get_password_hash(admin_password)
                admin_user = User(
                    username=admin_username,
                    email=admin_email,
                    hashed_password=hashed_admin_password,
                    is_active=True
                )

                # Assign Admin role
                admin_role = created_roles.get("Admin")
                if admin_role:
                    admin_user.roles.append(admin_role)
                else:
                    logger.warning("Admin role not found for assigning to admin user.")

                db.add(admin_user)
                await db.commit()
                logger.info(f"Created admin user: {admin_user.username} with Admin role.")
            else:
                logger.info(f"Admin user already exists: {admin_user.username}")
                # Optionally, ensure admin user has Admin role if they exist
                admin_role_obj = created_roles.get("Admin")
                if admin_role_obj and admin_role_obj not in admin_user.roles:
                    admin_user.roles.append(admin_role_obj)
                    await db.commit()
                    logger.info(f"Assigned Admin role to existing admin user: {admin_user.username}")


            # --- Seed Example Supplier User ---
            supplier_username = "supplier1"
            supplier_email = "supplier1@example.com"
            supplier_password = "supplierpassword"

            existing_supplier = await db.execute(
                 User.__table__.select().where(User.username == supplier_username)
            )
            supplier_user = existing_supplier.scalar_one_or_none()

            if not supplier_user:
                hashed_supplier_password = await get_password_hash(supplier_password)
                supplier_user = User(
                    username=supplier_username,
                    email=supplier_email,
                    hashed_password=hashed_supplier_password,
                    is_active=True
                )
                supplier_role = created_roles.get("Supplier")
                if supplier_role:
                    supplier_user.roles.append(supplier_role)
                db.add(supplier_user)
                await db.commit()
                logger.info(f"Created supplier user: {supplier_user.username} with Supplier role.")
            else:
                logger.info(f"Supplier user already exists: {supplier_user.username}")


            logger.info("Data seeding completed successfully.")

        except Exception as e:
            await db.rollback()
            logger.error(f"Error during data seeding: {e}")
            raise
        finally:
            await db.close()

async def main():
    # This is to ensure DATABASE_URL is loaded from .env if script is run directly
    # For docker-compose, it's set in the environment.
    from dotenv import load_dotenv
    import os
    # Load .env file from the directory of this script (api/.env)
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path=dotenv_path)

    # Re-initialize settings if needed, as DATABASE_URL might have just been loaded
    # This is a bit of a hack for standalone script.
    # In a FastAPI app context, Pydantic settings handle this more gracefully.
    from app.core.config import settings as app_settings
    global settings # make settings available to the module if it's imported
    settings = app_settings

    # Re-initialize engine with potentially updated settings.DATABASE_URL
    # This is also a hack. Ideally, engine configuration is done once.
    from app.database import engine as app_engine
    global engine
    engine = app_engine

    logger.info(f"Using database URL: {settings.DATABASE_URL}")
    if not settings.DATABASE_URL or "None" in str(settings.DATABASE_URL):
         logger.error("DATABASE_URL is not configured correctly. Seeding cannot proceed.")
         return

    await seed_data()

if __name__ == "__main__":
    # Ensure .env is loaded for direct script execution
    from dotenv import load_dotenv
    import os
    # Load .env file from the directory of this script (api/.env)
    # This path assumes seed.py is in the 'api' directory.
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
    else:
        logger.warning(f".env file not found at {dotenv_path}. Assuming environment variables are set.")

    # Need to re-import settings and engine after dotenv load for standalone script
    from app.core.config import settings as app_settings
    from app.database import engine as app_engine, AsyncSessionLocal as app_session_local, Base as app_base

    # Make them available globally within this script's context for seed_data
    settings = app_settings
    engine = app_engine
    AsyncSessionLocal = app_session_local
    Base = app_base

    # Update User and Role to use the re-imported Base
    User.metadata = Base.metadata
    Role.metadata = Base.metadata

    if not settings.DATABASE_URL or "None" in str(settings.DATABASE_URL) or not settings.POSTGRES_DB:
         logger.error("DATABASE_URL or its components are not configured correctly in .env or environment. Seeding cannot proceed.")
         logger.error(f"Current DB URL from settings: {settings.DATABASE_URL}")

    else:
        logger.info(f"Starting seed script. Database URL: {settings.DATABASE_URL}")
        asyncio.run(main())

# To run this script:
# Ensure your .env file is configured in the `api` directory.
# From the `api` directory: `python seed.py`
# Or via docker-compose:
# `docker-compose run --rm backend python seed.py`
# (Ensure DATABASE_URL is correctly passed from docker-compose.yml to the backend service environment)
