# -*- coding: utf-8 -*-
"""Office models."""

from .database import Column, Model, SurrogatePK, db, reference_col, relationship, UUID, ForeignKey


class Office(SurrogatePK, Model):
    """A Office of the app."""

    __tablename__ = "offices"
    parent_id = Column(UUID, ForeignKey("offices.id"))
    children = relationship("Office", lazy="joined", join_depth=1)
    name = Column(db.String(80), unique=True, nullable=True)
    address = Column(db.String(80), unique=True, nullable=True)
    code = Column(db.String(64), unique=True, nullable=True)
