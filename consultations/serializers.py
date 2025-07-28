from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from .fields import PhoneField
from .models import Consultation


class ConsultationSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(
        write_only=True,
        format="%Y-%m-%d",
        help_text="Data de início no formato AAAA-MM-DD.",
    )
    start_time = serializers.TimeField(
        write_only=True, format="%H:%M", help_text="Hora de início no formato HH:MM."
    )
    end_date = serializers.DateField(
        write_only=True,
        format="%Y-%m-%d",
        help_text="Data de fim no formato AAAA-MM-DD.",
    )
    end_time = serializers.TimeField(
        write_only=True, format="%H:%M", help_text="Hora de fim no formato HH:MM."
    )

    patient_phone = PhoneField(allow_blank=True, required=False)

    class Meta:
        model = Consultation
        fields = [
            "id",
            "doctor",
            "patient_name",
            "patient_email",
            "patient_phone",
            "symptoms_description",
            "notes",
            "status",
            "start_datetime",
            "end_datetime",
            "start_date",
            "start_time",
            "end_date",
            "end_time",
        ]
        read_only_fields = (
            "created_at",
            "updated_at",
            "start_datetime",
            "end_datetime",
        )

    def validate(self, data):
        """
        Pega os 4 campos de data/hora, combina-os em start_datetime e end_datetime,
        e executa as validações de negócio.
        """
        start_datetime_aware = timezone.make_aware(
            datetime.combine(data.pop("start_date"), data.pop("start_time"))
        )
        end_datetime_aware = timezone.make_aware(
            datetime.combine(data.pop("end_date"), data.pop("end_time"))
        )

        if start_datetime_aware >= end_datetime_aware:
            raise serializers.ValidationError(
                "O horário de término deve ser posterior ao de início."
            )

        if not self.instance and start_datetime_aware < timezone.now():
            raise serializers.ValidationError(
                "Não é possível agendar uma consulta no passado."
            )

        doctor = data.get("doctor")
        if doctor:
            overlapping = Consultation.objects.filter(
                doctor=doctor,
                start_datetime__lt=end_datetime_aware,
                end_datetime__gt=start_datetime_aware,
            )
            if self.instance:
                overlapping = overlapping.exclude(pk=self.instance.pk)

            if overlapping.exists():
                raise serializers.ValidationError(
                    "O médico já possui uma consulta neste horário."
                )

        data["start_datetime"] = start_datetime_aware
        data["end_datetime"] = end_datetime_aware

        return data
