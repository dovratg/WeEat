from django.db import models
import uuid
import numpy as np
from googlegeocoder import GoogleGeocoder
from geopy.geocoders import Nominatim
from django.core.validators import MaxValueValidator, MinValueValidator


class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    cuisine_choices = (
            ("Burgerim", "Burgerim"),
            ("Sushi", "Sushi"),
            ("Pizza", "Pizza"),
            ("Fish", "Fish"),
            ("Other", "Other")
        )
    cuisine = models.CharField(max_length=20, choices=cuisine_choices, default="Other")
    ten_bis = models.BooleanField(default=False)
    address = models.CharField(max_length=200)
    maximum_delivery_time = models.IntegerField(
        default=60,
        validators=[MaxValueValidator(300), MinValueValidator(1)]
     )
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    list_filter = ['name', 'ten_bis']

    def average_rating(self):
        all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
        return np.mean(all_ratings)

    def lat_lag(self):
        import requests
        api_key = "AIzaSyD3G7raKIv3Uco7ajFUYXon-Lmp4SuR9nM"
        address = self.address
        api_response = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
        api_response_dict = api_response.json()
        return api_response_dict['results'][0]['geometry']['location']['lng'], api_response_dict['results'][0]['geometry']['location']['lng']


    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_CHOICES = (
        (1, '*'),
        (2, '**'),
        (3, '***')
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    pub_date = models.DateTimeField('date published')
    user_name = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)