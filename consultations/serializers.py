from rest_framework import serializers

from . import models


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Consultation
        fields = "__all__"
