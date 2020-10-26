from django.urls import include, path
from . import views

urlpatterns = [
    path(
        '',
        views.home,
        name='home'
    ),
    path(
        'cars/',
        views.cars,
        name='cars'
    ),
    path(
        'rate/',
        views.rate,
        name='rate'
    ),
    path(
        'popular/',
        views.popular,
        name='popular'
    )

]
