from rest_framework import generics
from . import models 
from .serializers import ConsultationSerializer


class ConsultationListCreateView(generics.ListCreateAPIView):
    queryset = models.Consultation.objects.all()
    serializer_class = ConsultationSerializer


class ConsultationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Consultation.objects.all()
    serializer_class = ConsultationSerializer


class ConsultationByDoctorView(generics.ListAPIView):
    serializer_class = ConsultationSerializer

    def get_queryset(self):
        doctor_id = self.kwargs.get('doctor_id')
        return models.Consultation.objects.filter(doctor_id=doctor_id)