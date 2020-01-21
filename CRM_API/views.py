from CRM_API.models import Customer
from CRM_API.serializers import CustomerInfoSerializer, CustomerCreationSerializer

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# Returns all the customers (GET) or creates a new customer (POST).
class CustomerList(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        data = CustomerInfoSerializer(customers, many=True).data
        return Response(data)

    def post(self, request):
        name = request.data.get('name')
        surname = request.data.get('surname')
        img_url = request.data.get('img_url')
        user = request.user.pk
        if not img_url:
            data = {'name': name, 'surname': surname, 'created_by': user, 'last_updated_by': user}
        else:
            data = {'name': name, 'surname': surname, 'img_url': img_url, 'created_by': user, 'last_updated_by': user}
        customer_serial = CustomerCreationSerializer(data=data)

        if customer_serial.is_valid():
            customer_serial.save()
            return Response(customer_serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(customer_serial.errors, status=status.HTTP_400_BAD_REQUEST)


# Allows to get (GET), update (PUT) and delete (DELETE) a customer with a given 'id' (pk)
class CustomerDetail(APIView):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        data = CustomerInfoSerializer(customer).data
        return Response(data)

    def put(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        name = request.data.get('name')
        if not name:
            name = customer.name

        surname = request.data.get('surname')
        if not surname:
            surname = customer.surname

        img_url = request.data.get('img_url')
        if not img_url:
            img_url = customer.img_url

        user = request.user.pk
        data = {'name': name, 'surname': surname, 'img_url': img_url,
                'created_by': customer.created_by_id,
                'last_updated_by': user}
        customer_serial = CustomerCreationSerializer(data=data)

        if customer_serial.is_valid():
            customer_serial.update(customer, data)
            customer_info = CustomerInfoSerializer(customer)
            return Response(customer_info.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(customer_serial.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        customer.delete()
        data = {'message': 'The customer has been successfully deleted.'}
        return Response(data, status=status.HTTP_202_ACCEPTED)


