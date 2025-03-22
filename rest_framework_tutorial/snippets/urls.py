from .views import snippet_detail, snippet_list
from django.urls import path

urlpatterns = [
    path("snippets/", snippet_list, name="snippet_list"),
    path("snippet/<int:pk>/", snippet_detail, name="snippet_detail")
]