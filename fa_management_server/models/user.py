# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from dataclasses import dataclass
from flask_login import UserMixin

from ..extensions import bcrypt
from .database import Column, Model, SurrogatePK, db, reference_col, relationship


@dataclass
class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = "users"

    # 配置JSON返回数据字段
    username: str
    email: str
    mobile: str
    wechat_nickname: str
    wechat_gender: str
    wechat_province: str
    avatar_url: str

    # 配置数据库字段信息
    username = Column(db.String(80), unique=True, nullable=True)
    email = Column(db.String(80), unique=True, nullable=True)
    mobile = Column(db.String(32), unique=True, nullable=True)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    # 头像地址
    avatar_url = Column(db.String(256), nullable=True)
    # 是否有效
    active = Column(db.Boolean(), default=False)
    # 用户类型
    user_type = Column(db.Integer, default=0)
    is_admin = Column(db.Boolean(), default=False)
    address = Column(db.String(256), nullable=True)
    # 绑定的微信信息
    wechat_openid = Column(db.String(64), nullable=True, index=True)
    wechat_nickname = Column(db.String(256), nullable=True)
    wechat_gender = Column(db.Integer, default=0)
    wechat_province = Column(db.String(256), nullable=True)
    wechat_city = Column(db.String(256), nullable=True)
    wechat_country = Column(db.String(256), nullable=True)
    wechat_avatar = Column(db.String(256), nullable=True)
    wechat_privilege = Column(db.String(256), nullable=True)
    wechat_union_id = Column(db.String(256), nullable=True)
    wechat_language = Column(db.String(32), nullable=True)

    roles = relationship("UserRole", back_populates="user")

    def __init__(self, username, email=None, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """设置密码"""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """检查密码"""
        return bcrypt.check_password_hash(self.password, value)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "address": self.address,
        }

    @property
    def full_name(self):
        """Full user name."""
        return "{0} {1}".format(self.first_name, self.last_name)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<User({username!r})>".format(username=self.username)

    def __str__(self):
        return {
            "id": self.id,
        }
