# ---> automatically creating vote
import random

from base_app.models import Guest, Referral
i = 0
while i < 20:
    for ref in c.referral_contest.all():  # busines_owner contest queryset
        g = Guest.objects.create(referral=ref, business_owner=ref.business_owner, ip='78.179.210.232', guest_name='afeez-%s' % random.randint(1, 100))
        g.phone_number = phone_number='081%s000202%s' % (random.randint(1, 9), random.randint(1,5))
        g.save()
    i += 1


i = 0
while i < 10:
    for contest in c.referral_contest.all():  # busines_owner contest queryset
        Referral.objects.create(business_owner=contest.business_owner, refer_name='afeez-%s' % random.randint(1, 100), phone_number='081%s000202%s' % (random.randint(1, 10), random.randint(1,5)))
    i += 1
