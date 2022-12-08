from django.db import models
from django.urls import reverse


class School(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    address = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('stats', args=[str(self.name)])
