from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^search/results$', views.SearchResults.as_view(), name="home"),
]
