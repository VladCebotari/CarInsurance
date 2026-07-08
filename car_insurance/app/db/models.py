import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.utils.enums.car_category import CarCategory
from app.utils.enums.driver_license_category import DriverLicenseCategory


class Base(DeclarativeBase):
    pass


class Owner(Base):
    __tablename__ = "owners"
    __table_args__ = (
        CheckConstraint(
            "length(name) BETWEEN 1 AND 255 "
            "AND name ~ '^[A-Za-z]+( [A-Za-z]+)*$'",
            name="ck_owners_name_format",
        ).ddl_if(dialect="postgresql"),
        CheckConstraint(
            "birthdate >= DATE '1900-01-01' AND birthdate <= CURRENT_DATE",
            name="ck_owners_birthdate_range",
        ).ddl_if(dialect="postgresql"),
        CheckConstraint(
            "year_of_driver_license BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE)",
            name="ck_owners_license_year_range",
        ).ddl_if(dialect="postgresql"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    birthdate: Mapped[date] = mapped_column(Date, nullable=False)
    year_of_driver_license: Mapped[int] = mapped_column(Integer, nullable=False)

    driver_license_cat: Mapped[DriverLicenseCategory | None] = mapped_column(
        SqlEnum(
            DriverLicenseCategory,
            values_callable=lambda enum: [item.value for item in enum],
            native_enum=False,
            create_constraint=True,
            length=4,
        ),
        nullable=True,
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
    )

    cars: Mapped[list["Car"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class Car(Base):
    __tablename__ = "cars"
    __table_args__ = (
        CheckConstraint(
            "length(vin) BETWEEN 1 AND 16 AND vin ~ '^[A-Za-z0-9]+$'",
            name="ck_cars_vin_format",
        ).ddl_if(dialect="postgresql"),
        CheckConstraint(
            "make IS NULL OR (length(make) BETWEEN 1 AND 150 "
            "AND make ~ '^[A-Za-z0-9]+( [A-Za-z0-9]+)*$')",
            name="ck_cars_make_format",
        ).ddl_if(dialect="postgresql"),
        CheckConstraint(
            "model IS NULL OR (length(model) BETWEEN 1 AND 150 "
            "AND model ~ '^[A-Za-z0-9]+( [A-Za-z0-9]+)*$')",
            name="ck_cars_model_format",
        ).ddl_if(dialect="postgresql"),
        CheckConstraint(
            "year_of_manufacture BETWEEN 1900 AND EXTRACT(YEAR FROM CURRENT_DATE)",
            name="ck_cars_year_of_manufacture_range",
        ).ddl_if(dialect="postgresql"),
        CheckConstraint("cc BETWEEN 1 AND 10000", name="ck_cars_cc_range").ddl_if(
            dialect="postgresql"
        ),
        CheckConstraint("power BETWEEN 1 AND 500", name="ck_cars_power_range").ddl_if(
            dialect="postgresql"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4,
    )

    vin: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    make: Mapped[str | None] = mapped_column(String(150), nullable=True)
    model: Mapped[str | None] = mapped_column(String(150), nullable=True)
    year_of_manufacture: Mapped[int] = mapped_column(Integer, nullable=False)
    category: Mapped[CarCategory | None] = mapped_column(
        SqlEnum(
            CarCategory,
            values_callable=lambda enum: [item.value for item in enum],
            native_enum=False,
            create_constraint=True,
            length=8,
        ),
        nullable=True,
    )
    cc: Mapped[int] = mapped_column(Integer, nullable=False)
    power: Mapped[int] = mapped_column(Integer, nullable=False)

    owner_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("owners.id", ondelete="CASCADE"),
        nullable=False,
    )

    owner: Mapped["Owner"] = relationship(back_populates="cars")
    # TO DO: Add needed relationships
