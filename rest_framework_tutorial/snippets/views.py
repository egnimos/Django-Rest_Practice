from rest_framework.decorators import api_view 
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Snippet
from .serializers import SnippetMSerializer

# Create your views here.

# Allowed Http Methods for this view function
@api_view(["GET", "POST"])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet
    """

    if request.method == "GET":
        # get all the snippets
        snippets = Snippet.objects.all()
        # serialize the snippets
        snippet_list = SnippetMSerializer(snippets, many=True)
        # convert the python data type into json datastructure
        # using the Response class of rest framework
        snip_json = Response(snippet_list.data)
        return snip_json
    
    if request.method == "POST":
        # parse the data in python datatypes
        # data = JSONParser().parse(request.data)
        # deserialzed the data
        # as parsing already performed by api_view decorator so we don't need to parse the request data
        de_data = SnippetMSerializer(data=request.data)
        # check if the data is valid
        if de_data.is_valid():
            # save the data if it valid
            de_data.save()
            return Response(de_data.data, status=status.HTTP_201_CREATED)
        
        # if the data is not valid
        return Response(de_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # return Response("Invalid VERB", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET", "PATCH", "PUT", "DELETE"])
def snippet_detail(request: Request, pk, format=None):
    """
    Fetch the Snipppet Detail or Update a Snippet Detail, Delete Snippet
    """
    try:
        # get the snippet instace based on the primary key
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse("Snippet doesn't exists", status=404)
    
    if request.method == "GET":
        # serialize the data recieved from the database through model
        snippet_data = SnippetMSerializer(snippet)
        # convert the serialize data into json data
        return Response(snippet_data.data, status=status.HTTP_200_OK)

    if request.method == "PATCH" or request.method == "PUT":
        # parse the request data into python data types
        # parsed_data = JSONParser().parse()
        # deserialized the request data as the rest framework process it into dictionary
        # so we don't need json parse object
        deserialized_data = SnippetMSerializer(
            snippet, data=request.data, 
            partial=request.method == "PATCH"
        )
        # check if the deserialized data is valid 
        if deserialized_data.is_valid():
            deserialized_data.save()
            return Response(deserialized_data.data, status=status.HTTP_200_OK)
        
        # if the deserialized data is invalid then throw response error
        return Response(deserialized_data.errors, status=status.HTTP_400_BAD_REQUEST)


    if request.method == "DELETE":
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # return Response("Invalid VERB", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
