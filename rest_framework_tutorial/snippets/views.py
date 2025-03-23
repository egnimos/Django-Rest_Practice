from rest_framework.decorators import api_view 
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, generics, mixins
from .models import Snippet
from rest_framework.views import APIView
from .serializers import SnippetMSerializer

# Create your views here.

# Let's write some generics with class based views
class GSnippetListView(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetMSerializer

class GSnippetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetMSerializer

# Lets write some mixin and generics with class based views to even reduce the
# code size
class MSnippetListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Snippet.objects.all()
    serializer_class = SnippetMSerializer

    def get(self, request, *args, **kargs):
        return self.list(request=request, *args, **kargs)

    def post(self, request, *args, **kargs):
        return self.create(request=request, *args, **kargs)

class MSnippetDetailView(generics.GenericAPIView, 
                         mixins.RetrieveModelMixin, 
                         mixins.DestroyModelMixin, 
                         mixins.UpdateModelMixin):
    queryset = Snippet.objects.all()
    serializer_class = SnippetMSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request=request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request=request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request=request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request=request, *args, **kwargs)


# LETS write some class based views
class SnippetListView(APIView):
    """
    List all the  snippets or create a new snippets
    """

    def get(self, request, format=None):
        # get the list of snippet instances from database
        snippet_list = Snippet.objects.all()
        # serialize the list of snippet instances into python data types
        serialize_snippet = SnippetMSerializer(snippet_list, many=True)
        # generate response
        return Response(serialize_snippet.data)
    
    def post(self, request, format=None):
        # deserialize the request
        deserialize_data = SnippetMSerializer(data=request.data)
        # check the validitiy of deserialize data
        if deserialize_data.is_valid():
            deserialize_data.save()
        # save the data if it is valid
            return Response(deserialize_data.data, status=status.HTTP_201_CREATED)
        
        # or return error response if it is not valid
        return Response(deserialize_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SnippetDetailView(APIView):
    """
    Fetch, Delete, PUT and PATCH the Snippets data
    """

    def get(self, request, pk, format=None):
        try:
            # get the snippets data from the data base
            snippet_data = Snippet.objects.get(pk=pk) # pk => primary key
            # serialize the data 
            serialize_data = SnippetMSerializer(snippet_data)
            return Response(serialize_data.data)
        
        except Snippet.DoesNotExist:
            return Response("snippet not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f"internal server error {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def _updateSnippet(self, request, pk, partial=False):
        try:
            # get the snippets data from the data base
            snippet_data = Snippet.objects.get(pk=pk) # pk => primary key
            # deserialize the data with request data
            deserialize_data = SnippetMSerializer(snippet_data, data=request.data, partial=partial)
            # check for validity
            if deserialize_data.is_valid():
                deserialize_data.save()
            # save it if it is valid
                return Response(deserialize_data.data)
            
            return Response(deserialize_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Snippet.DoesNotExist:
            return Response("snippet not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f"internal server error {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request, pk, format=None):
        return self._updateSnippet(request=request, pk=pk)


    def patch(self, request, pk, format=None):
        return self._updateSnippet(request=request, pk=pk, partial=True)

    def delete(self, request, pk, format=None):
        try:
            snippet_data = Snippet.objects.get(pk=pk)
            snippet_data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Snippet.DoesNotExist:
            return Response("snippet not found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(f"internal server error {str(e)}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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


