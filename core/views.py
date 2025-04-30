from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Patient, VitalSigns, LabResults, ImagingStudy, Consultation, Notification
from .forms import PatientForm, VitalSignsForm, LabResultsForm, ImagingStudyForm, ConsultationForm

# Create your views here.

def role_select(request):
    return render(request, 'core/role_select.html')

def set_role(request, role):
    if role in ['technician', 'neurologist']:
        request.session['role'] = role
        messages.success(request, f'You are now logged in as a {role}.')
        return redirect('patient-list')
    return redirect('role-select')

class PatientListView(ListView):
    model = Patient
    template_name = 'core/patient_list.html'
    context_object_name = 'patients'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.request.session.get('role')
        context['unread_notifications'] = Notification.objects.filter(is_read=False).count()
        return context

class PatientDetailView(DetailView):
    model = Patient
    template_name = 'core/patient_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.get_object()
        context['role'] = self.request.session.get('role')
        context['vitals'] = patient.vital_signs.all().order_by('-timestamp')
        context['labs'] = patient.lab_results.all().order_by('-timestamp')
        context['imaging_studies'] = patient.imaging_studies.all().order_by('-timestamp')
        context['consultations'] = patient.consultations.all().order_by('-timestamp')
        context['notifications'] = patient.notifications.filter(is_read=False)
        context['vital_signs_form'] = VitalSignsForm()
        context['lab_results_form'] = LabResultsForm()
        context['imaging_study_form'] = ImagingStudyForm()
        context['consultation_form'] = ConsultationForm()
        return context

class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'core/patient_form.html'
    success_url = reverse_lazy('patient-list')

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('role') != 'technician':
            messages.error(request, 'Only technicians can create new patients.')
            return redirect('patient-list')
        return super().dispatch(request, *args, **kwargs)

def add_vital_signs(request, pk):
    if request.session.get('role') != 'technician':
        messages.error(request, 'Only technicians can add vital signs.')
        return redirect('patient-detail', pk=pk)
    
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = VitalSignsForm(request.POST)
        if form.is_valid():
            vital_signs = form.save(commit=False)
            vital_signs.patient = patient
            vital_signs.save()
            # Check for critical values and create notification
            if vital_signs.is_critical():
                Notification.objects.create(
                    patient=patient,
                    message=f"Critical vital signs detected: BP {vital_signs.systolic_bp}/{vital_signs.diastolic_bp}, HR {vital_signs.heart_rate}, RR {vital_signs.respiratory_rate}, SpO2 {vital_signs.oxygen_saturation}%",
                    severity='critical',
                    notification_type='vitals'
                )
                patient.is_critical = True
                patient.save()
            messages.success(request, 'Vital signs added successfully.')
            return redirect('patient-detail', pk=pk)
    else:
        form = VitalSignsForm()
    return render(request, 'core/vital_signs_form.html', {'form': form, 'patient': patient})

def add_lab_results(request, pk):
    if request.session.get('role') != 'technician':
        messages.error(request, 'Only technicians can add lab results.')
        return redirect('patient-detail', pk=pk)
    
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = LabResultsForm(request.POST)
        if form.is_valid():
            lab_results = form.save(commit=False)
            lab_results.patient = patient
            lab_results.save()
            # Check for critical values and create notification
            if lab_results.is_critical():
                Notification.objects.create(
                    patient=patient,
                    message=f"Critical lab results detected: {lab_results.cbc_status}, {lab_results.bmp_status}, Glucose {lab_results.glucose_level} mg/dL, {lab_results.coagulation_status}",
                    severity='high',
                    notification_type='lab'
                )
                patient.is_critical = True
                patient.save()
            messages.success(request, 'Lab results added successfully.')
            return redirect('patient-detail', pk=pk)
    else:
        form = LabResultsForm()
    return render(request, 'core/lab_results_form.html', {'form': form, 'patient': patient})

def add_imaging_study(request, pk):
    if request.session.get('role') != 'technician':
        messages.error(request, 'Only technicians can add imaging studies.')
        return redirect('patient-detail', pk=pk)
    
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = ImagingStudyForm(request.POST)
        if form.is_valid():
            imaging_study = form.save(commit=False)
            imaging_study.patient = patient
            imaging_study.save()
            # Check for critical findings and create notification
            if imaging_study.is_critical():
                Notification.objects.create(
                    patient=patient,
                    message=f"Critical imaging findings: {imaging_study.findings}",
                    severity='high',
                    notification_type='imaging'
                )
                patient.is_critical = True
                patient.save()
            messages.success(request, 'Imaging study added successfully.')
            return redirect('patient-detail', pk=pk)
    else:
        form = ImagingStudyForm()
    return render(request, 'core/imaging_study_form.html', {'form': form, 'patient': patient})

def add_consultation(request, pk):
    if request.session.get('role') != 'neurologist':
        messages.error(request, 'Only neurologists can add consultations.')
        return redirect('patient-detail', pk=pk)
    
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.patient = patient
            consultation.save()
            # Check for critical NIHSS score and create notification
            if consultation.is_critical():
                Notification.objects.create(
                    patient=patient,
                    message=f"Critical NIHSS score: {consultation.NIHSS_score} - {consultation.diagnosis}",
                    severity='critical',
                    notification_type='consultation'
                )
                patient.is_critical = True
                patient.save()
            messages.success(request, 'Consultation added successfully.')
            return redirect('patient-detail', pk=pk)
    else:
        form = ConsultationForm()
    return render(request, 'core/consultation_form.html', {'form': form, 'patient': patient})

def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('patient-detail', pk=notification.patient.pk)
