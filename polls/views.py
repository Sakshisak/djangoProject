from django.http import HttpResponse, HttpResponseRedirect
#from django.contrib.auth import login, authenticate
#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
#from django.urls import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm

#To let the user remain logged in after updating password
from django.contrib.auth import update_session_auth_hash 

from .models import Choice, Question
from django.contrib.auth.models import User


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
def register(request):
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/polls')
    else:
        form = UserCreationForm()
        args = {'form': form}
        return render(request, 'polls/reg_form.html',args)

def profile(request):
    args = {'user' : request.user}
    return render(request, 'polls/profile.html', args)

def edit(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance = request.user)

        if form.is_valid():
            form.save()
            return redirect('../../polls/profile')

    else :
        form = UserChangeForm(instance = request.user)
        args = {'form' : form}
        return render(request, 'polls/edit.html', args)

def pw_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data = request.POST, user = request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('../../polls/profile')
        else:
            return redirect('polls/pw_change.html', args)
    
    else :
        form = PasswordChangeForm(user = request.user)
        args = {'form' : form}
        return render(request, 'polls/pw_change.html', args)
