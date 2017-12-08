from django.shortcuts import render
from django.views.generic import (View,TemplateView,
                                    ListView,DetailView,
                                    CreateView, UpdateView,
                                    DeleteView)
from django.core.urlresolvers import reverse_lazy
from . import models
from .forms import UserForm,UserProfileInfoForm

# for login and authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

#user profile
from basic_app.models import UserProfileInfo, Movie, Genre
from django.contrib.auth.models import User

#pagenation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#search
import operator
from django.db.models import Q


# Create your views here.
def index(request):
    #template_name = 'basic_app/index.html'
    movies_rate = Movie.objects.filter(rate__range=(9, 10))[:8]
    #movies_new = Movie.objects.filter(rate__range=(9, 10))[:12]
    movies_usa = Movie.objects.filter(country='美国',rate__range=(7.0, 10))[:8]
    movies_cn = Movie.objects.filter(language='国语',rate__range=(8.0, 10))[:8]
    movies_kr = Movie.objects.filter(country='韩国',rate__range=(8.0, 10))[:8]
    return render(request,'basic_app/index.html',
                    {'movies_rate':movies_rate,
                    #'movies_new':movies_new,
                    'movies_usa':movies_usa,
                    'movies_cn':movies_cn,
                    'movies_kr':movies_kr,
                    })

class MovieListView(ListView):
    #context_object_name = 'movies'
    model = models.Movie
    template_name = 'basic_app/movie_list.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
       context = super(MovieListView, self).get_context_data(**kwargs)
       list_movies = models.Movie.objects.all()
       paginator = Paginator(list_movies, self.paginate_by)

       page = self.request.GET.get('page')

       try:
           movies = paginator.page(page)
       except PageNotAnInteger:
           movies = paginator.page(1)
       except EmptyPage:
           movies = paginator.page(paginator.num_pages)

       context['movies'] = movies
       return context

def genre_list_view(request):
    genre_list = Genre.objects.all()

    paginator = Paginator(genre_list, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        genres = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        genres = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        genres = paginator.page(paginator.num_pages)

    data_dict = {'genres':genres}

    return render(request,'basic_app/genre_list.html',context=data_dict)

class GenreDetailView(DetailView):
    context_object_name = 'genre_detail'
    model = models.Genre
    template_name = 'basic_app/genre_detail.html'
    

class MovieDetailView(DetailView):
    context_object_name = 'movie_detail'
    model = models.Movie
    template_name = 'basic_app/movie_detail.html'


class MovieCreateView(LoginRequiredMixin, CreateView):
    fields = ('title', 'year','date','runtime',
    'country','language','genres',
    'rate','imgurl','downloadurl','desc')
    model = models.Movie
    template_name = 'basic_app/movie_form.html'


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    fields = ('title', 'year','date','runtime',
    'country','language','genres',
    'rate','imgurl','downloadurl','desc')
    model = models.Movie
    template_name = 'basic_app/movie_form.html'


class MovieDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Movie
    success_url = reverse_lazy('movies')
    template_name = 'basic_app/movie_confirm_delete.html'


from functools import reduce

class MovieSearchListView(MovieListView):
    """
    Display a List of movies filtered by the search query.
    """

    paginate_by = 10

    def get_queryset(self):
        result = super(MovieSearchListView, self).get_queryset()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in query_list)) |
                reduce(operator.and_,
                       (Q(country__icontains=q) for q in query_list))
            )

        return result

@login_required(login_url='/login/')
def profile_view(request):
    if request.user.is_authenticated():
        user = request.user
        profile = UserProfileInfo.objects.get(user_id=user.id)
        return render(request,'basic_app/profile.html',{'user':user,'profile':profile})
    else:
        # Do something for anonymous users.
        user=''
        return render(request,'basic_app/profile.html',{'user':user})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Account not active')
        else:
            print('someone tried to login and failed.')
            print('Username: {0} and password {1}'.format(username,password))
            return HttpResponse('invalid login details supplied.')

    return render(request,'basic_app/login.html',{})

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True

            return render(request,'basic_app/login.html',{})

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                            {'user_form':user_form,
                             'profile_form': profile_form,
                             'registered':registered})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
#-----TemplateView-------
# class IndexView(TemplateView):
#     # def get(self,request):
#     #     return HttpResponse('hello word')
#     template_name = 'index.html'
#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         context['inject'] = ' this is injected data'
#         context['inject2'] = ' this is injected data 2'
#         return context
#--------function view----
# def index(request):
#
#     return render(request,'index.html')
