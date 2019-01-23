from django.conf.urls import url
from . import views

app_name = 'we_eat'
urlpatterns = [
    # ex: /
    url(r'^$', views.restaurant_list, name='restaurant_list'),
    url(r'^review/(?P<review_id>[0-9]+)/', views.review_detail, name='review_detail'),
    url(r'^review', views.review_list, name='review_list'),
    url(r'^restaurant/(?P<restaurant_id>[0-9]+)/add_review/', views.add_review, name='add_review'),
    url(r'^restaurant/(?P<restaurant_id>[0-9]+)/$', views.restaurant_detail, name='restaurant_detail'),
    url(r'^restaurant', views.restaurant_list, name='restaurant_list'),

]