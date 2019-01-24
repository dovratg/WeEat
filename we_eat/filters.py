import django_filters
from django import forms
from we_eat.models import Restaurant
import numpy as np

cuisine_choices = (
    ("Burgerim", "Burgerim"),
    ("Sushi", "Sushi"),
    ("Pizza", "Pizza"),
    ("Fish", "Fish"),
    ("Other", "Other")
)

RATING_CHOICES = (
    (1, '*'),
    (2, '**'),
    (3, '***')
)


def average_rating(self= Restaurant):
    all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
    return np.mean(all_ratings)

class RestaurantFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Restaurant name'),
    cuisine = django_filters.ChoiceFilter(choices=cuisine_choices, label='Cuisine')
    ten_bis = django_filters.BooleanFilter(label='10 bis')
    maximum_delivery_time = django_filters.NumberFilter(field_name='maximum_delivery_time', lookup_expr='lt', label='Maximum delivery time')




    class Meta:
        model = Restaurant
        fields = ['name', 'cuisine', 'ten_bis', 'maximum_delivery_time']
