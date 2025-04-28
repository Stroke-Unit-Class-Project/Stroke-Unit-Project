from django.contrib import admin
from .models import Patient, VitalSigns, LabResults, ImagingStudy, Consultation

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'sex', 'created_at')
    search_fields = ('name',)
    list_filter = ('sex', 'created_at')

@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'systolic_bp', 'diastolic_bp', 'heart_rate', 'oxygen_saturation', 'timestamp')
    list_filter = ('timestamp',)

@admin.register(LabResults)
class LabResultsAdmin(admin.ModelAdmin):
    list_display = ('patient', 'cbc_status', 'bmp_status', 'glucose_level', 'coagulation_status', 'timestamp')
    list_filter = ('timestamp',)

@admin.register(ImagingStudy)
class ImagingStudyAdmin(admin.ModelAdmin):
    list_display = ('patient', 'study_type', 'timestamp')
    list_filter = ('study_type', 'timestamp')

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diagnosis', 'NIHSS_score', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('diagnosis', 'treatment_plan')
