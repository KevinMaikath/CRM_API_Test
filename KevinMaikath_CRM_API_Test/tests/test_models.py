from django.contrib.auth.models import User
from django.test import TestCase
from CRM_API.models import Customer
from django.conf import settings


class UserTest(TestCase):
    def setUp(self):
        User.objects.create(username='user', email='user@user.user', password='password')

    # User creation.
    def test_user_created(self):
        user = User.objects.first()
        self.assertEqual(user.username, 'user')
        self.assertEqual(user.email, 'user@user.user')
        self.assertEqual(user.password, 'password')


class CustomerTest(TestCase):
    def setUp(self):
        # Create an user for 'created_by' and 'last_updated_by'.
        User.objects.create(username='user', email='user@user.user', password='passwd')
        Customer.objects.create(name='TestCust', surname='cust', created_by_id=1, last_updated_by_id=1)

    # Customer creation without image.
    def test_customer_created_default_img(self):
        customer = Customer.objects.first()
        default_img_url = settings.MEDIA_URL + settings.IMAGE_FOLDER + settings.DEFAULT_IMAGE_FILE
        self.assertEqual(customer.name, 'TestCust')
        self.assertEqual(customer.surname, 'cust')
        self.assertEqual(customer.img_url.url, default_img_url)
        self.assertEqual(customer.created_by_id, 1)
        self.assertEqual(customer.last_updated_by_id, 1)
