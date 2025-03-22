from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Snippet
from .serializers import SnippetMSerializer

# Create your views here.
@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet
    """

    if request.method == "GET":
        # get all the snippets
        snippets = Snippet.objects.all()
        # serialize the snippets
        snippet_list = SnippetMSerializer(snippets, many=True)
        # convert the python data type into json datastructure
        snip_json = JsonResponse(snippet_list.data, safe=False)
        return snip_json
    
    if request.method == "POST":
        # parse the data in python datatypes
        data = JSONParser().parse(request)
        # deserialzed the data 
        de_data = SnippetMSerializer(data=data)
        # check if the data is valid
        if de_data.is_valid():
            # save the data if it valid
            de_data.save()
            return JsonResponse(de_data.data, status=201)
        
        # if the data is not valid
        return JsonResponse(de_data.errors, status=400)
    
    return HttpResponse("Invalid VERB", status=500)


@csrf_exempt
def snippet_detail(request, pk):
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
        return JsonResponse(snippet_data.data, status=200)

    if request.method == "PUT":
        # parse the request data into python data types
        parsed_data = JSONParser().parse(request)
        # deserialized the parsed data 
        deserialized_data = SnippetMSerializer(snippet, data=parsed_data)
        # check if the deserialized data is valid 
        if deserialized_data.is_valid():
            deserialized_data.save()
            return JsonResponse(deserialized_data.data, status=200)
        return JsonResponse(deserialized_data.errors, status=400)


    if request.method == "DELETE":
        snippet.delete()
        return HttpResponse(status=204)
    
    return HttpResponse("Invalid VERB", status=500)
