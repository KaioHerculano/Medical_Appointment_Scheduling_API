from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from . import models
from .serializers import ConsultationSerializer
from app.permissions import GlobalDefaultPermission


class ConsultationListCreateView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Consultation.objects.all()
    serializer_class = ConsultationSerializer


class ConsultationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = models.Consultation.objects.all()
    serializer_class = ConsultationSerializer


class ConsultationByDoctorView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    serializer_class = ConsultationSerializer

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return models.Consultation.objects.filter(doctor_id=doctor_id)
