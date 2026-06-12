from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from database import Base


class GameResult(Base):
    __tablename__ = "game_results"

    id = Column(Integer, primary_key=True, index=True)

    difficulty = Column(String, nullable=False)

    result = Column(String, nullable=False)

    moves = Column(Integer, nullable=False)

    completion_time = Column(Float, nullable=False)