from django.db import models
import uuid

class User(models.Model):
    PANEL_CHOICES = [
        (1, 'Healthcare Strategies in Climate-hit Regions'),
        (2, 'Empowering Women in Refugees Health Management'),
        (3, 'Innovation Solutions and Mental Health Support'),
        (4, 'Mental Health Support in Climate-Affected Regions'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    job = models.CharField(max_length=100, default="")  # Change default=None to empty string
    company = models.CharField(max_length=100, null=True, blank=True)  # Allow null and blank for company
    panel = models.PositiveSmallIntegerField(choices=PANEL_CHOICES, verbose_name="Which panel would you like to attend", default=1)  # Set a valid default
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True,)
    

    def __str__(self):
        return f"{self.name} - {dict(self.PANEL_CHOICES).get(self.panel, 'Not selected')}"


class ScannedQRCode(models.Model):
    uid = models.CharField(max_length=255, unique=True)
    status = models.IntegerField(default=1)

    def _str_(self):
        return self.uid

