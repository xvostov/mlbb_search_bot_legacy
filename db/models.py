from sqlalchemy import String, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.mysql import BIGINT as BigInteger, TINYINT as TinyInteger, MEDIUMINT as MediumInteger
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from db.enums import ROLES, REGIONS


class BaseModel(DeclarativeBase):
    def __repr__(self):
        obj_attrs_dict = self.__dict__
        return ', '.join([f"{key}={obj_attrs_dict.get(key)}" for key in obj_attrs_dict if key[0] != "_"])


class User(BaseModel):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(BigInteger(unsigned=True), primary_key=True)
    username: Mapped[str] = mapped_column(String(32), nullable=True)
    first_name: Mapped[str] = mapped_column(String(32), nullable=True)
    last_name: Mapped[str] = mapped_column(String(32), nullable=True)
    has_tg_premium: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_bot_premium: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)


class Profile(BaseModel):
    __tablename__ = 'profiles'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    nickname: Mapped[str] = mapped_column(String(255))
    last_season_rank: Mapped[int] = mapped_column(TinyInteger(unsigned=True))
    current_rank: Mapped[int] = mapped_column(TinyInteger(unsigned=True))
    current_pts: Mapped[int] = mapped_column(MediumInteger(unsigned=True), nullable=True)
    max_rank: Mapped[int] = mapped_column(TinyInteger)
    current_win_rate: Mapped[int] = mapped_column(TinyInteger(unsigned=True))
    first_role: Mapped[Enum] = mapped_column(ROLES)
    second_role: Mapped[Enum] = mapped_column(ROLES)
    main_characters: Mapped[str] = mapped_column(String(255))
    region: Mapped[Enum] = mapped_column(REGIONS)
    voice_communication: Mapped[bool] = mapped_column(Boolean)


class UserFilter(BaseModel):
    __tablename__ = 'users_filters'
    user_id: Mapped[int] = mapped_column(ForeignKey('profiles.user_id', ondelete='CASCADE'), primary_key=True)
    min_rank: Mapped[int] = mapped_column(TinyInteger)
    min_pts: Mapped[int] = mapped_column(MediumInteger(unsigned=True), nullable=True)
    min_win_rate: Mapped[int] = mapped_column(TinyInteger(unsigned=True))
    role: Mapped[Enum] = mapped_column(ROLES, nullable=True)


class View(BaseModel):
    __tablename__ = 'views'
    id: Mapped[int] = mapped_column(BigInteger(unsigned=True), primary_key=True)
    observer_user_id: Mapped[int] = mapped_column(ForeignKey('profiles.user_id', ondelete='CASCADE'))
    observed_user_id: Mapped[int] = mapped_column(ForeignKey('profiles.user_id', ondelete='CASCADE'))