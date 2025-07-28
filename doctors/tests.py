from django.contrib.auth.models import Permission, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Doctor


class DoctorAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        permissions = Permission.objects.filter(
            codename__in=["view_doctor", "add_doctor", "change_doctor", "delete_doctor"]
        )
        self.user.user_permissions.set(permissions)
        self.user.save()

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        self.doctor = Doctor.objects.create(
            name="Dr. Teste",
            cpf="26208784620",
            crm_number="123456",
            crm_state="SP",
            specialty="Cardiology",
            phone="11999999999",
            email="dr.teste@example.com",
            address="Rua Teste, 123",
            date_of_birth="1980-01-01",
        )

    def test_get_doctor_list(self):
        url = reverse("doctor-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_doctor(self):
        url = reverse("doctor-list-create")
        data = {
            "name": "Dr. Novo",
            "cpf": "042.815.546-45",
            "crm_number": "654321",
            "crm_state": "RJ",
            "specialty": "Neurology",
            "phone": "21988888888",
            "email": "dr.novo@example.com",
            "address": "Av. Novo, 100",
            "date_of_birth": "1975-05-05",
            "status": "active",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_doctor(self):
        url = reverse("doctor-list-create")
        data = {"name": "", "cpf": "11111111111"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_doctor(self):
        url = reverse("doctor-detail-view", kwargs={"pk": self.doctor.id})
        data = {
            "name": "Dr. Atualizado",
            "cpf": self.doctor.cpf,
            "crm_number": "123456",
            "crm_state": "SP",
            "specialty": "Generalist",
            "phone": "11911112222",
            "email": "dr.atualizado@example.com",
            "address": "Rua Nova, 456",
            "date_of_birth": "1980-01-01",
            "status": "inactive",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_doctor(self):
        url = reverse("doctor-detail-view", kwargs={"pk": self.doctor.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_access(self):
        self.client.credentials()
        url = reverse("doctor-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
