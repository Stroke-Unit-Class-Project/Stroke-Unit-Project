from django.urls import path
from . import views

urlpatterns = [
    path('', views.role_select, name='role-select'),
    path('set-role/<str:role>/', views.set_role, name='set-role'),
    path('patients/', views.PatientListView.as_view(), name='patient-list'),
    path('patient/new/', views.PatientCreateView.as_view(), name='patient-create'),
    path('patient/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('patient/<int:pk>/vital-signs/', views.add_vital_signs, name='add-vital-signs'),
    path('patient/<int:pk>/lab-results/', views.add_lab_results, name='add-lab-results'),
    path('patient/<int:pk>/imaging-study/', views.add_imaging_study, name='add-imaging-study'),
    path('patient/<int:pk>/consultation/', views.add_consultation, name='add-consultation'),
    path('notification/<int:notification_id>/read/', views.mark_notification_read, name='mark-notification-read'),
] 