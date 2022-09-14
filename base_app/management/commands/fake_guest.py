from django.core.management.base import BaseCommand
from auth_app.models import Contest
from base_app.models import Referral, Guest
import random

name_list = ['Blessing', 'Mercy', 'Favour', 'Joy', 'Favour', 'Precious', 'Peace', 'Marvelous', 'Gift', 'Glory']
base_number = '081044033%s' % random.randint(10, 99)
ip_list = ['255.208.149.128', '212.159.46.181', '12.135.15.111', '116.223.47.205', '136.31.63.6', '5.109.190.63', '239.147.145.72', '31.28.173.47', '72.5.55.120', '76.168.125.227', ]
# ip = 76.168.125.227

class Command(BaseCommand):
    def handle(self, *args, **options):
        count = random.randint(1, len(name_list))

        for contest in Contest.objects.all():
            ref = Referral.objects.create(business_owner=contest,
                                          refer_name=name_list[random.randint(1, len(name_list)-1)],
                                          phone_number=base_number)

            # contest = Contest.objects.get(unique_id='16ccbced')
            # ref = Referral.objects.get(ref_shortcode='Gnrd')

            Guest.objects.create(referral=ref, business_owner=contest,
                                 guest_name=name_list[random.randint(1, len(name_list)-1)], phone_number=base_number, ip=ip_list[random.randint(1, len(ip_list)-1)])


        print('------------------------')
        print('Done')
