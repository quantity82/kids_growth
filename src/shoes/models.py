from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models import KidsProfile

#靴データ
class ShoesData(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    kidsProfile = models.ForeignKey(KidsProfile, on_delete=models.CASCADE,null=True)
    buy_date = models.DateField(default=timezone.now)
    shoes_size = models.DecimalField(
                max_digits=3,
                decimal_places=1,
                choices = ((x/2, str(x/2)) for x in range(16,50,1)),
                blank = False
                )
    shoes_memo = models.TextField(blank=True, null=True)
    shoes_image = models.ImageField(upload_to="image/", blank=True)

    def __str__(self):
        return self.kidsProfile.name + str(self.buy_date)