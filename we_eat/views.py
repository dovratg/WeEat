from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Review, Restaurant
from .filters import RestaurantFilter
from .forms import ReviewForm
import datetime
from django.db.models import Avg
# from uni_form.helper import FormHelper
from crispy_forms.helper import FormHelper


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list': latest_review_list}
    return render(request, 'we_eat/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'we_eat/review_detail.html', {'review': review})


def restaurant_list(request):
    restaurant_list = Restaurant.objects.all()
    # context = {'restaurant_list': restaurant_list}
    filter = RestaurantFilter(request.GET, queryset=restaurant_list)
    context = {'restaurant_list': restaurant_list, 'filter': filter}
    return render(request, 'we_eat/restaurant_list.html', context)


def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    form = ReviewForm()
    return render(request, 'we_eat/restaurant_detail.html', {'restaurant': restaurant, 'form': form})


def calc_avg_review(restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    avg = list(Review.objects.filter(restaurant_id=restaurant_id).aggregate(Avg('rating')).values())[0]
    restaurant.avg_rating = avg
    restaurant.save()


def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    form = ReviewForm(request.POST)
    print('start valid')
    if form.is_valid():
        print('yes valid')
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = form.cleaned_data['user_name']
        review = Review()
        review.restaurant = restaurant
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        calc_avg_review(restaurant_id)
        return HttpResponseRedirect(reverse('we_eat:restaurant_detail', args=(restaurant.id,)))

    return render(request, 'we_eat/restaurant_detail.html', {'restaurant': restaurant, 'form': form})
