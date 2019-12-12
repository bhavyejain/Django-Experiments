from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice 
from django.urls import reverse
from django.views import generic
from django.utils import timezone
# from django.template import loader
# from django.http import Http404

# Each view is responsible for doing one of two things: returning an HttpResponse object 
# containing the content for the requested page, or raising an exception such as Http404.


def vote(request, question_id):
	question = get_object_or_404(Question, pk = question_id)
	try:
		selected_choice = question.choice_set.get(pk = request.POST['choice'])	
		# request.POST is a dictionary like object that allows us to access submitted data key-wise. All its values are strings.
		# It gereates a KeyError if choice is not provided.
	except (KeyError, Choice.DoesNotExist):
		# Re-display the question voting form
		return render(request, 'polls/detail.html', {
			'question' : question,
			'error_message' : "You didn't select a choice!",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


############## WITHOUT USING GENERIC VIEWS ###############

# def index(request):
#	  # To test routing:
#	  # return HttpResponse("Hello, world. You're at the polls index.")
#
#	  latest_question_list = Question.objects.order_by('-pub_date')[:5]	# get last 5 published questions
#	  context = {
#		  'latest_question_list' : latest_question_list
#	  }
#
#	  # We can use the following code to return the response and render:
#	  ## template = loader.get_template('polls/index.html')
#	  ## return HttpResponse(template.render(context, request))
#
#	  # Or a shortcut : render()
#	  return render(request, 'polls/index.html', context)
#
# def detail(request, question_id):
#	  # Complete method of raising a 404:
#
#	  ##try:
#	  ##	  question = Question.objects.get(pk = question_id)
#	  ##except Question.DoesNotExist:
#	  ##	  raise Http404("Question does not exist! :(")
#
#	  # Shortcut using get_object_or_404():
#
#	  question = get_object_or_404(Question, pk = question_id)
#	  return render(request, 'polls/detail.html', {'question' : question})
#
# def results(request, question_id):
#	  question = get_object_or_404(Question, pk = question_id)
#	  return render(request, 'polls/results.html', {'question' : question})


############## USING GENERIC VIEWS ###############

# The DetailView generic view expects the primary key value captured from the URL to be called "pk", 
# so we’ve changed question_id to pk for the generic views in urls.py.


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'	# specify explicitly because default generated context variable is question_list

	def get_queryset(self):
		"""Return last 5 published questions (not including future questions)"""
		return Question.objects.filter(
			pub_date__lte = timezone.now() # questions whose pub_date is less than or equal to timezone.now
			).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question 						# by deafult, th context variable generated is question.
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'