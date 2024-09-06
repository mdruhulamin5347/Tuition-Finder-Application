from django.db import models

# Create your models here.
class ContactModel(models.Model):
    name=models.CharField( max_length=50)
    Phone_number=models.IntegerField()
    gmail=models.EmailField( max_length=254)
    text=models.TextField()
    def __str__(self):
        return self.name
