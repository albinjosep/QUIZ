from django.urls import path
from . import views

urlpatterns = [
    path("start/", views.start_session, name="start_session"),
    path("question/", views.get_random_question, name="get_random_question"),
    path("submit/", views.submit_answer, name="submit_answer"),
    path("results/", views.results, name="results"),
]
