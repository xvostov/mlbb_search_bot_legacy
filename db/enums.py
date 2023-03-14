import sqlalchemy as sa

ROLES = sa.Enum('Стрелок', 'Маг', 'Танк', 'Поддержка', 'Убийца', 'Боец')