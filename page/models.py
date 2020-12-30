from django.db import models

class Notification(models.Model):
    title = models.CharField(max_length=30)
    description  = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.title
# Create your models here.
