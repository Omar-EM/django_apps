from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

#def index(request):
    #latest_question_list = Question.objects.order_by("-publication_date")[:5]   #Get the recent latest 5 questions
    #context = {"latest_question_list": latest_question_list}
    #return render(request, "polls/index.html", context)

#def detail(request, question_id):
#    question = get_object_or_404(Question, id=question_id)
#    return render(request, "polls/detail.html", {"question": question} )

#def results(request, q_id):
#    question = get_object_or_404(Question, pk=q_id)
#    return render(request, "polls/results.html", {"question": question})

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        # __lte for Less Than or Equal
        return Question.objects.filter(publication_date__lte=timezone.now()).order_by("-publication_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        #Redisplay the question voting form
        return render(request,
                      "polls/detail.html",
                      {"question" : question, "error_message": "You Need To select a choice!!"},
                    )
    else:
        selected_choice.votes += 1
        selected_choice.save()      #This might lead to a race condition, see how to resolve it
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))  #Afrer successfully dealing with POST data, always redirect to another page