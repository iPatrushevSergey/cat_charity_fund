from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """
    A diagram with the basic fields of the user model, except
    for the password. Fields: id, email, is_active, is_superuser,
    is_verified. Int is the data type for annotating the user id.
    """
    pass


class UserCreate(schemas.BaseUserCreate):
    """
    Scheme for creating a user. Required fields: email, password.
    Any other fields will be ignored.
    """
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """
    The schema for updaiting the user object. Contains all the basic fields
    of the user model. All fields are optional. Is_active, is_superuser,
    is_verified can only be changed by the superuser.
    """
    pass
