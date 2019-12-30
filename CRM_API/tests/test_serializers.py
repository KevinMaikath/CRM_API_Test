from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from CRM_API.models import Customer
from CRM_API.serializers import CustomerInfoSerializer, CustomerCreationSerializer, UserSerializer


class CustomerInfoSerializerTest(TestCase):
    def setUp(self):
        # Create an user for 'created_by' and 'last_updated_by'.
        self.user = User.objects.create(username='user', email='user@user.user', password='passwd')
        Customer.objects.create(name='TestCust', surname='cust', created_by_id=1, last_updated_by_id=1)

    # Get a single customer's info.
    def test_get_customer_info(self):
        customer = Customer.objects.first()
        customer_serial = CustomerInfoSerializer(customer)
        default_img_url = settings.MEDIA_URL + settings.IMAGE_FOLDER + settings.DEFAULT_IMAGE_FILE
        expected_data = {
            'id': 1,
            'name': 'TestCust',
            'surname': 'cust',
            'img_url': default_img_url
        }
        self.assertEqual(customer_serial.data, expected_data)


class CustomerCreationSerializerTest(TestCase):
    def setUp(self):
        # Create an user for 'created_by' and 'last_updated_by'.
        self.user = User.objects.create(username='user', email='user@user.user', password='passwd')

        self.valid_data = {
            'name': 'newCustomer',
            'surname': 'newCustomer',
            'created_by': 1,
            'last_updated_by': 1
        }
        self.invalid_data = {
            'name': [1, 2, 3],
            'surname': 'newCustomer',
            'created_by': 1,
            'last_updated_by': 1
        }
        self.missing_param_data = {
            'surname': 'newCustomer',
            'created_by': 1,
            'last_updated_by': 1
        }

    # Successfully create a new customer without image.
    def test_create_new_customer(self):
        customer_serial = CustomerCreationSerializer(data=self.valid_data)
        self.assertTrue(customer_serial.is_valid())
        customer_serial.save()
        default_img_url = settings.MEDIA_URL + settings.IMAGE_FOLDER + settings.DEFAULT_IMAGE_FILE
        expected_data = {
            'id': 1,
            'name': 'newCustomer',
            'surname': 'newCustomer',
            'img_url': default_img_url,
            'created_by': 1,
            'last_updated_by': 1,
        }
        customer = Customer.objects.first()
        self.assertEquals(customer_serial.data, expected_data)
        self.assertEqual(customer.id, expected_data['id'])
        self.assertEqual(customer.name, expected_data['name'])
        self.assertEqual(customer.surname, expected_data['surname'])
        self.assertEqual(customer.img_url.url, expected_data['img_url'])
        self.assertEqual(customer.created_by_id, expected_data['created_by'])
        self.assertEqual(customer.last_updated_by_id, expected_data['last_updated_by'])

    # Try to create a new customer with an invalid parameter.
    def test_create_new_customer_invalid_data(self):
        customer_serial = CustomerCreationSerializer(data=self.invalid_data)
        self.assertFalse(customer_serial.is_valid())

    # Try to create a new customer with a missing required field.
    def test_create_new_customer_missing_field(self):
        customer_serial = CustomerCreationSerializer(data=self.missing_param_data)
        self.assertFalse(customer_serial.is_valid())

    # Successfully update a customer's parameters one by one.
    def test_update_customer_one_by_one(self):
        customer = Customer.objects.create(name='TestCust', surname='cust', created_by_id=1, last_updated_by_id=1)
        customer_serial = CustomerCreationSerializer(customer)

        name_data = {'name': 'newName', 'img_url': customer.img_url}
        customer_serial.update(customer, name_data)
        self.assertEqual(customer.name, name_data['name'])

        surname_data = {'surname': 'newSurname', 'img_url': customer.img_url}
        customer_serial.update(customer, surname_data)
        self.assertEqual(customer.surname, surname_data['surname'])

    # Successfully update a customer's parameters all at once.
    def test_update_customer_all_parameters(self):
        customer = Customer.objects.create(name='TestCust', surname='cust', created_by_id=1, last_updated_by_id=1)
        customer_serial = CustomerCreationSerializer(customer)
        new_data = {'name': 'newName', 'surname': 'newSurname', 'img_url': customer.img_url}
        customer_serial.update(customer, new_data)
        self.assertEqual(customer.name, new_data['name'])
        self.assertEqual(customer.surname, new_data['surname'])


class UserSerializerTest(TestCase):
    def setUp(self):
        pass

    # Successfully creat a new user, providing a hash password and an authentication token.
    def test_user_creation(self):
        data = {
            'username': 'newUser',
            'email': 'user@user.user',
            'password': '1234'
        }
        user_serial = UserSerializer(data=data)
        self.assertTrue(user_serial.is_valid())

        user_serial.save()
        user = User.objects.first()
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.email, data['email'])
        self.assertNotEqual(user.password, data['password'])  # Password must have been saved as a hash value.
        self.assertIsNotNone(user.auth_token)  # Check if the user has an authentication token.
