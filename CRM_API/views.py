from django.contrib.auth import authenticate

from CRM_API.models import Customer
from CRM_API.serializers import CustomerSerializer, UserSerializer

from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView


# Returns all the customers (GET) or creates a new customer (POST).
class CustomerList(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        data = CustomerSerializer(customers, many=True).data
        return Response(data)

    def post(self, request):
        name = request.data.get('name')
        surname = request.data.get('surname')
        imgUrl = request.data.get('imgUrl')
        if not imgUrl:
            imgUrl = 'No image yet'
        # user = request.user.pk
        user = 2
        data = {'name': name, 'surname': surname, 'imgUrl': imgUrl, 'created_by': user, 'last_updated_by': user}
        customer_serial = CustomerSerializer(data=data)

        if customer_serial.is_valid():
            customer_serial.save()
            return Response(customer_serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(customer_serial.errors, status=status.HTTP_400_BAD_REQUEST)


# Allows to get (GET), update (PUT) and delete (DELETE) a customer with a given 'id' (pk)
class CustomerDetail(APIView):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        data = CustomerSerializer(customer).data
        return Response(data)

    def put(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        name = request.data.get('name')
        if not name:
            name = customer.name

        surname = request.data.get('surname')
        if not surname:
            surname = customer.surname

        imgUrl = request.data.get('imgUrl')
        if not imgUrl:
            imgUrl = customer.imgUrl

        # user = request.user.pk
        user = 1
        data = {'name': name, 'surname': surname, 'imgUrl': imgUrl, 'created_by': customer.created_by_id,
                'last_updated_by': user}
        customer_serial = CustomerSerializer(data=data)

        if customer_serial.is_valid():
            customer_serial.update(customer, customer_serial.data)
            return Response(customer_serial.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(customer_serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        data = {'message': 'The customer has been successfully deleted'}
        return Response(data, status=status.HTTP_202_ACCEPTED)


# User login for authentication
class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer

    # Override global authentication settings
    authentication_classes = ()
    permission_classes = ()
