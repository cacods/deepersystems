from pyramid.security import Allow, Everyone

from sqlalchemy import (
    Column,
    Integer,
    Float,
    Text,
    ForeignKey,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Theme(Base):
    __tablename__ = 'themes'
    uid = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    score = Column(Float, default=0)
    videos = relationship('Video')


class Video(Base):
    __tablename__ = 'videos'
    uid = Column(Integer, primary_key=True)
    name = Column(Text)
    theme_uid = Column(Integer, ForeignKey('themes.uid'))
    thumbs_up = Column(Integer, default=0)
    thumbs_down = Column(Integer, default=0)


class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'group:editors', 'edit')]

    def __init__(self, request):
        pass
