
import sqlalchemy

# ROLES = Enum('Marksman', 'Mage', 'Tank', 'Support', 'Assassin', 'Fighter')
# RANKS = Enum('Warrior', 'Elite', 'Master', 'Grandmaster', 'Epic', 'Legend', 'Mythic', 'Mythic Glory')


# RANKS = sqlalchemy.Enum('Воин', 'Элита', 'Мастер', 'Грандмастер', 'Эпический', 'Легенда', 'Мифический', 'Мифическая слава')
ROLES = sqlalchemy.Enum('Стрелок', 'Маг', 'Танк', 'Поддержка', 'Убийца', 'Боец')
