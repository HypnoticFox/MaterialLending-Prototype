from django.db.models import F
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django_htmx.http import HttpResponseLocation

from polls.models import Choice, Question

def index(request):
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    base_template = "base_partial.html" if request.htmx else "base_complete.html"
    return render(
        request,
        "polls/index.html",
        {
            "base_template": base_template,
            "latest_question_list": latest_question_list
        }
    )

def details(request, question_id):
    try:
        question = Question.objects.filter(pub_date__lte=timezone.now()).get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    error_message = request.session.pop("error_message", None)
    base_template = "base_partial.html" if request.htmx else "base_complete.html"
    return render(
        request,
        "polls/details.html",
        {
            "base_template": base_template,
            "question": question,
            "error_message": error_message,
        }
    )

def results(request, question_id):
    try:
        question = Question.objects.filter(pub_date__lte=timezone.now()).get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    base_template = "base_partial.html" if request.htmx else "base_complete.html"
    return render(
        request,
        "polls/results.html",
        {
            "base_template": base_template,
            "question": question
        }
    )

def vote(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        request.session["error_message"] = "You didn't select a choice."
        return HttpResponseLocation(reverse("polls:details", args=(question_id,)))
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseLocation(reverse("polls:results", args=(question.id,)))