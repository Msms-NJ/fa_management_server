# -*- coding: utf-8 -*-
"""Role models."""
import datetime as dt

from flask_login import UserMixin

from .database import (
    Column,
    ForeignKey,
    Model,
    SurrogatePK,
    db,
    reference_col,
    relationship,
    UUID,
)
from .role import Role
from .user import User


class UserRole(SurrogatePK, Model):
    """用户角色关联表"""

    __tablename__ = "user_role"
    user_id = Column(UUID, db.ForeignKey("users.id"), nullable=False)
    role_id = Column(UUID, db.ForeignKey("roles.id"), nullable=False)
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")

    def __init__(self, user, role, **kwargs):
        """Create instance."""
        db.Model.__init__(self, user=user, role=role, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<UserRole({id})>".format(id=self.id)
