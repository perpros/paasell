from .crud_user import user, role

# This pattern allows to import like:
# from app.crud import user
# user.get_by_email(...)

# Or if you prefer to make them directly available:
# from .crud_user import CRUDUser
# from .crud_role import CRUDRole # Assuming you might split them
# user_crud = CRUDUser()
# role_crud = CRUDRole()
