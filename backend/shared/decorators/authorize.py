from functools import wraps

from fastapi import HTTPException
from shared.enums.user.user_role import UserRole


def authorize(roles: list[UserRole], user_attr: str = 'user'):
    """
    A decorator to restrict access to specific roles for class-based view methods. (decorated with @cbv)

    Args:
        roles (List[UserRole]): A list of allowed roles that can access the decorated method.
        user_attr (str): The name of the class atribute that represents the User principal, DEFAULT = 'user'

    Raises:
        HTTPException: Raised with status code 403 if the class does not has a user atribute or current user's role is not in the allowed roles.

    Example:
        @authorize(roles=[UserRole.ADMIN, UserRole.USER])
        def some_protected_method(self):
            # Logic for authorized users only
            pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            formmated_roles = [role.value for role in roles]
            if not hasattr(self, user_attr) or self.user.role not in formmated_roles:
                raise HTTPException(
                    status_code=403,
                    detail=f'Access denied, requires one of the following roles: {formmated_roles}, user has {self.user.role}'
                    )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator