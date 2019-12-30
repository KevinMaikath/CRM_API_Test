import json

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from ..models import Customer
from ..serializers import CustomerInfoSerializer

default_img_url = settings.MEDIA_URL + settings.IMAGE_FOLDER + settings.DEFAULT_IMAGE_FILE


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

    # Try to get customers list without authentication.
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


class CustomerDetailTest(APITestCase):
    def setUp(self):
        # Create an user for 'created_by' and 'last_updated_by'.
        self.user_1 = User.objects.create(username='first_user', email='user@user.user', password='passwd')
        self.token = Token.objects.create(user=self.user_1)

        # initialize the APIClient app
        self.client = APIClient()

        Customer.objects.create(name='TestCust', surname='cust', created_by_id=1, last_updated_by_id=1)
        Customer.objects.create(name='CustTest', surname='tomer', created_by_id=1, last_updated_by_id=1)
        Customer.objects.create(name='Customer', surname='customer', created_by_id=1, last_updated_by_id=1)

    # Successfully get a customer by it's id.
    def test_get_customer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/customer/1')
        customer = Customer.objects.first()
        expected_data = {
            'id': customer.id,
            'name': customer.name,
            'surname': customer.surname,
            'img_url': customer.img_url.url
        }
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Try to get a customer without authentication.
    def test_get_customer_no_authentication(self):
        response = self.client.get('/customer/1')
        error_data = 'Authentication credentials were not provided.'
        self.assertEqual(response.data.get('detail'), error_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Try to get a nonexistent customer.
    def test_get_nonexistent_customer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/customer/10')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Successfully update a customer (without image).
    def test_update_customer_all_params(self):
        user_2 = User.objects.create(username='second', email='user@user.user', password='passwd')
        token_2 = Token.objects.create(user=user_2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_2.key)
        new_data = {'name': 'newName', 'surname': 'newSurname'}
        response = self.client.put(
            '/customer/1',
            data=json.dumps(new_data),
            content_type='application/json')
        expected_data = {
            'id': 1,
            'name': 'newName',
            'surname': 'newSurname',
            'img_url': default_img_url
        }
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        customer = Customer.objects.filter(id=1).first()
        self.assertEqual(customer.name, new_data['name'])
        self.assertEqual(customer.surname, new_data['surname'])
        self.assertEqual(customer.last_updated_by_id, user_2.id)

    # Try to update a customer with an invalid parameter.
    def test_update_customer_invalid_param(self):
        user_2 = User.objects.create(username='second', email='user@user.user', password='passwd')
        token_2 = Token.objects.create(user=user_2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_2.key)
        new_data = {'name': [1, 2, 3]}
        response = self.client.put(
            '/customer/1',
            data=json.dumps(new_data),
            content_type='application/json')
        print(response.data)
        expected_error = 'Not a valid string.'
        self.assertEqual(response.data.get('name')[0], expected_error)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Successfully delete a customer.
    def test_delete_customer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete('/customer/3')
        message = 'The customer has been successfully deleted.'
        self.assertEquals(response.data.get('message'), message)
        self.assertEquals(response.status_code, status.HTTP_202_ACCEPTED)

        customer = Customer.objects.filter(id=3).first()
        self.assertIsNone(customer)

    # Try to get a deleted customer.
    def test_delete_and_get_customer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        delete_response = self.client.delete('/customer/3')
        message = 'The customer has been successfully deleted.'
        self.assertEquals(delete_response.data.get('message'), message)
        self.assertEquals(delete_response.status_code, status.HTTP_202_ACCEPTED)

        get_response = self.client.get('/customer/3')
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)
