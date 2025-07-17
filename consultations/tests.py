from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Permission
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Consultation
from doctors.models import Doctor
from django.utils import timezone
import datetime


class ConsultationAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

        permissions = Permission.objects.filter(codename__in=[
            'view_consultation',
            'add_consultation',
            'change_consultation',
            'delete_consultation',
        ])
        self.user.user_permissions.set(permissions)
        self.user.save()

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.doctor = Doctor.objects.create(
            name='Dr. Teste',
            cpf='123.456.789-00',
            crm_number='123456',
            crm_state='SP',
            specialty='Cardiology',
            phone='11999999999',
            email='dr.teste@example.com',
            address='Rua Teste, 123',
            date_of_birth='1980-01-01',
            status='active',
        )

        aware_date = timezone.make_aware(datetime.datetime(2025, 7, 20, 10, 0, 0))
        self.consultation = Consultation.objects.create(
            patient_name='Paciente Teste',
            doctor=self.doctor,
            date=aware_date,
            symptoms_description='Sintomas iniciais',
            status='scheduled',
            notes='Consulta inicial',
        )

    def test_get_consultation_list(self):
        url = reverse('consultation-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_create_consultation(self):
        url = reverse('consultation-list-create')
        data = {
            "doctor": self.doctor.id,
            "patient_name": "Novo Paciente",
            "date": "2025-07-18T14:00:00Z",
            "symptoms_description": "Sintomas de teste",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Consultation.objects.get(id=response.data['id']).patient_name, "Novo Paciente")

    def test_invalid_create_consultation(self):
        url = reverse('consultation-list-create')
        data = {
            "patient_name": "",
            "doctor": 9999,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_consultation(self):
        url = reverse('consultation-detail-view', kwargs={'pk': self.consultation.id})
        data = {
            "doctor": self.doctor.id,
            "patient_name": "Paciente Atualizado",
            "date": self.consultation.date.isoformat(),
            "symptoms_description": "Sintomas atualizados",
            "status": "completed",
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.consultation.refresh_from_db()
        self.assertEqual(self.consultation.patient_name, "Paciente Atualizado")
        self.assertEqual(self.consultation.status, "completed")

    def test_delete_consultation(self):
        url = reverse('consultation-detail-view', kwargs={'pk': self.consultation.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Consultation.objects.filter(id=self.consultation.id).exists())

    def test_unauthenticated_access(self):
        self.client.credentials()
        url = reverse('consultation-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
