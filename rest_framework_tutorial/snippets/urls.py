from .views import snippet_detail, snippet_list, GSnippetDetailView, GSnippetListView, SnippetListView, SnippetDetailView, MSnippetListView, MSnippetDetailView
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # path("snippets/", snippet_list, name="snippet_list"),
    # path("snippet/<int:pk>/", snippet_detail, name="snippet_detail")
    path("snippets/", SnippetListView.as_view(), name="snippet_list"),
    path("snippet/<int:pk>/", SnippetDetailView.as_view(), name="snippet_detail"),

    # MIXINs
    path("msnippets/", MSnippetListView.as_view(), name="msnippet_list"),
    path("msnippet/<int:pk>/", MSnippetDetailView.as_view(), name="msnippet_detail"),

    # Generics
    path("gsnippets/", GSnippetListView.as_view(), name="gsnippet_list"),
    path("gsnippet/<int:pk>/", GSnippetDetailView.as_view(), name="gsnippet_detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)