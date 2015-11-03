# **Magnify**
- Python-Version - python 2.7.9
- App-version : 0.1

## **Project Description**

generating reports from rdbms systems(mysql, mssql, etc) is very common in the field of information technology. Often we will just create custom php scripts to get what we want. Magnify looks at the same problem as a framework. In Magnify you can create reports dynamically by passing data at the time of generating reports.

for eg: Suppose there is table 'testdata' and has muliple columns , one of the column is date_field

Now you usually get data using the query below, where you basically replace the date field everytime you need to generate a report.

```sql
SELECT *FROM `testdata`WHERE (date_field BETWEEN '2010-01-30' AND '2010-09-29')
```

With magnigy you basically make these date values variable, and tell magnify what type of these two values are, You need to tell magnify that FROM_DATE, TO_DATE are variables of type date. hence when you select a query , you are asked for these variables in an html form , in this case it will be a date picker.

```sql
SELECT *FROM `testdata`WHERE (date_field BETWEEN FROM_DATE AND TO_DATE)
```

Once you provide that data , your report is generated , now you can export it as csv, pdf, (in future email support will be added), etc.
## **Reqiurements**
first things first , lets get all the dependencies out of the way

- install freetds (Google up on this , in case you face issues)

    - install on Mac:

      ```
         brew install freetds
      ```

    - install on unix:

      ```
         yum install freetds freetds-devel
      ```

    - install on windows:

      download from following link : [Download FreeTDS](http://sourceforge.net/projects/freetdswindows/).

- python packages required

```python
  pip install django
  pip install mysql-python
  pip install pymssql
  pip install reportlab
  pip install django-grappelli
```

## **Setup**

Create a db in mysql setup name it 'magnify'
```sql
create database magnify
```

open setting.py and update db connection settings of the database in which you created magnify db
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'magnify',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        }
}
```

When done with this you need to run below to generate schema for project
```python
python manage.py schemamigration reporttool
```

Now run syncdb on django app to create actual tables, create an admin account too.
```python
python manage.py syncdb
```

Now try running the app using
```python
python manage.py runserver 0.0.0.0:8000
```
