# -*- coding: utf-8 -*-
"""Office models."""

from .database import Column, Model, SurrogatePK, db, reference_col, relationship, UUID, ForeignKey


class DataDict(SurrogatePK, Model):
    """A Data dict of the app."""

    __tablename__ = "data_dict"
    dict_key = Column(db.String(64), index=True)
    dict_value = Column(db.String(64))
    dict_label = Column(db.String(64))
    dict_description = Column(db.String(256))
    dict_type = Column(db.String(64), index=True)

    @classmethod
    def get_value_by_key(cls, key):
        """
        Get value by key
        @param key:
        @return:
        """
        pass

