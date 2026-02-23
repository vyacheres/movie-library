from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    release_date = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)  # in minutes
    rating = Column(Float, nullable=True)
    poster_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign Keys
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=False)
    director_id = Column(Integer, ForeignKey("directors.id"), nullable=False)

    # Relationships
    genre = relationship("Genre", back_populates="movies")
    director = relationship("Director", back_populates="movies")
    favorites = relationship("Favorite", back_populates="movie")
