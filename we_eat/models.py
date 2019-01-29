from django.db import models
import uuid
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
    avg_rating = models.FloatField(null=True, blank=True, default=None)
    list_filter = ['name', 'ten_bis']

    # def average_rating(self):
    #     all_ratings = list(map(lambda x: x.rating, self.review_set.all()))
    #     return np.mean(all_ratings)

    def cuisine_img(self):
        if self.cuisine == "Burgerim":
            return ["A", "orange"]
        if self.cuisine == "Sushi":
            return ["I", "green"]
        if self.cuisine == "Pizza":
            return ["L", "coral"]
        if self.cuisine == "Fish":
            return ["K", "yellowgreen"]
        else:
            return ["4", "darkred"]

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