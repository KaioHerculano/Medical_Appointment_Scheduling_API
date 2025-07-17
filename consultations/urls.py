from django.urls import path
from . import views


urlpatterns = [
    path('consultations/', views.ConsultationListCreateView.as_view(), name='consultation-list-create'),
    path('consultations/<int:pk>/', views.ConsultationRetrieveUpdateDestroyView.as_view(), name='consultation-detail-view'),
    path('consultations/doctor/<int:doctor_id>/', views.ConsultationByDoctorView.as_view(), name='consultation-by-doctor'),
]
