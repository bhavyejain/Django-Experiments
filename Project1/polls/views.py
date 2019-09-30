from django.shortcuts import get_object_or_404, render

# Create your views here.
from django.http import HttpResponse
from .models import Question 
from django.template import loader
from django.http import Http404

# Each view is responsible for doing one of two things: returning an HttpResponse object 
# containing the content for the requested page, or raising an exception such as Http404.

def index(request):
	# To test routing:
	# return HttpResponse("Hello, world. You're at the polls index.")

	latest_question_list = Question.objects.order_by('-pub_date')[:5]	# get last 5 published questions
	context = {
		'latest_question_list' : latest_question_list
	}

	# We can use the following code to return the response and render:
	## template = loader.get_template('polls/index.html')
	## return HttpResponse(template.render(context, request))

	# Or a shortcut : render()
	return render(request, 'polls/index.html', context)

def detail(request, question_id):
	# Complete method of raising a 404:

	##try:
	##	  question = Question.objects.get(pk = question_id)
	##except Question.DoesNotExist:
	##	  raise Http404("Question does not exist! :(")

	# Shortcut using get_object_or_404():

	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question' : question})

def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)

def vote(request, question_id):
	return HttpResponse("You're voting on question %s." % question_id)