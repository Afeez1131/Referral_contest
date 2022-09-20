from django.core.management.base import BaseCommand
from auth_app.models import Contest, BusinessOwner
from base_app.models import Referral, Guest
import random
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from django.db.utils import IntegrityError

start_date = make_aware(datetime.now())
end_date = start_date + timedelta(days=100)

name_list = ['Blessing', 'Mercy', 'Favour', 'Joy', 'Favour', 'Precious', 'Peace', 'Marvelous', 'Gift', 'Glory']
base_number = '081044033%s' % random.randint(10, 99)
ip_list = ['255.208.149.128', '212.159.46.181', '12.135.15.111', '116.223.47.205', '136.31.63.6', '5.109.190.63',
           '239.147.145.72', '31.28.173.47', '72.5.55.120', '76.168.125.227']

User = get_user_model()
contest_list = []

# ip = 76.168.125.227

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake_owner = User.objects.create(username='demo', phone_number='08102221110',
                                         full_name="Demo User", business_name='Demo Name')
        fake_owner.set_password('password@123')
        fake_owner.save()

        for k in range(1, 5):
            contest = Contest.objects.create(business_owner=fake_owner,
                                             cash_price=random.randrange(1000, 10000, 500),
                                             starting_date=start_date, ending_date=end_date, duration=45)
            contest_list.append(contest)

        for i in range(random.randint(10, 15)):
            try:
                contest = random.choice(contest_list)

                referral = Referral.objects.create(
                    contest=contest,
                    refer_name=name_list[random.randint(1, len(name_list) - 1)],
                    phone_number=base_number)
                contest.referral_count += 1
                contest.save()

            except IntegrityError:
                print('integrity error')
                pass

            for j in range(random.randint(10, 15)):
                # print(referral)
                try:
                    Guest.objects.create(referral=referral, contest=contest,
                                         ip=ip_list[random.randint(1, len(ip_list) - 1)],
                                         guest_name=name_list[random.randint(1, len(name_list) - 1)],
                                         phone_number=base_number)
                    referral.guest_count += 1
                    referral.save()
                except IntegrityError:
                    print('guest integrity error')
                    pass

        print('------------------------')
        print('Done')

# count = random.randint(1, len(name_list))

# for contest in Contest.objects.all():
# ref = Referral.objects.create(business_owner=contest,
#                               refer_name=name_list[random.randint(1, len(name_list)-1)],
#                               phone_number=base_number)
#
# # contest = Contest.objects.get(unique_id='16ccbced')
# # ref = Referral.objects.get(ref_shortcode='Gnrd')
#
# Guest.objects.create(referral=ref, business_owner=contest,
#                      guest_name=name_list[random.randint(1, len(name_list)-1)], phone_number=base_number, ip=ip_list[random.randint(1, len(ip_list)-1)])
