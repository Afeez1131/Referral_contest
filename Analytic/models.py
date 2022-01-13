from django.db import models
from base_app.models import Referral


# Create your models here.
# class GuestCountManager(models.Manager):
#     def create_guest_count(self, GuestInstance):
#         # Refer instance is imported from the base_app Refer model
#         if isinstance(GuestInstance, Referral):
#             obj, created = self.get_or_create(referral=GuestInstance)
#             obj.count += 1
#             obj.save()
#             return obj.count
#
#
# class GuestCount(models.Model):
#     referral = models.OneToOneField(
#         Referral, on_delete=models.CASCADE, related_name="refer_count"
#     )
#     count = models.IntegerField(default=0)
#
#     objects = GuestCountManager()
#
#     def __str__(self):
#         return str(self.count)
