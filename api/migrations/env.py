import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine # Import AsyncEngine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add the 'app' directory to the Python path
# This ensures that Alembic can find your models and other app modules
# Adjust the path as necessary if your Alembic scripts are not in project_root/migrations
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# Import your Base model and any specific models if needed for target_metadata
# This is crucial for autogenerate to detect changes.
from app.database import Base  # Your declarative base
from app.models import * # Import all your models to ensure they are registered with Base.metadata

# For async, Alembic needs to run migrations in a synchronous way.
# We use the database URL directly from settings or environment.
from app.core.config import settings # Your application settings

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    # Prefer DATABASE_URL from environment if available (e.g., from docker-compose)
    # Fallback to settings if not set (though settings should load from env)
    db_url = os.getenv("DATABASE_URL", settings.DATABASE_URL)
    if not db_url:
        raise ValueError("DATABASE_URL is not set in environment or settings.")
    # Alembic needs a sync URL. If your DATABASE_URL is async, convert it.
    # Example: "postgresql+asyncpg://" becomes "postgresql://"
    return db_url.replace("+asyncpg", "")


target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url() # Use the modified get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # compare_type=True, # Add this if you want type comparison during autogenerate
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # compare_type=True, # Add this if you want type comparison during autogenerate
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Get the synchronous URL
    sync_url = get_url()

    # Create a synchronous engine for Alembic
    connectable = engine_from_config(
        {"sqlalchemy.url": sync_url}, # Pass config directly
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        # future=True # For SQLAlchemy 2.0 style if needed
    )

    # For async, connectable should be an AsyncEngine
    # However, Alembic's context.configure expects a sync connection.
    # So we use a sync engine for migration tasks.
    # If your application uses an async engine, ensure the URL is compatible.

    if isinstance(connectable, AsyncEngine):
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)
        await connectable.dispose()
    else: # Sync engine
        with connectable.connect() as connection:
            do_run_migrations(connection)


if context.is_offline_mode():
    run_migrations_offline()
else:
    # Due to Alembic running migrations synchronously,
    # we can't directly use asyncio.run() if this script is imported
    # by another asyncio process.
    # For simplicity, we'll assume direct execution or careful handling.
    # If issues arise, consider using `nest_asyncio` or restructuring.
    import asyncio
    asyncio.run(run_migrations_online())
