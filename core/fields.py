import re

from rest_framework import serializers
from validate_docbr import CPF


class CPFField(serializers.CharField):
    """
    Campo customizado para CPF com validação reforçada
    """

    def to_internal_value(self, data):
        clean_cpf = re.sub(r"\D", "", data)

        if len(clean_cpf) != 11:
            raise serializers.ValidationError("CPF deve ter 11 dígitos.")

        if clean_cpf == clean_cpf[0] * 11:
            raise serializers.ValidationError("CPF inválido.")

        cpf = CPF()
        if not cpf.validate(clean_cpf):
            raise serializers.ValidationError("CPF inválido.")

        return clean_cpf

    def to_representation(self, value):
        return value


class PhoneField(serializers.CharField):
    """
    Campo customizado para número de telefone
    """

    def to_internal_value(self, data):
        clean_phone = re.sub(r"\D", "", data)

        if len(clean_phone) not in (10, 11):
            raise serializers.ValidationError("Número de telefone inválido.")

        return clean_phone

    def to_representation(self, value):
        if len(value) == 11:
            return f"({value[:2]}) {value[2:7]}-{value[7:]}"
        elif len(value) == 10:
            return f"({value[:2]}) {value[2:6]}-{value[6:]}"
        return value
