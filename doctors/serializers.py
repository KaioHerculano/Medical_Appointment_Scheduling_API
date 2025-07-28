from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from datetime import date
from dateutil.relativedelta import relativedelta
import re

from .models import Doctor
from core.fields import CPFField, PhoneField


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Doctor, com tratamento e validação avançada de dados.
    """

    cpf = CPFField(
        validators=[
            UniqueValidator(
                queryset=Doctor.objects.all(),
                message="Já existe um médico cadastrado com este CPF.",
            )
        ]
    )

    phone = PhoneField()

    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate_name(self, value):
        """Remove espaços e aplica capitalização padrão."""
        return value.strip().title()

    def validate_email(self, value):
        """Remove espaços e converte para minúsculas para padronização."""
        return value.strip().lower()

    def validate_crm_number(self, value):
        """Garante que o CRM tenha apenas os dígitos."""
        return re.sub(r"\D", "", str(value))

    def validate_specialty(self, value):
        """Remove espaços em branco do início e do fim."""
        return value.strip()

    def validate_address(self, value):
        """Remove espaços em branco do início e do fim."""
        return value.strip()

    def validate_date_of_birth(self, value):
        """
        Validação de regra de negócio: o médico deve ter pelo menos 25 anos.
        """
        today = date.today()
        age = relativedelta(today, value).years

        if age < 25:
            raise serializers.ValidationError(
                "O médico deve ter no mínimo 25 anos de idade."
            )

        return value
