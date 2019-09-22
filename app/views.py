from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse
from django.views import View
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import generics
from app import models
import pandas as pd
import requests
import re


# Create your views here.
class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CodeReference
        fields = ['status_code', 'status_description']

class OrderCustomerSerializer(serializers.ModelSerializer):
    #status = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Customer
        fields = ['task_id', 'customer_code', 'customer_first_name', 'customer_last_name', 'delivery_address', 'status_code']#, 'status']


class ViewOders(generics.ListAPIView):
	serializer_class = OrderCustomerSerializer
	queryset = models.Customer.objects.all()
		
class StatusCode(APIView):
    def get(self, *arg, **kwargs):
        response = requests.get('http://197.97.154.196/live/logic/courier_demo')
        p = re.compile(r'<.*?>')
        update_codes = [[x.lstrip().split('\n')[0], int(x.lstrip().split('\n')[1].lstrip())] 
        for x in p.sub('', response.text).split('\n    \n') 
        if x not in ('\n', '')]

        for customer in update_codes:
            model = models.Customer.objects.get(customer_code=customer[0])
            # try:
            model.status_code_id = customer[1]
            model.save()
            # except:
            #     print('Skipped')

        return Response({'message': 'Orders Status updated Successfully'})

class Customers(APIView):

	def get(self, request, *arg, **kwargs):
		customers = pd.read_csv('http://197.97.154.196/live/logic/CustomerImport.csv', sep=';', header=None)
		customers.columns = ['customer_code', 'customer_first_name', 'customer_last_name', 'delivery_address']
		for index, row in customers.iterrows():
			model = models.Customer()
			model.customer_code = row['customer_code']
			model.customer_first_name = row['customer_first_name']
			model.customer_last_name = row['customer_last_name']
			model.delivery_address = row['delivery_address']
			model.save()

		return Response({'message': 'Orders are logged Successfully'})