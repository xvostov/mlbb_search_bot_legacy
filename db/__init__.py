from loader import DB_ENGINE
from .models import Base

Base.metadata.create_all(DB_ENGINE)
