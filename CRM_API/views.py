from CRM_API.models import Customer
from CRM_API.serializers import CustomerSerializer

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView


# Returns all the customers.
class CustomerList(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


# Allows to get (GET), create (POST), update (PUT) and delete (DELETE) a customer with a given 'id' (pk)
class CustomerDetail(APIView):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        data = CustomerSerializer(customer).data
        return Response(data)
