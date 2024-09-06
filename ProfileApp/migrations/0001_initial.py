# Generated by Django 4.2.2 on 2024-08-20 20:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Post', '0003_alter_postmodel_available'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=6)),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=3)),
                ('address', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=15)),
                ('nationality', models.CharField(max_length=50)),
                ('religion', models.CharField(max_length=40)),
                ('biodata', models.TextField()),
                ('image', models.ImageField(upload_to='media/profile')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='Post.category')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeacherProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', multiselectfield.db.fields.MultiSelectField(choices=[('Group_Tuition', 'Group Tuition'), ('Private_Tuition', 'Private Tuition')], max_length=29)),
                ('place', multiselectfield.db.fields.MultiSelectField(choices=[('Classroom', 'Classroom'), ('Coaching_Center', 'Coaching Center'), ('Home_Visit', 'Home Visit'), ('My_Place', 'My Place')], max_length=45)),
                ('approach', multiselectfield.db.fields.MultiSelectField(choices=[('Online_Help', 'Online Help'), ('Phone_Help', 'Phone Help'), ('Provide_Hand_Notes', 'Provide Hand Notes'), ('Video_Tutorials', 'Video Tutorials')], max_length=57)),
                ('medium', multiselectfield.db.fields.MultiSelectField(choices=[('Bangla_Medium', 'Bangla Medium'), ('English_Medium', 'English Medium'), ('Arabic_Medium', 'Arabic Medium'), ('Hindi_Medium', 'Hindi Medium'), ('Chinese_Medium', 'Chinese Medium'), ('Computer_Learning', 'Computer Learning'), ('Language_Learning', 'Language Learning')], max_length=106)),
                ('salary', models.IntegerField()),
                ('days_per_week', models.CharField(max_length=50)),
                ('education', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Busy', 'Busy')], max_length=9)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('classin', models.ManyToManyField(related_name='teachers', to='Post.classin')),
                ('district', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teachers', to='Post.district')),
                ('subject', models.ManyToManyField(related_name='teachers', to='Post.subject')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]