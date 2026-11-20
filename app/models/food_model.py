from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Food(Base):
    __tablename__ = "foods"
    id : Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str] = mapped_column(String(100), nullable = False)
    description : Mapped[str] = mapped_column(String(500), nullable = False)
    price : Mapped[float] = mapped_column(nullable = False)
    category : Mapped[str] = mapped_column(String(100), nullable = False)
    restaurant_id : Mapped[int] = mapped_column(ForeignKey("restaurants.id"), nullable = False)
    restaurant : Mapped["Restaurant"] = relationship(back_populates = "foods")

class Restaurant(Base):
    __tablename__ = "restaurants"
    id : Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str] = mapped_column(String(100), nullable = False)
    location : Mapped[str] = mapped_column(String(100), nullable = False)
    owner_id : Mapped[int] = mapped_column(ForeignKey("users.id"),nullable = False)
    owner : Mapped["User"] = relationship(back_populates = "restaurants")
    foods : Mapped[list["Food"]] = relationship(back_populates = "restaurant")

class User(Base):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key = True)

    username : Mapped[str] = mapped_column(
        String(100), unique = True, nullable = False
    )

    email : Mapped[str] = mapped_column(
        String(150), unique = True, nullable = False
    )

    hashed_password : Mapped[str] = mapped_column(
        String(255), nullable = False
    )

    is_active : Mapped[bool] = mapped_column(
        Boolean, default = True, nullable = False
    )

    restaurants : Mapped[list["Restaurant"]] = relationship(back_populates = "owner")