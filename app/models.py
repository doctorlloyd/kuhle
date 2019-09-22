from django.db import models

# Create your models here.

class CodeReference(models.Model):
	status_code = models.IntegerField(primary_key=True, null=False, unique=True)
	status_description = models.CharField(max_length=70, null=True)


class Customer(models.Model):
	task_id = models.AutoField(primary_key=True)
	customer_code = models.CharField(null=False, unique=True, max_length=30)
	customer_first_name = models.CharField(null=False, max_length=30)
	customer_last_name = models.CharField(null=False, max_length=30)
	delivery_address = models.TextField(null=False, max_length=100)
	status_code = models.ForeignKey(CodeReference, default=100, on_delete=models.CASCADE)