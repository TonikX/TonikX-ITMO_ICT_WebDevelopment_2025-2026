from django.db import models

class Class(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        return self.name
