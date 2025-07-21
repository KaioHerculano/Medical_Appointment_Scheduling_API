from django.db import models

from doctors.models import Doctor


class Consultation(models.Model):
    STATUS_CHOICES = [
        ("scheduled", "Agendada"),
        ("completed", "Concluída"),
        ("canceled", "Cancelada"),
    ]

    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="consultations"
    )
    patient_name = models.CharField("Nome do Paciente", max_length=100)
    patient_email = models.EmailField("E-mail do Paciente", blank=True, null=True)
    patient_phone = models.CharField(
        "Telefone do Paciente", max_length=20, blank=True, null=True
    )
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    symptoms_description = models.TextField("Descrição dos Sintomas")
    notes = models.TextField("Observações Adicionais", blank=True, null=True)
    status = models.CharField(
        "Status", max_length=10, choices=STATUS_CHOICES, default="scheduled"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_datetime"]
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"

    def __str__(self):
        return f"{self.patient_name} com {self.doctor.name} em {self.date.strftime('%d/%m/%Y %H:%M')}"
