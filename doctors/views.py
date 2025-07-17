from rest_framework import generics
from . import models
from .serializers import DoctorSerializer


class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Doctor.objects.all()
    serializer_class = DoctorSerializer
