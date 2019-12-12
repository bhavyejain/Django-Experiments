# INITIALIZATION
_______________________________________________________________________________

## 1) Create a project:	(A collection of configuration and apps for a particular website)
```
$ cd <path_to_directory_to_store_code>				// cd into master dev folder
$ django-admin startproject <project_name>
```
-------------------------------------------------------------------------------

## 2) To run the development server:
```sh
$ cd <project_name>									// cd into outer project directory
$ python manage.py runserver
```
For custom port,
```sh
$ python manage.py runserver 8080
```
--------------------------------------------------------------------------------

## 3) Create an app: (An app is a Web application that does something – e.g., a Weblog system, a database of public records or a simple poll app.)

A project can contain multiple apps. An app can be in multiple projects.
```sh
$ python manage.py startapp <app_name>
```


=========================================================================================
# CREATING VIEWS AND MAPPING URLs
_________________________________________________________________________________

## 1) Writing a view:

Open the file <app_name>/views.py
A simple view:

```py
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello World!") 
```
---------------------------------------------------------------------------------

## 2) Map the view to a URL:

In the <app_name> directory, create a `urls.py` file. 
The the file, include the following code:

```py
from django.urls import path

from . import views

app_name = <app_name>
urlpatterns = [
    path('', views.index, name='index'),	# The first argument is what shows up in the address bar at that page. Here we expect nothing. 
    										# The second argument is the view that we want to call and the function when we go to the URL.
    										# The name argument is how we will refer this later on. 
]
```
----------------------------------------------------------------------------------

## 3) Point the root URLconf at the polls.urls module:

In <project_name>/urls.py, 
add an import for `django.urls.include` and insert an `include()` in the urlpatterns list:

```py
from django.contrib import admin
from django.urls import include, path 			# added the include import. The include() function allows referencing other URLconfs.

urlpatterns = [
    path('app_name/', include('app_name.urls')),		# included the app_name.urls file and created a new URL path.
    path('admin/', admin.site.urls),
]
```


=========================================================================================
# DATABASE SETUP
__________________________________________________________________________________

## 1) SQLite Database

Go to <project_name>/settings.py

Scroll down to DATABASES. The default is set for sqlite3.

To change database, the keys in the 'default' should be changed.
ENGINE – Either 'django.db.backends.sqlite3', 'django.db.backends.postgresql', 'django.db.backends.mysql', or 'django.db.backends.oracle'
NAME – The name of the database. If you’re using SQLite, the database will be a file on your computer; in that case, NAME should be the full absolute path, including filename, of that file. The default value, os.path.join(BASE_DIR, 'db.sqlite3'), will store the file in your project directory.

Change the time zone. (Asia/Kolkata)

The migrate command looks at the INSTALLED_APPS setting and creates any necessary database tables according to the database settings in your 
mysite/settings.py file and the database migrations shipped with the app.

```sh
$ python manage.py migrate
```


=========================================================================================
# CREATING MODELS
___________________________________________________________________________________

## 1) Creating a model:

A model is the single, definitive source of truth about your data. 
It contains the essential fields and behaviors of the data you’re storing.

Each model is represented by a class with a subclass `django.db.models.Model`. Each model can have multiple
variables which represent a database field in the model.

Each field is represented by an instance of a Field class – e.g., CharField for character fields.

To create a model, in <app_name>/models.py, write the following code:

```py
import datetime
from django.db import models
from django.utils import timezone

class App_model_1(models.Model):
    text_variable_1 = models.CharField(max_length=200)	# some text variable like question_text, choice_text
    pub_date = models.DateTimeField('date published')	# publication date

    def __str__(self):					# method for self convenience and later representation in django admin
        return self.question_text

    def was_published_recently(self):
		return self.pub_date >=  timezone.now() - datetime.timedelta(days=1)

class App_model_2(models.Model):
	app_model_1 = models.ForeignKey(App_model_1, on_delete = CASCADE)	# link between 2 models. Each App_model_2 related to single App_model_1
	text_variable_2 = models.CharField(max_length=200)
    integer_variable = models.IntegerField(default=0)		# int field like votes

    def __str__(self):
        return self.choice_text
```
------------------------------------------------------------------------------------

## 2) Activating a model:

To include the app in our project, we need to add a reference to its configuration class in the INSTALLED_APPS setting. 
The `App_nameConfig` class is in the `app_name/apps.py` file, so its dotted path is `'app_name.apps.App_nameConfig'`. 
Edit the `project_name/settings.py` file and add that dotted path to the INSTALLED_APPS setting. 

Migrations are how Django stores changes to your models.
By running makemigrations, you’re telling Django that you’ve made some changes to your models and that you’d like the 
changes to be stored as a migration.

Now run:
```sh
$ python manage.py makemigrations app_name
```

Then run the command for migrate:
```sh
$ python manage.py migrate
```


=========================================================================================
# DATABASE API
____________________________________________________________________________________

First initialize the shell
```sh
$ python manage.py shell
```

Then import the model classes and timezone.
```sh
>>> from app_name.models import App_model_1, App_model_2
>>> from django.utils import timezone
```

To create objects of a model class:
```py
>>> q = App_model_1(text_variable_1 = "some string", pub_date = timezone.now())
>>> q.save()		# save the object into database

>>> q.id 			# print id of the object
>>> q.text_variable_1	# view value of the variable text_variable_1
>>> q.pub_date

>>> q.text_variable_1 = "some string 2"		# change value
>>> q.save()

>>> current_year = timezone.now().year

>>> App_model_1.objects.all()	# view all objects of App_model_1
>>> App_model_1.objects.filter(id=1)
>>> App_model_1.objects.filter(text_variable_1__startswith='What')
>>> App_model_1.objects.get(pub_date__year=current_year)

>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()

# Display any objects from the related object set -- none so far.
>>> q.app_model_2_set.all()

# Create objects for realted class.
>>> q.app_model_2_set.create(text_variable_2='Not much', integer_variable=0)
>>> q.app_model_2_set.create(text_variable_2='The sky', integer_variable=0)
>>> c = q.app_model_2_set.create(text_variable_2='Just hacking again', integer_variable=0)

# App_model_2 objects have API access to their related App_model_1 objects.
>>> c.question

# And vice versa
>>> q.app_model_2_set.all()
>>> q.app_model_2_set.count()

>>> App_model_2.objects.filter(app_model_1__pub_date__year=current_year)

# Delete one of the choices. Use delete() for that.
>>> c = q.app_model_2_set.filter(text_variable_2__startswith='Just hacking')
>>> c.delete()
```


=========================================================================================
# DJANGO ADMIN
___________________________________________________________________________________

## 1) Creating Admin User:

Create a user who can login to the admin site:
```sh
$ python manage.py createsuperuser
```
Enter your desired username and press enter.
You will then be prompted for your desired email address:
The final step is to enter your password.

Start the development server and go to "/admin/" on local domain
```sh
$ python manage.py runserver
```
-----------------------------------------------------------------------------------

## 2) Make app modifiable for admin:

We need to tell the admin that `App_model_1` objects have an admin interface.
Open the `<app_name>/admin.py` file, and edit it to look like this:

```py
from django.contrib import admin

from .models import App_model_1

admin.site.register(App_model_1)
```


=========================================================================================
# TEMPLATES
___________________________________________________________________________________

First, create a directory called `templates` in your `app_name` directory. Django will look for templates in there.
Within the templates directory you have just created, create another directory called `app_name`, and within that 
create a file called `<view_name>.html`.
you can refer to this template within Django simply as `app_name/view_name.html`.

Write HTML code in the template for the webpage.
Example:
```HTML
{% if list_variable %}
    <ul>
    {% for question in list_variable %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

Update our <view_name> view in `app_name/views.py` to use the template. Example:

```py
from django.template import loader

# ...

def view_name(request):
    list_variable = App_model_1.objects.order_by('-pub_date')[:5]
    template = loader.get_template('app_name/view_name.html')
    context = {
        'list_variable': list_variable,
    }
    return HttpResponse(template.render(context, request))
```

We can use a shortcut with the `render()` function as follows (then no need to inport HttpResponse and loader):

```py
def index(request):
    list_variable = App_model_1.order_by('-pub_date')[:5]
    context = {'list_variable': list_variable}
    return render(request, 'app_name/view_name.html', context)
```

The render() function takes the request object as its first argument, a template name as its second argument and a 
dictionary as its optional third argument. It returns an HttpResponse object of the given template rendered with the given context.


=========================================================================================
# RAISING 404 ERRORS
___________________________________________________________________________________

In `app_name/views.py`, to the view where we need to add 404, add the code (example):
```py
from django.http import Http404

# ...

def view_name(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")                                # custom 404 message
    return render(request, 'app_name/view_name.html', {'question': question})
```

Or use the shortcut with `get_object_or_404()`:
```py
from django.shortcuts import get_object_or_404, render

# ...

def view_name(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'app_name/view_name.html', {'question' : question})
```

There’s also a `get_list_or_404()` function, which works just as `get_object_or_404()` – except using filter() instead of get(). 
It raises Http404 if the list is empty.


=========================================================================================
# CREATE AND EDIT MORE TEMPLATES
_________________________________________________________________________________________

The code for templates is commented to provide explanation.

### Templates created:
-> index.html

-> detail.html

-> results.html


=========================================================================================
# GENERIC VIEWS
_________________________________________________________________________________________

To convert to generic views:

1) Convert the URLconf.
2) Delete some of the old, unneeded views.
3) Introduce new views based on Django’s generic views.

For the views which will be replaced by generic views, in `<app name>/urls.py`,
modify the paths to the views as:
```py
urlpatterns = [
    path('', views.GenericViewClass1.as_view(), name='view1'),
    path('<int:pk>/', views.GenericViewClass2.as_view(), name='view2'),
    path('<int:pk>/view3/', views.GenericViewClass3.as_view(), name='view3'),
]
```

The `DetailView` generic view expects the name of the primary key to be "pk", hence the earlier change.

Each generic view expects a model to be provided. We can provide querysets if we want the view to work on filtered data.

Using model:
```py
class View_name(generic.DetailView):
    model = App_model_1
    template_name = 'app_name/view_name.html'
```

Using queryset:
```py
class View_name(generic.ListView):
    template_name = 'app_name/view_name.html'
    context_object_name = 'latest_question_list'    # specify explicitly because default generated context variable might not be correct

    def get_queryset(self):
        """Return last 5 published questions"""
        return Question.objects.order_by('-pub_date')[:5]
```
(Ref: https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#django.views.generic.list.ListView)
(Ref: https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-display/)


=========================================================================================
#CREATING TEST FILES
_________________________________________________________________________________________

Edit the tests.py in the app directory to include tests.

Check `polls/tests.py` for examples.

To execute tests:
```sh
$ python manage.py test <app_name>
```

Django provides a test Client to simulate a user interacting with the code at the view level. 
We can use it in tests.py or even in the shell.

```sh
$ python manage.py shell
```

```py
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()
```

Next, import the test client class
```py
>>> from django.test import Client
>>> # create an instance of the client
>>> client = Client()
```

Now use the client to do some work:
```py
>>> # get a response from '/'
>>>  response = client.get('/')
Not Found: /
>>> # we should expect a 404 from that address; if you instead see an
>>> # "Invalid HTTP_HOST header" error and a 400 response, you probably
>>> # omitted the setup_test_environment() call described earlier.
>>> response.status_code
404
>>> # on the other hand we should expect to find something at '/polls/'
>>> # we'll use 'reverse()' rather than a hardcoded URL
>>> from django.urls import reverse
>>> response = client.get(reverse('<app_name>:<url_name>'))
>>> response.status_code
>>> response.content
>>> response.context['latest_question_list']
```

Now modify the test.py to include tests for views.