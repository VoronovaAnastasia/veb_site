from django.shortcuts import render, redirect
from .models import Film,Feedback,Genre
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate

from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
# Create your views here.





def get_films_list(request):
    films=Film.objects.order_by('title')
    template = loader.get_template('films/index.html')
    context = {'films': films}
    return HttpResponse(template.render(context, request))

def log_out(request):
    logout(request)
    return redirect(reverse('get_films_list'))



def log_in(request):
    if request.method == 'POST':
        logout(request)
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('get_films_list'))
            else:
                form.add_error('Invalid credentials!')
    else: # GET
        form = LoginForm()
    return render(request, 'films/login.html', {'form': form})



def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            logout(request)

            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_again = form.cleaned_data['password_again']
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'User already exists!')
            elif password != password_again:
                form.add_error('password_again', 'Passwords mismatch!')
            else:
                user = User.objects.create_user(username, email, password)
                #blog = Blog.objects.create(author=user, title=blog_title)
                login(request, user)
                return redirect(reverse('get_films_list'))
    else: # GET
        form = RegistrationForm()
    return render(request, 'films/signup.html', {'form': form})




@login_required(login_url='/films/login')
def film(request, film_id):
    if request.method == 'POST':
        return create_feedback(request, film_id)
    else:
        return render_film(request, film_id)

def render_film(request,film_id,additional_context={}):
    try:
        film = Film.objects.get(id=film_id)
        genres=Film.objects.get(id=film_id).genres.all()


    except Film.DoesNotExist:
        raise Http404('НЕ ЛЕЗЬ')

    template = loader.get_template('films/Film.html')
    context={'film':film,
             'genres': genres,
             'feedbacks':film.feedback_set.order_by('-created_at'),
             **additional_context
             }
    return HttpResponse(template.render(context,request))



def create_feedback(request,film_id):
    try:
        film = Film.objects.get(id=film_id)
    except Film.DoesNotExist:
        raise Http404('НЕ ЛЕЗЬ')
    rating = request.POST['rating']
    text = request.POST['text']
    rating_error = None
    if not rating or rating.isspace():
        rating_error='Please provide non-empty rating!'

    if not (rating == '1' or rating == '2' or rating == '3' or rating == '4' or rating == '5'):
        rating_error='Please provide rating between 1 and 5!'

    text_error = None

    if not text or text.isspace():
        text_error='Please provide non-empty feedback!'

    if text_error or rating_error:
        error_context = {
            'rating_error': rating_error,
            'text_error': text_error,
            'rating': rating,
            'text': text


        }
        return render_film(request, film_id, error_context)

    else:
        user_id = None
        if request.user.is_authenticated:
            user_id = request.user.id
        else:
            user_id = 1
        Feedback(film_id=film.id, rating=rating,  text=text, author=User.objects.get(id=user_id)).save()
        counter=0
        film = Film.objects.get(id=film_id)
        feedbacks=film.feedback_set.all()

        if len(feedbacks)!=0:
            for feed in feedbacks:
                counter=counter +feed.rating
            counter=counter//len(feedbacks)

            film.rating=counter
            film.save()
        else:
            film.rating = 0
            film.save()
        return HttpResponseRedirect(reverse('get_films_by_id', kwargs={'film_id': film_id}))



