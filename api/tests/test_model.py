from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from auth_app.models import Contest
from base_app.models import Referral, Guest
from Individual.utils import get_ip_address

User = get_user_model()


def sample_business_owner(phone_number='08035281010', business_name="Temp Name", username="temp_user",
                          full_name="Temp User", password='password'):
    user = User.objects.create(phone_number=phone_number, business_name=business_name, username=username,
                               full_name=full_name)
    user.set_password(password)
    user.save()
    return user


# User = sample_business_owner(username='test_user', password='password')
start_date = make_aware(datetime.now())
end_date = start_date + timedelta(days=1)


def sample_contest(business_owner="", cash_price='15000', starting_date=start_date, ending_date=end_date,
                   duration='50'):
    contest = Contest.objects.create(business_owner=business_owner, cash_price=cash_price, starting_date=starting_date,
                                     ending_date=ending_date, duration=duration)
    return contest


def sample_referral(business_owner="", refer_name="Dummy Name", phone_number="08182284493"):
    referral = Referral.objects.create(business_owner=business_owner, refer_name=refer_name, phone_number=phone_number)
    return referral


def sample_guest(referral="", business_owner="", ip='141.189.121.180', guest_name="Test Guest Name",
                 phone_number="08105506074"):
    guest = Guest.objects.create(referral=referral, business_owner=business_owner, ip=ip, guest_name=guest_name,
                                 phone_number=phone_number)
    return guest


def get_url(view_name, arg):
    return reverse(view_name, args=[arg])


TOKEN_OBTAIN_URL = reverse("api_token_auth")
CUSTOM_TOKEN_OBTAIN_URL = reverse("obtain_token")
USERS_URL = reverse("users")
GET_USER_URL = "retrieve-user"
CREATE_BUSINESS_OWNER = reverse('create_user')
CREATE_CONTEST = reverse('create_contest')
CREATE_REFERRAL = reverse('create_referral')
CREATE_GUEST = reverse('create_guest')


class EndpointTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_business_owner_created_success(self):
        user = sample_business_owner(username='username1', password="testpass")
        self.assertTrue(user.check_password('testpass'))
        self.assertEqual(user.username, 'username1')

    def test_obtain_token_fail_with_get(self):
        user = sample_business_owner()
        Token.objects.get_or_create(user=user)
        data = {'username': user.username, 'password': user.password}
        response = self.client.get(TOKEN_OBTAIN_URL)
        # response = self.client.get(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_obtain_token_fail_without_data(self):
        user = sample_business_owner()
        Token.objects.get_or_create(user=user)
        response = self.client.post(TOKEN_OBTAIN_URL)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtain_token_success(self):
        user = sample_business_owner(username='afeez1131', phone_number='08105506074', password='password')
        # user.set_password('password')
        # user.save()
        # test_user = User.objects.get(username=user.username)
        Token.objects.get_or_create(user=user)

        data = {'username': 'afeez1131', 'password': 'password'}
        response = self.client.post(TOKEN_OBTAIN_URL, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())

    def test_custom_obtain_token_fail_get(self):
        response = self.client.get(CUSTOM_TOKEN_OBTAIN_URL)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_custom_obtain_token_fail_with_bad_data(self):
        user = sample_business_owner(username='user1', password='password')
        data = {'username': user.username, 'password': ""}
        response = self.client.post(CUSTOM_TOKEN_OBTAIN_URL, data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_custom_obtain_success_with_valid_data(self):
        user = sample_business_owner(username='afeez', password='password')
        data = {'username': user.username, 'password': 'password'}
        response = self.client.post(CUSTOM_TOKEN_OBTAIN_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIEndpointsPublicTest(TestCase):
    """All the functions underneath are simulating an unauthorized user"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_public_list_business_owners_fail(self):
        """testing without authentication listing business owner to fail"""
        response = self.client.get(USERS_URL)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_retrieve_user_fail(self):
        """test getting a user with pk to fail"""
        user = sample_business_owner()
        url = get_url(GET_USER_URL, user.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_retrieve_contest_fail(self):
        user = sample_business_owner(phone_number='0812233034')
        contest = sample_contest(business_owner=user)
        url = get_url('contest', contest.unique_id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_retrieve_referral_fail(self):
        """test getting a referral"""
        user = sample_business_owner(phone_number='0812233034')
        contest = sample_contest(business_owner=user)
        referral = sample_referral(business_owner=contest)

        url = get_url('referral', referral.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_retrieve_guest_fail(self):
        user = sample_business_owner(phone_number='0812233034')
        contest = sample_contest(business_owner=user)
        referral = sample_referral(business_owner=contest)
        guest = sample_guest(referral=referral, business_owner=contest)

        url = get_url('guest', guest.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_public_create_business_owner_pass(self):
        """business owner """
        data = {
            'username': 'ade1131',
            'business_name': "Milk and Honey",
            'phone_number': '08022849495',
            'full_name': "Omotosho Lawal AFeez",
        }
        response = self.client.post(CREATE_BUSINESS_OWNER, data=data)
        exist = User.objects.filter(username=data['username'], phone_number=data['phone_number'])
        user = User.objects.get(username=data['username'], phone_number=data['phone_number'])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.shortcode, response.data['shortcode'])
        self.assertTrue(exist)


class APIEndpointsPrivate(TestCase):
    """All the functions below are simulating an authorized user"""

    def setUp(self) -> None:
        self.client = APIClient()

        self.user = sample_business_owner(username='test_user', full_name="Set UP", password='password')
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.force_authenticate(self.user, token=token)

    def test_private_list_business_owners_pass(self):
        """testing with authentication listing business owner to pass"""
        test_user = User.objects.all()
        response = self.client.get(USERS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_private_retrieve_user_pass(self):
        url = get_url('retrieve-user', self.user.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('url', response.data)
        self.assertIn('business_name', response.data)

    def test_private_retrieve_contest_pass(self):
        contest = sample_contest(business_owner=self.user)
        exist = Contest.objects.filter(business_owner=contest.business_owner)
        url = get_url('contest', contest.unique_id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("unique_id", response.data[0])
        self.assertIn("cash_price", response.data[0])
        self.assertIn("starting_date", response.data[0])
        self.assertTrue(exist)

    def test_private_retrieve_referral_pass(self):
        contest = sample_contest(business_owner=self.user)
        exist_contest = Contest.objects.filter(business_owner=contest.business_owner)
        referral = sample_referral(business_owner=contest)
        referral_exist = Referral.objects.filter(business_owner=referral.business_owner)

        url = get_url('referral', referral.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(exist_contest)
        self.assertTrue(referral_exist)
        self.assertIn("shortcode", response.data[0])
        self.assertIn("phone_number", response.data[0])
        self.assertIn("guest_count", response.data[0])

    def test_private_retrieve_guest_pass(self):
        contest = sample_contest(business_owner=self.user)
        exist_contest = Contest.objects.filter(business_owner=contest.business_owner)
        referral = sample_referral(business_owner=contest)
        referral_exist = Referral.objects.filter(business_owner=referral.business_owner)
        guest = sample_guest(referral=referral, business_owner=contest)
        guest_exist = Guest.objects.filter(referral=guest.referral)

        url = get_url('referral', referral.id)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(exist_contest)
        self.assertTrue(referral_exist)
        self.assertTrue(guest_exist)
        self.assertIn("shortcode", response.data[0])
        self.assertIn("business_owner", response.data[0])
        self.assertIn("guest_count", response.data[0])

    def test_private_create_contest_pass(self):
        user = sample_business_owner(phone_number='08135281010', business_name="New Business Name",
                                     full_name="New Name 22")
        data = {"business_owner": user.id,
                "cash_price": "25000",
                "starting_date": start_date,
                "ending_date": end_date}

        response = self.client.post(CREATE_CONTEST, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_private_create_referral_pass(self):
        business_owner = sample_business_owner(full_name="New Name", business_name="Omo Ologi",
                                               username='test_business', phone_number='08102202033')
        contest = sample_contest(business_owner=business_owner)
        data = {
            "refer_name": "Test Referral",
            "business_owner": contest.unique_id,
            "phone_number": business_owner.phone_number,
        }

        response = self.client.post(CREATE_REFERRAL, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("business_owner", response.data)
        self.assertIn("shortcode", response.data)

    def test_create_guest(self):
        contest = sample_contest(business_owner=self.user)
        referral = sample_referral(business_owner=contest)

        data = {
            'referral': referral.id,
            'ip': '127.0.0.1',
            'guest_name': 'Guest Name test',
            'phone_number': self.user.phone_number
        }
        response = self.client.post(CREATE_GUEST, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['ip'], '127.0.0.1')
        self.assertIn("referral", response.data)