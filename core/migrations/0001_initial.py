# Generated by Django 5.2 on 2025-04-20 20:39

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(150)])),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('chief_complaint', models.TextField()),
                ('medical_history', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LabResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cbc_status', models.CharField(max_length=50)),
                ('bmp_status', models.CharField(max_length=50)),
                ('glucose_level', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('coagulation_status', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lab_results', to='core.patient')),
            ],
        ),
        migrations.CreateModel(
            name='ImagingStudy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_type', models.CharField(max_length=50)),
                ('findings', models.TextField()),
                ('image_url', models.URLField(blank=True, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imaging_studies', to='core.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diagnosis', models.CharField(max_length=200)),
                ('treatment_plan', models.TextField()),
                ('neurologist_notes', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('NIHSS_score', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(42)])),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to='core.patient')),
            ],
        ),
        migrations.CreateModel(
            name='VitalSigns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('systolic_bp', models.IntegerField()),
                ('diastolic_bp', models.IntegerField()),
                ('heart_rate', models.IntegerField()),
                ('respiratory_rate', models.IntegerField()),
                ('oxygen_saturation', models.DecimalField(decimal_places=1, max_digits=4)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vital_signs', to='core.patient')),
            ],
        ),
    ]
