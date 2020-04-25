# -*- coding: utf-8 -*-
from .database import db
from .office import Office
from .role import Role
from .user import User
from .user_role import UserRole
from .data_dict import DataDict


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {
            "db": db,
            "User": User,
            "Role": Role,
            "Office": Office,
            "UserRole": UserRole,
            "DataDict": DataDict,
        }

    app.shell_context_processor(shell_context)
