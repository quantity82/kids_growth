from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import KidsProfile

class PhysData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    kidsProfile = models.ForeignKey(KidsProfile, on_delete=models.CASCADE)
    weight = models.DecimalField(
                max_digits=6,
                decimal_places=3
             )
    height = models.DecimalField(
                max_digits=5,
                decimal_places=2
             )
    date   = models.DateField(default=timezone.now)

    def __str__(self):
        return self.kidsProfile.name + str(self.date)