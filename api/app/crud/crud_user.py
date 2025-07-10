from typing import Any, Dict, Optional, Union, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


from app.core.security import get_password_hash, verify_password
from app.models import User, Role # Use direct model import
from app.auth.schemas import UserCreate # Use auth.schemas for UserCreate for now


class CRUDUser:
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        result = await db.execute(select(User).options(selectinload(User.roles)).where(User.email == email))
        return result.scalars().first()

    async def get_by_username(self, db: AsyncSession, *, username: str) -> Optional[User]:
        result = await db.execute(select(User).options(selectinload(User.roles)).where(User.username == username))
        return result.scalars().first()

    async def get(self, db: AsyncSession, id: Any) -> Optional[User]:
        result = await db.execute(select(User).options(selectinload(User.roles)).where(User.id == id))
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=hashed_password,
            is_active=True # Default to active, or make it part of UserCreate
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: AsyncSession, *, username_or_email: str, password: str
    ) -> Optional[User]:
        # Try finding user by username first, then by email
        user = await self.get_by_username(db, username=username_or_email)
        if not user:
            user = await self.get_by_email(db, email=username_or_email)

        if not user:
            return None
        if not user.is_active: # Optional: check if user is active
            return None # Or raise an exception for inactive user
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def assign_role_to_user(self, db: AsyncSession, *, user: User, role: Role) -> User:
        if role not in user.roles:
            user.roles.append(role)
            db.add(user)
            await db.commit()
            await db.refresh(user)
        return user

    async def get_user_roles(self, user: User) -> List[str]:
        return [role.name for role in user.roles]

user = CRUDUser()

class CRUDRole:
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Role]:
        result = await db.execute(select(Role).where(Role.name == name))
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, name: str, description: Optional[str] = None) -> Role:
        db_obj = Role(name=name, description=description)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

role = CRUDRole()
