from django.utils import timezone
from rest_framework import serializers

from . import models


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Consultation
        fields = "__all__"

    def validate(self, data):
        start = data.get("start_datetime")
        end = data.get("end_datetime")
        doctor = data.get("doctor")

        # Validação segura para quando 'end' for None
        if start is not None and end is not None:
            if start >= end:
                raise serializers.ValidationError(
                    "A data/hora de início deve ser anterior à de término."
                )

        if start is not None and start < timezone.now():
            raise serializers.ValidationError(
                "Não é possível agendar uma consulta no passado."
            )

        # Verifica sobreposição de horários só se todos os campos necessários existirem
        if doctor is not None and start is not None and end is not None:
            overlapping = models.Consultation.objects.filter(
                doctor=doctor,
                start_datetime__lt=end,
                end_datetime__gt=start,
            )
            if self.instance:
                overlapping = overlapping.exclude(id=self.instance.id)

            if overlapping.exists():
                raise serializers.ValidationError(
                    "Este horário já está reservado para este médico."
                )

        return data
