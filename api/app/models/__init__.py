# Import all models here to make them accessible via app.models
from app.users.models import User, Role, user_roles_table
from app.database import Base # Base is needed for Alembic to find the models

# You can also define __all__ if you want to control what `from app.models import *` imports
# __all__ = ["User", "Role", "user_roles_table", "Base"]
