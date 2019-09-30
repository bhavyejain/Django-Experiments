from django.urls import path

from . import views

app_name = 'polls'

## Before using generic views

#urlpatterns = [
#	path('', views.index, name = 'index'),
#	# e.g. /polls/5/
#	path('<int:question_id>/', views.detail, name = 'detail'),	# using <> captures a part of the url and sends it as a keyword argument to the function
#	# e.g. /polls/5/results/
#	path('<int:question_id>/results/', views.results, name = 'results'),
#	# e.g. /polls/5/vote/
#	path('<int:question_id>/vote/', views.vote, name = 'vote'),
#]

## After using generic views for index, detail and results:

urlpatterns = [
	path('', views.IndexView.as_view(), name = 'index'),
	path('<int:pk>/', views.DetailView.as_view(), name = 'detail'),
	path('<int:pk>/results', views.ResultsView.as_view(), name = 'results'),
	path('<int:question_id>/vote/', views.vote, name = 'vote'),
]