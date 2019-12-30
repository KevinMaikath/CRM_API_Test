import json

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from ..models import Customer
from ..serializers import CustomerInfoSerializer


class CustomersListTest(APITestCase):
    def setUp(self):
        # Create an user for 'created_by' and 'last_updated_by'.
        self.user = User.objects.create(username='user', email='user@user.user', password='passwd')
        self.token = Token.objects.create(user=self.user)

        # initialize the APIClient app
        self.client = APIClient()

        Customer.objects.create(name='TestCust', surname='cust', created_by_id=1, last_updated_by_id=1)
        Customer.objects.create(name='CustTest', surname='tomer', created_by_id=1, last_updated_by_id=1)
        Customer.objects.create(name='Customer', surname='customer', created_by_id=1, last_updated_by_id=1)

        self.valid_customer_params = {
            'name': 'newCustomer',
            'surname': 'newCustomer',
            'created_by_id': 1,
            'last_updated_by_id': 1
        }

    # Try to customers list without authentication.
    def test_get_all_customers_no_authentication(self):
        response = self.client.get(reverse('customer_list'))
        error_data = 'Authentication credentials were not provided.'
        self.assertEqual(response.data.get('detail'), error_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Successfully get customers list.
    def test_get_all_customers(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(reverse('customer_list'))
        customers = Customer.objects.all()
        customers_serial = CustomerInfoSerializer(customers, many=True)
        self.assertEqual(response.data, customers_serial.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Try to post a new customer without authentication.
    def test_add_new_customer_no_authentication(self):
        response = self.client.post(
            reverse('customer_list'),
            self.valid_customer_params,
            content_type='application/json')
        error_data = 'Authentication credentials were not provided.'
        self.assertEqual(response.data.get('detail'), error_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Successfully post a new customer.
    def test_add_new_customer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            reverse('customer_list'),
            data=json.dumps(self.valid_customer_params),
            content_type='application/json')
        customer = Customer.objects.filter(name='newCustomer').first()
        default_img_url = settings.MEDIA_URL + settings.IMAGE_FOLDER + settings.DEFAULT_IMAGE_FILE
        self.assertEqual(response.data.get('id'), customer.id)
        self.assertEqual(response.data.get('name'), customer.name)
        self.assertEqual(response.data.get('surname'), customer.surname)
        self.assertEqual(response.data.get('img_url'), default_img_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Try posting a new user with a missing parameter.
    def test_add_new_customer_missing_param(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        customer_params_no_name = {
            'surname': 'newCustomer',
            'created_by_id': 1,
            'last_updated_by_id': 1
        }
        response = self.client.post(
            reverse('customer_list'),
            data=json.dumps(customer_params_no_name),
            content_type='application/json')
        expected_error_message = 'This field may not be null.'
        self.assertEqual(response.data.get('name')[0], expected_error_message)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
