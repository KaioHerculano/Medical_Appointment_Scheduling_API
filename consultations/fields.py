import re

from rest_framework import serializers


class PhoneField(serializers.CharField):
    """Campo que limpa o telefone na entrada e formata na saída."""

    def to_internal_value(self, data):
        return re.sub(r"\D", "", str(data))

    def to_representation(self, value):
        if len(value) == 11:
            return f"({value[0:2]}) {value[2:7]}-{value[7:11]}"
        if len(value) == 10:
            return f"({value[0:2]}) {value[2:6]}-{value[6:10]}"
        return value
