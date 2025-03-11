from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from typing import List

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50), nullable=True)
    email = mapped_column(String(100), nullable=False)
    password = mapped_column(String(100), nullable=False) 
    
    favorite_characters: Mapped[List["FavoriteCharacters"]] = relationship(back_populates="user")
    favorite_planets: Mapped[List["FavoritePlanets"]] = relationship(back_populates="user")
    favorite_vehicles: Mapped[List["FavoriteVehicles"]] = relationship(back_populates="user")
    favorite_spaceships: Mapped[List["FavoriteSpaceships"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__ = "planets"
    id = mapped_column(Integer, primary_key=True)
    planet_name = mapped_column(String(50), nullable=False)
    population = mapped_column(String(20), nullable=False)
    area = mapped_column(String(10), nullable=False)
    
    favorite_planets: Mapped[List["FavoritePlanets"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id_planet": self.id,
            "planet_name": self.planet_name
        }

class Characters(db.Model):
    __tablename__ = "characters"
    id = mapped_column(Integer, primary_key=True)
    character_name = mapped_column(String(50), nullable=False)
    eye_color = mapped_column(String(100), nullable=False)
    hair_color = mapped_column(String(20), nullable=False)
    height = mapped_column(String(10), nullable=False)
    
    favorite_characters: Mapped[List["FavoriteCharacters"]] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "character_name": self.character_name
        }

class Vehicles(db.Model):
    __tablename__ = "vehicles"
    id = mapped_column(Integer, primary_key=True)
    vehicle_name = mapped_column(String(50), nullable=False)
    model = mapped_column(String(50), nullable=False)
    passengers = mapped_column(String(10), nullable=False)

    favorite_vehicles: Mapped[List["FavoriteVehicles"]] = relationship(back_populates="vehicle")

    def serialize(self):
        return {
            "id": self.id,
            "vehicle_name": self.vehicle_name,
            "model": self.model,
            "passengers": self.passengers
        }

class Spaceships(db.Model):
    __tablename__ = "spaceships"
    id = mapped_column(Integer, primary_key=True)
    spaceship_name = mapped_column(String(50), nullable=False)
    model = mapped_column(String(50), nullable=False)
    passengers = mapped_column(String(10), nullable=False)
    favorite_spaceships: Mapped[List["FavoriteSpaceships"]] = relationship(back_populates="spaceship")

    def serialize(self):
        return {
            "id": self.id,
            "spaceship_name": self.spaceship_name,
            "model": self.model,
            "passengers": self.passengers

        }

class FavoriteCharacters(db.Model):
    __tablename__ = "favorite_characters"
    id = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"))

    user = relationship("User", back_populates="favorite_characters")
    character = relationship("Characters", back_populates="favorite_characters")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

class FavoritePlanets(db.Model):
    __tablename__ = "favorite_planets"
    id = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planets.id"))

    user = relationship("User", back_populates="favorite_planets")
    planet = relationship("Planets", back_populates="favorite_planets")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }

class FavoriteVehicles(db.Model):
    __tablename__ = "favorite_vehicles"
    id = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))

    user = relationship("User", back_populates="favorite_vehicles")
    vehicle = relationship("Vehicles", back_populates="favorite_vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "vehicle_id": self.vehicle_id
        }

class FavoriteSpaceships(db.Model):
    __tablename__ = "favorite_spaceships"
    id = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    spaceship_id: Mapped[int] = mapped_column(ForeignKey("spaceships.id"))

    user = relationship("User", back_populates="favorite_spaceships")
    spaceship = relationship("Spaceships", back_populates="favorite_spaceships")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "spaceship_id": self.spaceship_id
        }
