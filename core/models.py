from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)])
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    chief_complaint = models.TextField()
    medical_history = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.age})"

class VitalSigns(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_signs')
    systolic_bp = models.IntegerField()
    diastolic_bp = models.IntegerField()
    heart_rate = models.IntegerField()
    respiratory_rate = models.IntegerField()
    oxygen_saturation = models.DecimalField(max_digits=4, decimal_places=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vitals for {self.patient.name} at {self.timestamp}"

class LabResults(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_results')
    cbc_status = models.CharField(max_length=50)
    bmp_status = models.CharField(max_length=50)
    glucose_level = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    coagulation_status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

class ImagingStudy(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='imaging_studies')
    study_type = models.CharField(max_length=50)
    findings = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    diagnosis = models.CharField(max_length=200)
    treatment_plan = models.TextField()
    neurologist_notes = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    NIHSS_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(42)])
    
    def __str__(self):
        return f"Consultation for {self.patient.name} at {self.timestamp}"
