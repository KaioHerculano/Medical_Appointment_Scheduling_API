from datetime import datetime

from django.utils import timezone
from rest_framework import serializers

from core.fields import PhoneField

from .models import Consultation


class ConsultationSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(write_only=True, format="%Y-%m-%d")
    start_time = serializers.TimeField(write_only=True, format="%H:%M")
    end_date = serializers.DateField(write_only=True, format="%Y-%m-%d")
    end_time = serializers.TimeField(write_only=True, format="%H:%M")
    patient_phone = PhoneField(allow_blank=True, required=False)

    class Meta:
        model = Consultation
        fields = "__all__"
        read_only_fields = (
            "created_at",
            "updated_at",
            "start_datetime",
            "end_datetime",
        )

    def validate(self, data):
        if all(k in data for k in ["start_date", "start_time", "end_date", "end_time"]):
            start_date_val = data["start_date"]
            start_time_val = data["start_time"]
            end_date_val = data["end_date"]
            end_time_val = data["end_time"]

            start_datetime_aware = timezone.make_aware(
                datetime.combine(start_date_val, start_time_val)
            )
            end_datetime_aware = timezone.make_aware(
                datetime.combine(end_date_val, end_time_val)
            )

            if start_datetime_aware >= end_datetime_aware:
                raise serializers.ValidationError(
                    "O horário de término deve ser posterior ao de início."
                )

            if not self.instance and start_datetime_aware < timezone.now():
                raise serializers.ValidationError(
                    "Não é possível agendar uma consulta no passado."
                )

            doctor = data.get("doctor") or (self.instance and self.instance.doctor)
            if doctor:
                overlapping = Consultation.objects.filter(
                    doctor=doctor,
                    start_datetime__lt=end_datetime_aware,
                    end_datetime__gt=start_datetime_aware,
                ).exclude(pk=getattr(self.instance, "pk", None))

                if overlapping.exists():
                    raise serializers.ValidationError(
                        "O médico já possui uma consulta neste horário."
                    )

            data["start_datetime"] = start_datetime_aware
            data["end_datetime"] = end_datetime_aware
        return data

    def create(self, validated_data):
        validated_data.pop("start_date", None)
        validated_data.pop("start_time", None)
        validated_data.pop("end_date", None)
        validated_data.pop("end_time", None)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("start_date", None)
        validated_data.pop("start_time", None)
        validated_data.pop("end_date", None)
        validated_data.pop("end_time", None)

        return super().update(instance, validated_data)
