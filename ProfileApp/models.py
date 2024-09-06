from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from Post.models import District, Subject, ClassIn, Category
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectField

# Create your models here.

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)  # Changed to CharField for flexibility
    nationality = models.CharField(max_length=50)
    religion = models.CharField(max_length=40)
    biodata = models.TextField()
    profession = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    image = models.ImageField(upload_to='media/profile', default='default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class TeacherProfile(models.Model):
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Busy', 'Busy'),
    )

    TEACHING_STYLE_CHOICES = (
        ('Group_Tuition', 'Group Tuition'),
        ('Private_Tuition', 'Private Tuition'),
    )

    TEACHING_PLACE_CHOICES = (
        ('Classroom', 'Classroom'),
        ('Coaching_Center', 'Coaching Center'),
        ('Home_Visit', 'Home Visit'),
        ('My_Place', 'My Place'),
    )

    APPROACH_CHOICES = (
        ('Online_Help', 'Online Help'),
        ('Phone_Help', 'Phone Help'),
        ('Provide_Hand_Notes', 'Provide Hand Notes'),
        ('Video_Tutorials', 'Video Tutorials'),
    )

    MEDIUM_CHOICES = (
        ('Bangla_Medium', 'Bangla Medium'),
        ('English_Medium', 'English Medium'),
        ('Arabic_Medium', 'Arabic Medium'),
        ('Hindi_Medium', 'Hindi Medium'),
        ('Chinese_Medium', 'Chinese Medium'),
        ('Computer_Learning', 'Computer Learning'),
        ('Language_Learning', 'Language Learning'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, related_name='teachers')
    style = MultiSelectField(choices=TEACHING_STYLE_CHOICES, max_choices=3)
    place = MultiSelectField(choices=TEACHING_PLACE_CHOICES, max_choices=3)
    approach = MultiSelectField(choices=APPROACH_CHOICES, max_choices=3)
    medium = MultiSelectField(choices=MEDIUM_CHOICES, max_choices=3)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='cate')
    subject = models.ManyToManyField(Subject, related_name='teachers')
    classin = models.ManyToManyField(ClassIn, related_name='teachers')
    salary = models.IntegerField()
    days_per_week = models.CharField(max_length=50)
    education = models.CharField(max_length=50)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES)  # Corrected field name to "status"
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - Teacher Profile"





            


