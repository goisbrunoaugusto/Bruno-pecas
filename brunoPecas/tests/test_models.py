import pytest
from django.core.exceptions import ValidationError
from cars.models import CarModel
from parts.models import Part
from django.db import IntegrityError
from decimal import Decimal

@pytest.mark.django_db
class TestCarModel:
    def test_create_car(self, sample_car):
        assert str(sample_car) == "Test Car - Test Manufacturer (2024)"
        assert sample_car.manufacturer == "Test Manufacturer"
        assert sample_car.name == "Test Car"
        assert sample_car.year == 2024

    def test_car_part_relationship(self, sample_car, sample_part):
        sample_car.parts.add(sample_part)
        assert sample_part in sample_car.parts.all()

    @pytest.mark.parametrize(
        "name,manufacturer,year,details,valid",
        [
            ("", "Test", 2024, "Test", False),
            ("Test", "", 2024, "Test", False),
            ("Test", "Test", 0, "Test", True),
            ("Test", "Test", 2024, "", True),
        ],
    )
    def test_car_validation(self, name, manufacturer, year, details, valid):
        if not valid:
            with pytest.raises(ValidationError):
                car = CarModel(
                    name=name,
                    manufacturer=manufacturer,
                    year=year,
                    details=details
                )
                car.full_clean()
        else:
            car = CarModel(
                name=name,
                manufacturer=manufacturer,
                year=year,
                details=details
            )
            car.full_clean()

@pytest.mark.django_db
class TestPartModel:
    def test_create_part(self, sample_part):
        assert str(sample_part) == "1 - Test Part"
        assert sample_part.price == 99.99
        assert sample_part.quantity == 10

    def test_unique_part_number(self):
        Part.objects.create(
            part_number=1,
            name="Test Part 1",
            price=99.99,
            quantity=10
        )
        with pytest.raises(IntegrityError):
            Part.objects.create(
                part_number=1,
                name="Test Part 2",
                price=99.99,
                quantity=10
            )

    @pytest.mark.parametrize(
        "part_number,name,price,quantity,valid",
        [
            (1, "", 99.99, 10, False),
            (1, "Test", -99.99, 10, False),
            (1, "Test", 99.99, -10, False),
            (None, "Test", 99.99, 10, False),
            (1, "Test", Decimal('99.99'), 10, True),
        ],
    )
    def test_part_validation(self, part_number, name, price, quantity, valid):
        if not valid:
            with pytest.raises((ValidationError, IntegrityError)):
                part = Part(
                    part_number=part_number,
                    name=name,
                    price=price,
                    quantity=quantity
                )
                part.full_clean()
        else:
            part = Part(
                part_number=part_number,
                name=name,
                price=price,
                quantity=quantity
            )
            part.full_clean()