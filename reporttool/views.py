from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
from .models import sql_statement, custom_parameter
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table
import csv
import MySQLdb
import pymssql
import json


def home(request):
    c = {}
    c.update(csrf(request))

    request.session['param_requierd'] = "no"
    request.session['report_name'] = ""
    request.session['valid_form'] = "yes"
    request.session['valid_report'] = "yes"
    sql_statements = []

    for item in sql_statement.objects.all():
        sql_statements.append(item.query_name)

    c['sql_statements'] = sql_statements
    return render_to_response('index.html', c)


def get_params(request):
    if 'report_name' not in request.POST:
        report_name = request.session.get('report_name')
    else:
        request.session['param_requierd'] = "no"
        request.session['valid_report'] = "yes"
        request.session['valid_form'] = "yes"
        report_name = request.POST.get('report_name')

    if request.session.get('valid_form') == "no" and 'report_name' in request.POST:
        request.session['valid_form'] = "yes"
    report_details = sql_statement.objects.get(query_name=report_name)
    all_parameters = custom_parameter.objects.all()
    request.session['sql_query'] = report_details.sql_statement
    request.session['report_name'] = report_name

    c = {}
    c.update(csrf(request))
    sql_statements = []

    for item in sql_statement.objects.all():
        sql_statements.append(item.query_name)

    c['sql_statements'] = sql_statements

    params = []
    i = 0
    for obj in all_parameters:
        result = report_details.sql_statement.find(obj.parameter_name)
        if result != -1:

            params.append(obj)
            request.session['param_requierd'] = "yes"
            request.session['param' + str(i)] = obj.parameter_name
            i += 1

    request.session['param_count'] = str(i)
    c['params'] = params
    if i > 0 or request.session['valid_report'] == "no":
        return render_to_response('index.html', c, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse("report:load_report", kwargs={'report_name': request.session.get('report_name')}))


def load_report(request, report_name):
    report_name = request.session.get('report_name')
    param_count = int(request.session.get('param_count'))

    db_details = sql_statement.objects.get(query_name=report_name)

    formdata = []
    i = 0
    while i < param_count:
        if request.POST.get(request.session.get("param" + str(i))) == "":
            request.session['valid_report'] = "yes"
            request.session['valid_form'] = "no"
            request.session[
                'error_message'] = "Sorry, You can't leave any field blank"
            return HttpResponseRedirect(reverse("report:get_params"))
        else:
            formdata.append(request.POST.get(
                request.session.get("param" + str(i))))
            i += 1

    i = 0
    raw_query = request.session.get('sql_query')
    while i < param_count:
        raw_query = raw_query.replace(
            request.session.get("param" + str(i)), formdata[i])
        i += 1

    request.session['actual_query'] = raw_query
    cursor = object
    try:
        if db_details.database_type == "mysql":
            cursor = get_mysql_response(db_details.database_server, db_details.database_name,
                                        db_details.database_username, db_details.database_password, raw_query)
        else:
            cursor = get_mssql_response(db_details.database_server, db_details.database_name,
                                        db_details.database_username, db_details.database_password, raw_query)
    except:
        request.session['valid_form'] = "yes"
        request.session['valid_report'] = "no"
        request.session[
            'error_message'] = "Running SQL query is throwing exception"
        return HttpResponseRedirect(reverse("report:get_params"))

    # Fetch a single row using fetchone() method.
    results = cursor.fetchall()
    results_title = cursor.description
    # disconnect from server

    c = {}
    c['report_name'] = report_name
    c['raw_query'] = raw_query
    c['results_title'] = results_title
    c['queryresult'] = results
    return render_to_response('report.html', c, context_instance=RequestContext(request))


def pdf_generate(request):
    response = HttpResponse(content_type='application/pdf')
    doc = SimpleDocTemplate(response)
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    raw_query = request.session.get('actual_query')
    cursor = object
    if db_details.database_type == "mysql":
        cursor = get_mysql_response(db_details.database_server, db_details.database_name,
                                    db_details.database_username, db_details.database_password, raw_query)
    else:
        cursor = get_mssql_response(db_details.database_server, db_details.database_name,
                                    db_details.database_username, db_details.database_password, raw_query)
    results = cursor.fetchall()
    title = []
    for item in cursor.description:
        title.append(item[0])
    i = 1
    t_title = Table(title)
    t = Table(results)
    elements = []
    elements.append(t)
    doc.build(elements)
    return response


def csv_generate(request):
    report_name = request.session.get('report_name')
    db_details = sql_statement.objects.get(query_name=report_name)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    raw_query = request.session.get('actual_query')
    cursor = object
    if db_details.database_type == "mysql":
        cursor = get_mysql_response(db_details.database_server, db_details.database_name,
                                    db_details.database_username, db_details.database_password, raw_query)
    else:
        cursor = get_mssql_response(db_details.database_server, db_details.database_name,
                                    db_details.database_username, db_details.database_password, raw_query)
    results = cursor.fetchall()
    title = []
    for item in cursor.description:
        title.append(item[0])
    writer = csv.writer(response)
    writer.writerow(title)
    for r in results:
        writer.writerow(r)
    return response


def get_mysql_response(server, database, username, password, query):
    passd = password.strip(" ")
    db = MySQLdb.connect(server, username, passd, database)
    cursor = db.cursor()
    cursor.execute(query)
    db.close()
    return cursor


def get_mssql_response(server, database, username, password, query):
    passd = password.strip(" ")
    db = pymssql.connect(server, username, passd, database)
    cursor = db.cursor()
    cursor.execute(query)
    db.close
    return cursor
