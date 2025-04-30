from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

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
    is_critical = models.BooleanField(default=False)

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

    def is_critical(self):
        return (
            self.systolic_bp > 180 or self.systolic_bp < 90 or
            self.diastolic_bp > 120 or self.diastolic_bp < 60 or
            self.heart_rate > 120 or self.heart_rate < 50 or
            self.respiratory_rate > 30 or self.respiratory_rate < 10 or
            self.oxygen_saturation < 92
        )

class LabResults(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_results')
    cbc_status = models.CharField(max_length=50)
    bmp_status = models.CharField(max_length=50)
    glucose_level = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    coagulation_status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_critical(self):
        return (
            self.glucose_level and (self.glucose_level > 200 or self.glucose_level < 70) or
            'abnormal' in self.cbc_status.lower() or
            'abnormal' in self.bmp_status.lower() or
            'abnormal' in self.coagulation_status.lower()
        )

class ImagingStudy(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='imaging_studies')
    study_type = models.CharField(max_length=50)
    findings = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_critical(self):
        return any(keyword in self.findings.lower() for keyword in [
            'stroke', 'hemorrhage', 'infarct', 'ischemia', 'critical', 'urgent'
        ])

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    diagnosis = models.CharField(max_length=200)
    treatment_plan = models.TextField()
    neurologist_notes = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    NIHSS_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(42)])

    def is_critical(self):
        return self.NIHSS_score >= 15

    def __str__(self):
        return f"Consultation for {self.patient.name} at {self.timestamp}"

class Notification(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50)  # e.g., 'vitals', 'lab', 'imaging', 'consultation'

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_severity_display()} alert for {self.patient.name}: {self.message}"
