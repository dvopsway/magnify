from django.contrib import admin
from .models import sql_statement ,custom_parameter

class sql_statement_model(admin.ModelAdmin):
    list_display = ('query_name', 'database_name', 'database_server', 'database_type')
    #form = sql_statement_form

class custom_parameter_model(admin.ModelAdmin):
    list_display = ('parameter_name', 'parameter_label', 'parameter_type')
    list_filter = ['parameter_type']

admin.site.register(sql_statement, sql_statement_model)
admin.site.register(custom_parameter, custom_parameter_model)
