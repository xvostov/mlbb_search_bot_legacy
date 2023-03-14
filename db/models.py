from sqlalchemy import String, Boolean, Column, ForeignKey, Enum
from sqlalchemy.dialects.mysql import BIGINT as BigInteger, TINYINT as TinyInteger, MEDIUMINT as MediumInteger
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from db.enums import ROLES

class BaseModel(DeclarativeBase):
    pass

class User(BaseModel):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(BigInteger(unsigned=True), primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    has_tg_premium: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    has_bot_premium: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class Profile(BaseModel):
    __tablename__ = 'profiles'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    nickname: Mapped[str] = mapped_column(String(255))
    last_season_rank: Mapped[int] = mapped_column(TinyInteger(unsigned=True))
    current_ran: Mapped[int] = mapped_column(TinyInteger(unsigned=True))
    current_pts: Mapped[int] = mapped_column(MediumInteger(unsigned=True), nullable=True)
    max_rank: Mapped[int] = mapped_column(TinyInteger)
    current_win_rate: Mapped[int] = mapped_column(TinyInteger(unsigned=True))
    first_role: Mapped[Enum] = mapped_column(ROLES)
    second_role: Mapped[Enum] = mapped_column(ROLES)
    main_characters: Mapped[str] = mapped_column(String(255))
    voice_communication: Mapped[bool] = mapped_column(Boolean)

class UserFilter(BaseModel):
    __tablename__ = 'users_filters'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), primary_key=True)
    min_rank: Mapped[int] = mapped_column(TinyInteger)
    min_pts: Mapped[int] = mapped_column(MediumInteger(unsigned=True), nullable=True)
    min_win_rate: Mapped[int] = mapped_column(TinyInteger(unsigned=True))
    voice_communication: Mapped[bool] = mapped_column(Boolean)


class View(BaseModel):
    __tablename__ = 'views'
    id: Mapped[int] = mapped_column(BigInteger(unsigned=True), primary_key=True)
    observer_user_id: Mapped[int] = mapped_column(ForeignKey('profiles.user_id', ondelete='CASCADE'))
    observed_user_id = Column(String(50))
