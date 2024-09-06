from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.utils.text import slugify
from PIL import Image

# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ClassIn(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class PostModel(models.Model):
    LANGUAGE = (
        ('Bangla', 'Bangla'),
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Arabic', 'Arabic'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    salary = models.IntegerField()
    details = models.TextField()
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True)
    available = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', null=True, )
    language = MultiSelectField(choices=LANGUAGE, default=['Bangla'], max_choices=2)
    subject = models.ManyToManyField(Subject, related_name='posts')
    classin = models.ManyToManyField(ClassIn, related_name='posts')
    created_at = models.DateTimeField(default=now)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    views = models.ManyToManyField(User, related_name='viewed_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_views(self):
        return self.views.count()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(PostModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_subject_list(self):
        return ' , '.join([s.name for s in self.subject.all()])

    def get_classin_list(self):
        return ' , '.join([c.name for c in self.classin.all()])

    def title_proper(self):
        return self.title.title()

    def details_short(self):
        detail_word = self.details.split(' ')
        if len(detail_word) > 3:
            return ' '.join(detail_word[:3]) + '...'
        else:
            return self.details

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    create_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username}: {self.text[:10]}"

class PhotoAddModel(models.Model):
    image = models.ImageField(upload_to='image/')
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='images')

    def save(self, *args, **kwargs):
        super(PhotoAddModel, self).save(*args, **kwargs)
        image = Image.open(self.image.path)
        if image.height > 300 or image.width > 300:
            output = (300, 300)
            image.thumbnail(output)
            image.save(self.image.path)

    def __str__(self):
        return f"Image for {self.post}"
