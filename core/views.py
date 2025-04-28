from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Patient, VitalSigns, LabResults, ImagingStudy, Consultation
from .forms import PatientForm, VitalSignsForm, LabResultsForm, ImagingStudyForm, ConsultationForm

# Create your views here.

class PatientListView(ListView):
    model = Patient
    template_name = 'core/patient_list.html'
    context_object_name = 'patients'
    ordering = ['-created_at']

class PatientDetailView(DetailView):
    model = Patient
    template_name = 'core/patient_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.get_object()
        context['vital_signs'] = patient.vital_signs.order_by('-timestamp').first()
        context['lab_results'] = patient.lab_results.order_by('-timestamp').first()
        context['imaging_studies'] = patient.imaging_studies.order_by('-timestamp').first()
        context['consultations'] = patient.consultations.order_by('-timestamp').first()
        return context

class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'core/patient_form.html'
    success_url = reverse_lazy('patient-list')

def add_vital_signs(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = VitalSignsForm(request.POST)
        if form.is_valid():
            vital_signs = form.save(commit=False)
            vital_signs.patient = patient
            vital_signs.save()
            messages.success(request, 'Vital signs added successfully.')
            return redirect('patient-detail', pk=pk)
    else:
        form = VitalSignsForm()
    return render(request, 'core/vital_signs_form.html', {'form': form, 'patient': patient})

def add_lab_results(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = LabResultsForm(request.POST)
        if form.is_valid():
            lab_results = form.save(commit=False)
            lab_results.patient = patient
            lab_results.save()
            messages.success(request, 'Lab results added successfully.')
            return redirect('patient-detail', pk=pk)
    else:
        form = LabResultsForm()
    return render(request, 'core/lab_results_form.html', {'form': form, 'patient': patient})

def add_imaging_study(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = ImagingStudyForm(request.POST)
        if form.is_valid():
            imaging_study = form.save(commit=False)
            imaging_study.patient = patient
            imaging_study.save()
            messages.success(request, 'Imaging study added successfully.')
            return redirect('patient-detail', pk=pk)
    else:
        form = ImagingStudyForm()
    return render(request, 'core/imaging_study_form.html', {'form': form, 'patient': patient})

def add_consultation(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save(commit=False)
            consultation.patient = patient
            consultation.save()
            messages.success(request, 'Consultation added successfully.')
            return redirect('patient-detail', pk=pk)
    else:
        form = ConsultationForm()
    return render(request, 'core/consultation_form.html', {'form': form, 'patient': patient})
