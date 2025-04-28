from django import forms
from .models import Patient, VitalSigns, LabResults, ImagingStudy, Consultation

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'age', 'sex', 'chief_complaint', 'medical_history']
        widgets = {
            'chief_complaint': forms.Textarea(attrs={'rows': 3}),
            'medical_history': forms.Textarea(attrs={'rows': 3}),
        }

class VitalSignsForm(forms.ModelForm):
    class Meta:
        model = VitalSigns
        fields = ['systolic_bp', 'diastolic_bp', 'heart_rate', 'respiratory_rate', 'oxygen_saturation']
        labels = {
            'systolic_bp': 'Systolic Blood Pressure (mmHg)',
            'diastolic_bp': 'Diastolic Blood Pressure (mmHg)',
            'heart_rate': 'Heart Rate (bpm)',
            'respiratory_rate': 'Respiratory Rate (breaths/min)',
            'oxygen_saturation': 'Oxygen Saturation (%)',
        }

class LabResultsForm(forms.ModelForm):
    class Meta:
        model = LabResults
        fields = ['cbc_status', 'bmp_status', 'glucose_level', 'coagulation_status']
        labels = {
            'cbc_status': 'Complete Blood Count Status',
            'bmp_status': 'Basic Metabolic Panel Status',
            'glucose_level': 'Glucose Level (mg/dL)',
            'coagulation_status': 'Coagulation Studies Status',
        }

class ImagingStudyForm(forms.ModelForm):
    class Meta:
        model = ImagingStudy
        fields = ['study_type', 'findings', 'image_url']
        widgets = {
            'findings': forms.Textarea(attrs={'rows': 3}),
        }

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['diagnosis', 'treatment_plan', 'neurologist_notes', 'NIHSS_score']
        widgets = {
            'treatment_plan': forms.Textarea(attrs={'rows': 3}),
            'neurologist_notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'NIHSS_score': 'NIHSS Score (0-42)',
        } 