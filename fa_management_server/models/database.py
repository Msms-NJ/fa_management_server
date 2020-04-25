# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from datetime import datetime
import json
from flask_login import current_user
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm.attributes import QueryableAttribute
from sqlalchemy import text
from dataclasses import dataclass

from ..compat import basestring
from ..extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship
ForeignKey = db.ForeignKey


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def all(cls):
        return cls.query.all()

    def __init__(self, json_data):
        """Create instance."""
        db.Model.__init__(self, json_data)

    def __eq__(self, other):
        return self.id == other.id

    @classmethod
    def create_from_json(cls, json_data):
        instance = cls()
        for k, v in json_data.items():
            setattr(instance, k, v)
        if current_user is not None and current_user and current_user.is_active:
            instance.create_by = current_user.id
            instance.update_by = current_user.id
        return instance.save()

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        if current_user is not None and current_user and current_user.is_active:
            setattr(instance, "create_by", current_user.id)
            setattr(instance, "update_by", current_user.id)
        # instance.id = str(uuid()).replace("-", "")
        return instance.save()

    def update(self, dict_dta: dict, commit=True):
        if self is None:
            return
        for k, v in dict_dta.items():
            if v is not None:
                setattr(self, k, v)
        if current_user is not None and current_user:
            setattr(self, "update_by", current_user.id)
        return commit and self.save() or self

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if current_user is not None and current_user:
            setattr(self, "update_by", current_user.id)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base models class that includes CRUD convenience methods."""

    __abstract__ = True

    # 废弃使用 dataclass 来代替
    # def to_dict(self, show=None, _hide=[], _path=None):
    #     """
    #     Return a dictionary representation of this model.
    #     https://wakatime.com/blog/32-flask-part-1-sqlalchemy-models-to-json
    #     """
    #
    #     show = show or []
    #
    #     hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
    #     default = self._default_fields if hasattr(self, "_default_fields") else []
    #     default.extend(['id', 'modified_at', 'created_at'])
    #
    #     if not _path:
    #         _path = self.__tablename__.lower()
    #
    #         def prepend_path(item):
    #             item = item.lower()
    #             if item.split(".", 1)[0] == _path:
    #                 return item
    #             if len(item) == 0:
    #                 return item
    #             if item[0] != ".":
    #                 item = ".%s" % item
    #             item = "%s%s" % (_path, item)
    #             return item
    #
    #         _hide[:] = [prepend_path(x) for x in _hide]
    #         show[:] = [prepend_path(x) for x in show]
    #
    #     columns = self.__table__.columns.keys()
    #     relationships = self.__mapper__.relationships.keys()
    #     properties = dir(self)
    #
    #     ret_data = {}
    #
    #     for key in columns:
    #         if key.startswith("_"):
    #             continue
    #         check = "%s.%s" % (_path, key)
    #         if check in _hide or key in hidden:
    #             continue
    #         if check in show or key in default:
    #             ret_data[key] = getattr(self, key)
    #
    #     for key in relationships:
    #         if key.startswith("_"):
    #             continue
    #         check = "%s.%s" % (_path, key)
    #         if check in _hide or key in hidden:
    #             continue
    #         if check in show or key in default:
    #             _hide.append(check)
    #             is_list = self.__mapper__.relationships[key].uselist
    #             if is_list:
    #                 items = getattr(self, key)
    #                 if self.__mapper__.relationships[key].query_class is not None:
    #                     if hasattr(items, "all"):
    #                         items = items.all()
    #                 ret_data[key] = []
    #                 for item in items:
    #                     ret_data[key].append(
    #                         item.to_dict(
    #                             show=list(show),
    #                             _hide=list(_hide),
    #                             _path=("%s.%s" % (_path, key.lower())),
    #                         )
    #                     )
    #             else:
    #                 if (
    #                         self.__mapper__.relationships[key].query_class is not None
    #                         or self.__mapper__.relationships[key].instrument_class
    #                         is not None
    #                 ):
    #                     item = getattr(self, key)
    #                     if item is not None:
    #                         ret_data[key] = item.to_dict(
    #                             show=list(show),
    #                             _hide=list(_hide),
    #                             _path=("%s.%s" % (_path, key.lower())),
    #                         )
    #                     else:
    #                         ret_data[key] = None
    #                 else:
    #                     ret_data[key] = getattr(self, key)
    #
    #     for key in list(set(properties) - set(columns) - set(relationships)):
    #         if key.startswith("_"):
    #             continue
    #         if not hasattr(self.__class__, key):
    #             continue
    #         attr = getattr(self.__class__, key)
    #         if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
    #             continue
    #         check = "%s.%s" % (_path, key)
    #         if check in _hide or key in hidden:
    #             continue
    #         if check in show or key in default:
    #             val = getattr(self, key)
    #             if hasattr(val, "to_dict"):
    #                 ret_data[key] = val.to_dict(
    #                     show=list(show),
    #                     _hide=list(_hide),
    #                     _path=("%s.%s" % (_path, key.lower()))
    #                 )
    #             else:
    #                 try:
    #                     ret_data[key] = json.loads(json.dumps(val))
    #                 except:
    #                     pass
    #
    #     return ret_data


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
@dataclass
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {"extend_existing": True}

    # 默认相关JSON字段
    create_date: str
    id: str
    update_date: str
    sort_number: int

    # 主键ID，使用 postgresql 的函数来自动生成UUID
    id = Column(UUID, primary_key=True, server_default=text("gen_random_uuid()"))
    # 备注信息
    remarks = Column(db.String(128))
    # 创建时间
    create_date = Column(db.DateTime, nullable=False, default=datetime.now)
    # 更新时间
    update_date = Column(db.DateTime, nullable=False, onupdate=datetime.now, default=datetime.now)
    # 创建人员
    create_by = Column(db.String(64), nullable=True)
    # 更新人员
    update_by = Column(db.String(64), nullable=True)
    # 查询顺序
    sort_number = Column(db.Integer, autoincrement=True, index=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if isinstance(record_id, str) or isinstance(record_id, bytes):
            return cls.query.get(record_id)
        return None
        # if any(
        #     (
        #         isinstance(record_id, basestring) and record_id.isdigit(),
        #         isinstance(record_id, (int, float)),
        #     )
        # ):
        #     print("this is get by id")
        #     print(record_id)
        #     return cls.query.get(record_id)
        # print("wrong")
        # return None


def reference_col(
    tablename, nullable=False, pk_name="id", foreign_key_kwargs=None, column_kwargs=None
):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name), **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs
    )
