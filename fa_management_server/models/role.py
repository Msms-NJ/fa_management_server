# -*- coding: utf-8 -*-
"""Role models."""
from dataclasses import dataclass
from array import array
from .database import Column, Model, SurrogatePK, db, reference_col, relationship
from sqlalchemy.dialects.postgresql import ARRAY


@dataclass
class Role(SurrogatePK, Model):
    """用户角色信息表"""
    __tablename__ = "roles"

    # 配置JSON返回字段信息
    name: str
    id: str
    remarks: str
    web_menus: array
    update_date: str

    # role 角色数据权限 data_scope
    # 0 默认值 1 只能看到自己数据 2 能看到当前所在机构下的数据 3 能看到系统中的所有数据
    DATA_SCOPE_DEFAULT = 0
    DATA_SCOPE_SELF = 1
    DATA_SCOPE_OFFICE = 2
    DATA_SCOPE_ALL = 3

    # 配置数据库字段信息
    name = Column(db.String(80), unique=True, nullable=False)
    users = relationship("UserRole", back_populates="role")
    data_scope = Column(db.SmallInteger, nullable=False)
    web_menus = Column(ARRAY(db.String))

    def __init__(self, **kwargs):
        """Create instance."""
        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Role({name})>".format(name=self.name)
