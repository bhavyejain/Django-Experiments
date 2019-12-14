from django.contrib import admin

# Register your models here.
from .models import Question, Choice

# default form
# admin.site.register(Question)
# admin.site.register(Choice)

"""
class ChoiceInLine(admin.StackedInline):	# stacked display
	model = Choice
	extra = 3
"""

class ChoiceInLine(admin.TabularInline):	# tabular display
	model = Choice
	extra = 3

class QuestionAdmin(admin.ModelAdmin):
	#fields = ['pub_date', 'question_text']	# order of fields
	fieldsets = [
		(None, {'fields': ['question_text']}),
		('Date information', {'fields': ['pub_date']}),
	]
	inlines = [ChoiceInLine]	# tells django Choice objects are edited on the Question admin page.
	list_display = ('question_text', 'pub_date', 'was_published_recently')	# display individual fields while listing questions.
	list_filter = ['pub_date'] # add option to filter questions by publication date
	search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)