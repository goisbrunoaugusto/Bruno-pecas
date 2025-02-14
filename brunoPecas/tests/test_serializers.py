import pytest
from cars.serializers import CarModelSerializer, CarModelDetailSerializer
from parts.serializers import PartSerializer, PartDetailsSerializer
from users.serializers import UserSerializer

@pytest.mark.django_db
class TestCarSerializers:
    def test_car_serializer(self, sample_car):
        serializer = CarModelSerializer(sample_car)
        assert serializer.data['name'] == sample_car.name
        assert serializer.data['year'] == sample_car.year

    def test_car_detail_serializer(self, sample_car, sample_part):
        sample_car.parts.add(sample_part)
        serializer = CarModelDetailSerializer(sample_car)
        assert serializer.data['name'] == sample_car.name
        assert len(serializer.data['parts']) == 1
        assert serializer.data['parts'][0]['name'] == sample_part.name

@pytest.mark.django_db
class TestPartSerializers:
    def test_part_serializer(self, sample_part):
        serializer = PartSerializer(sample_part)
        assert serializer.data['name'] == sample_part.name
        assert float(serializer.data['price']) == 99.99

    def test_part_details_serializer(self, sample_part, sample_car):
        sample_car.parts.add(sample_part)
        serializer = PartDetailsSerializer(sample_part)
        assert serializer.data['name'] == sample_part.name
        assert sample_car.name in serializer.data['car_models']

@pytest.mark.django_db
class TestUserSerializer:
    def test_user_serializer_create(self):
        data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpass123",
            "role": "REGULAR"
        }
        serializer = UserSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.username == "testuser"
        assert user.check_password("testpass123")