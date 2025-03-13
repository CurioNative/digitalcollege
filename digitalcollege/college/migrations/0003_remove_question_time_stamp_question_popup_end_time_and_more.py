# Generated by Django 5.1.7 on 2025-03-13 12:37

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0002_alter_customuser_department_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='time_stamp',
        ),
        migrations.AddField(
            model_name='question',
            name='popup_end_time',
            field=models.DurationField(default=datetime.timedelta(seconds=60), help_text='End time (HH:MM:SS) until which the question can pop up'),
        ),
        migrations.AddField(
            model_name='question',
            name='popup_start_time',
            field=models.DurationField(default=datetime.timedelta(0), help_text='Start time (HH:MM:SS) when the question can pop up'),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(help_text='The MCQ question text'),
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(help_text='Text of the choice option', max_length=255)),
                ('is_correct', models.BooleanField(default=False, help_text='Indicates if this is the correct answer')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='college.question')),
            ],
        ),
    ]
