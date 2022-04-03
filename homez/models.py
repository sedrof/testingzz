from django.db import models
from ckeditor.fields import RichTextField

class Home(models.Model):
    title = models.CharField(max_length=150)
    body = RichTextField()
    date = models.DateField(auto_now=True)


    def __str__(self):
        return self.title


class Home2(models.Model):
    title = models.CharField(max_length=150)
    body = RichTextField()
    date = models.DateField(auto_now=True)


    def __str__(self):
        return self.title

