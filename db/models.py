from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from db.enums import ROLES


class Base(DeclarativeBase):
    pass


class Profile(Base):
    __tablename__ = 'profiles'

    user_id = Column(String(50), primary_key=True)
    nickname = Column(String(255))
    last_season_rank = Column(Integer)
    current_rank = Column(Integer)
    current_pts = Column(Integer)
    max_rank = Column(Integer)
    current_win_rate = Column(Integer)
    first_role = Column(ROLES)
    second_role = Column(ROLES)
    main_characters = Column(String(250))
    voice_communication = Column(Boolean)
    user_filter = relationship('UserFilter', back_populates='profile', uselist=False, single_parent=True, lazy='joined',
                               cascade='all, delete')

    views = relationship('View', back_populates='profile', lazy='joined', cascade='all, delete', passive_deletes=True)


class UserFilter(Base):
    __tablename__ = 'users_filters'
    filter_id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(String(50), ForeignKey('profiles.user_id', ondelete='CASCADE'))
    min_rank = Column(Integer)
    min_pts = Column(Integer)
    min_win_rate = Column(Integer)
    voice_communication = Column(Boolean)
    profile = relationship('Profile', back_populates='user_filter', uselist=False)


class View(Base):
    __tablename__ = 'views'
    id = Column(Integer, autoincrement=True, primary_key=True)
    observer_user_id = Column(String(50), ForeignKey('profiles.user_id', ondelete='CASCADE'))
    observed_user_id = Column(String(50))
    profile = relationship('Profile', back_populates='views')
