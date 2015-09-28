from django.db import models

# Create your models here.

class sql_statement(models.Model):
    query_name = models.CharField(max_length=60)
    query_description = models.TextField()
    database_name = models.CharField(max_length=60)
    database_server = models.CharField(max_length=60)
    database_username = models.CharField(max_length=40)
    database_password = models.CharField(max_length=40,null=True)
    database_type = models.CharField(max_length=20)
    sql_statement = models.TextField()

    def __unicode__(self):
        return self.query_name

class custom_parameter(models.Model):
    parameter_name = models.CharField(max_length=50)
    parameter_label = models.CharField(max_length=30 , default='Input')
    parameter_type = models.CharField(max_length=30)
    parameter_format = models.CharField(max_length=30)

    def __unicode__(self):
        return self.parameter_name
