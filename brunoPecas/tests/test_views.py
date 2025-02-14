import pytest
from rest_framework import status
from django.urls import reverse
from parts.models import Part

@pytest.mark.django_db
class TestCarViews:
    def test_list_cars_authenticated(self, authenticated_regular_client, sample_car):
        url = reverse('car-list')
        response = authenticated_regular_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_list_cars_unauthenticated(self, api_client):
        url = reverse('car-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_car_as_admin(self, authenticated_admin_client):
        url = reverse('car-create')
        data = {
            "name": "New Car",
            "manufacturer": "New Manufacturer",
            "year": 2024,
            "details": "New Details"
        }
        response = authenticated_admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == "New Car"

    def test_create_car_as_regular_user(self, authenticated_regular_client):
        url = reverse('car-create')
        data = {
            "name": "New Car",
            "manufacturer": "New Manufacturer",
            "year": 2024,
            "details": "New Details"
        }
        response = authenticated_regular_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_car_unauthenticated(self, api_client):
        url = reverse('car-create')
        data = {
            "name": "New Car",
            "manufacturer": "New Manufacturer",
            "year": 2024,
            "details": "New Details"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    
    def test_retrieve_car_detail_authenticated(self, authenticated_regular_client, sample_car):
        url = reverse('car-detail', args=[sample_car.id])
        response = authenticated_regular_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == sample_car.name

    def test_retrieve_car_detail_unauthenticated(self, api_client, sample_car):
        url = reverse('car-detail', args=[sample_car.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_car_as_admin(self, authenticated_admin_client, sample_car):
        url = reverse('car-update', args=[sample_car.id])
        data = {
            "name": "Updated Car",
            "manufacturer": "Updated Manufacturer",
            "year": 2025,
            "details": "Updated Details"
        }
        response = authenticated_admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == "Updated Car"

    def test_update_car_as_regular_user(self, authenticated_regular_client, sample_car):
        url = reverse('car-update', args=[sample_car.id])
        data = {
            "name": "Updated Car",
            "manufacturer": "Updated Manufacturer",
            "year": 2025,
            "details": "Updated Details"
        }
        response = authenticated_regular_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_car_unauthenticated(self, api_client, sample_car):
        url = reverse('car-update', args=[sample_car.id])
        data = {
            "name": "Updated Car",
            "manufacturer": "Updated Manufacturer",
            "year": 2025,
            "details": "Updated Details"
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_car_models_for_part_authenticated(self, authenticated_regular_client, sample_car, sample_part):
        sample_car.parts.add(sample_part)
        url = reverse('list-car-models-for-part', args=[sample_part.id])
        response = authenticated_regular_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == sample_car.name

    def test_list_car_models_for_part_unauthenticated(self, api_client, sample_car, sample_part):
        sample_car.parts.add(sample_part)
        
        url = reverse('list-car-models-for-part', args=[sample_part.id])
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
class TestPartViews:
    def test_associate_parts_as_admin(self, authenticated_admin_client, sample_part, sample_car):
        url = reverse('associate-parts')
        data = {
            "part_ids": [sample_part.id],
            "car_model_ids": [sample_car.id]
        }
        print('id do carro', sample_car.id)
        print('id da part', sample_part.id)
        print("Before association:", sample_car.parts.all())
        response = authenticated_admin_client.post(url, data)
        print("After association:", sample_car.parts.all())

        assert response.status_code == status.HTTP_200_OK
        assert sample_part in sample_car.parts.all()

    def test_associate_parts_as_regular_user(self, authenticated_regular_client, sample_part, sample_car):
        url = reverse('associate-parts')
        data = {
            "part_ids": [sample_part.id],
            "car_model_ids": [sample_car.id]
        }
        response = authenticated_regular_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_associate_parts_unauthenticated(self, api_client, sample_part, sample_car):
        url = reverse('associate-parts')
        data = {
            "part_ids": [sample_part.id],
            "car_model_ids": [sample_car.id]
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_associate_parts_invalid_data(self, authenticated_admin_client):
        url = reverse('associate-parts')
        data = {
            "part_ids": [999],
            "car_model_ids": [999]
        }
        response = authenticated_admin_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_disassociate_part_as_admin(self, authenticated_admin_client, sample_part, sample_car):
        sample_car.parts.add(sample_part)
        url = reverse('disassociate-part')
        data = {
            "part_id": sample_part.id,
            "car_model_id": sample_car.id
        }
        response = authenticated_admin_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert sample_part not in sample_car.parts.all()

    def test_disassociate_part_as_regular_user(self, authenticated_regular_client, sample_part, sample_car):
        sample_car.parts.add(sample_part)
        url = reverse('disassociate-part')
        data = {
            "part_id": sample_part.id,
            "car_model_id": sample_car.id
        }
        response = authenticated_regular_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_disassociate_part_unauthenticated(self, api_client, sample_part, sample_car):
        sample_car.parts.add(sample_part)
        url = reverse('disassociate-part')
        data = {
            "part_id": sample_part.id,
            "car_model_id": sample_car.id
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_disassociate_part_invalid_data(self, authenticated_admin_client):
        url = reverse('disassociate-part')
        data = {
            "part_id": 999,
            "car_model_id": 999
        }
        response = authenticated_admin_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_parts_for_car_model_authenticated(self, authenticated_regular_client, sample_car, sample_part):
        sample_car.parts.add(sample_part)
        url = reverse('list-parts-for-car-model', args=[sample_car.id])
        response = authenticated_regular_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == sample_part.name

    def test_list_parts_for_car_model_unauthenticated(self, api_client, sample_car, sample_part):
        sample_car.parts.add(sample_part)
        url = reverse('list-parts-for-car-model', args=[sample_car.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_parts_for_car_model_not_found(self, authenticated_regular_client):
        url = reverse('list-parts-for-car-model', args=[999])
        response = authenticated_regular_client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_parts_authenticated(self, authenticated_regular_client, sample_part):
        url = reverse('part-list')
        response = authenticated_regular_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_list_parts_unauthenticated(self, api_client, sample_part):
        url = reverse('part-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_retrieve_part_detail_authenticated(self, authenticated_regular_client, sample_part):
        url = reverse('part-detail', args=[sample_part.id])
        response = authenticated_regular_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == sample_part.name

    def test_retrieve_part_detail_unauthenticated(self, api_client, sample_part):
        url = reverse('part-detail', args=[sample_part.id])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_part_as_admin(self, authenticated_admin_client):
        url = reverse('part-create')
        data = {
            "part_number": 1,
            "name": "New Part",
            "price": "99.99",
            "quantity": 10
        }
        response = authenticated_admin_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == "New Part"

    def test_create_part_as_regular_user(self, authenticated_regular_client):
        url = reverse('part-create')
        data = {
            "part_number": 1,
            "name": "New Part",
            "price": "99.99",
            "quantity": 10
        }
        response = authenticated_regular_client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_part_unauthenticated(self, api_client):
        url = reverse('part-create')
        data = {
            "part_number": 1,
            "name": "New Part",
            "price": "99.99",
            "quantity": 10
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_part_as_admin(self, authenticated_admin_client, sample_part):
        url = reverse('part-update', args=[sample_part.id])
        data = {
            "part_number": 1,
            "name": "Updated Part",
            "price": "149.99",
            "quantity": 5
        }
        response = authenticated_admin_client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == "Updated Part"

    def test_update_part_as_regular_user(self, authenticated_regular_client, sample_part):
        url = reverse('part-update', args=[sample_part.id])
        data = {
            "part_number": 1,
            "name": "Updated Part",
            "price": "149.99",
            "quantity": 5
        }
        response = authenticated_regular_client.put(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_part_unauthenticated(self, api_client, sample_part):
        url = reverse('part-update', args=[sample_part.id])
        data = {
            "part_number": 1,
            "name": "Updated Part",
            "price": "149.99",
            "quantity": 5
        }
        response = api_client.put(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_part_as_admin(self, authenticated_admin_client, sample_part):
        url = reverse('part-delete', args=[sample_part.id])
        response = authenticated_admin_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Part.objects.filter(id=sample_part.id).exists()

    def test_delete_part_as_regular_user(self, authenticated_regular_client, sample_part):
        url = reverse('part-delete', args=[sample_part.id])
        response = authenticated_regular_client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_part_unauthenticated(self, api_client, sample_part):
        url = reverse('part-delete', args=[sample_part.id])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserViews:
    def test_register_user(self, api_client):
        url = reverse('register')
        data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpass123",
            "role": "REGULAR"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == "testuser"

    def test_token_obtain(self, api_client, regular_user):
        url = reverse('token_obtain_pair')
        data = {
            "username": "regular",
            "password": "testpass123"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data