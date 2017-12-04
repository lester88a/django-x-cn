from django.conf.urls import url
from basic_app import views

#app_name = 'schools'

urlpatterns = [

    url(r'^$',views.MovieListView.as_view(),name='movies'),
    url(r'^create/$',views.MovieCreateView.as_view(),name='create'),
    url(r'^(?P<pk>[-\w]+)/$',views.MovieDetailView.as_view(),name='detail'),
    url(r'^update/(?P<pk>[-\w]+)/$',views.MovieUpdateView.as_view(),name='update'),
    url(r'^delete/(?P<pk>[-\w]+)/$',views.MovieDeleteView.as_view(),name='delete'),
]
