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
            codename__in=[
                "view_doctor",
                "add_doctor",
                "change_doctor",
                "delete_doctor",
            ]
        )

        self.user.user_permissions.set(permissions)
        self.user.save()

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.doctor = Doctor.objects.create(
            name="Dr. Teste",
            cpf="123.456.789-00",
            crm_number="123456",
            crm_state="SP",
            specialty="Cardiology",
            phone="11999999999",
            email="dr.teste@example.com",
            address="Rua Teste, 123",
            date_of_birth="1980-01-01",
            status="active",
        )

    def test_get_doctor_list(self):
        url = reverse("doctor-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_create_doctor(self):
        url = reverse("doctor-list-create")
        data = {
            "name": "Dr. Novo",
            "cpf": "987.654.321-00",
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
        self.assertEqual(Doctor.objects.count(), 2)
        self.assertEqual(Doctor.objects.get(id=response.data["id"]).name, "Dr. Novo")

    def test_invalid_create_doctor(self):
        url = reverse("doctor-list-create")
        data = {
            "name": "",
            "cpf": "invalid_cpf",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_doctor(self):
        url = reverse("doctor-detail-view", kwargs={"pk": self.doctor.id})
        data = {
            "name": "Dr. Atualizado",
            "cpf": self.doctor.cpf,
            "crm_number": self.doctor.crm_number,
            "crm_state": self.doctor.crm_state,
            "specialty": self.doctor.specialty,
            "phone": self.doctor.phone,
            "email": self.doctor.email,
            "address": self.doctor.address,
            "date_of_birth": str(self.doctor.date_of_birth),
            "status": "inactive",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.doctor.refresh_from_db()
        self.assertEqual(self.doctor.name, "Dr. Atualizado")
        self.assertEqual(self.doctor.status, "inactive")

    def test_delete_doctor(self):
        url = reverse("doctor-detail-view", kwargs={"pk": self.doctor.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Doctor.objects.filter(id=self.doctor.id).exists())

    def test_unauthenticated_access(self):
        self.client.credentials()
        url = reverse("doctor-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
