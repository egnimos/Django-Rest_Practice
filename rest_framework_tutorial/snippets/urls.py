from .views import snippet_detail, snippet_list
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("snippets/", snippet_list, name="snippet_list"),
    path("snippet/<int:pk>/", snippet_detail, name="snippet_detail")
]

urlpatterns = format_suffix_patterns(urlpatterns)