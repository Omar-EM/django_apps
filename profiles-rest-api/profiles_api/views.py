from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated


from . import serializers
from . import models
from . import permissions


class HelloApiView(APIView):
    """Test API View"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            "Uses HTTP methods as function (get, post, patch, put, delete)",
            "Is similar to a traditional Django View",
            "Gives you the most control over your app logic",
            "Is mapped manually to URLs",
        ]

        return Response({'message': 'Hello!', 'an_apiview': an_apiview})  # Will be converted to json

    def post(self, request):
        """Create a hello msg with our name"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name} !'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):  # pk: ID of the object to be updated
        """Handle updating an object"""
        return Response({'method': 'PUT'})

    def patch(self, request, pk=None):
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})

    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method': 'DELETE'})


# Contrary to the APIView, we add actions (CRUD) to perform on our resources instead of the HTTP methods
class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        """Return a hello msg"""
        a_viewset = [
            "Uses actions (list, create, retrieve, update, partial_update)",
            'Automatically map to URLs using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'message': 'Hello!', 'a_viewset': a_viewset})

    def create(self, request):
        """Create a new hello msg"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handle updating an object by its ID"""
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        """Handle getting part of an object by its ID"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request, pk=None):
        """Handle deleting an object by its ID"""
        return Response({'http_method': 'DELETE'})


# TO BUILD: API URLs:
# /api/profile    --->   list all profiles when HTTP GET method is called; create new profile when HTTP POST is called
# /api/profile/<profile_id>   --->  view specific profile details with HTTP GET; update object using HTTP PUT/PATCH;
# remove it completely using HTTP DELETE
# All of this is done using the following 2 classes

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserPorfileSerializer
    queryset = models.UserProfile.objects.all()
    # This line adds how we authenticate (using auth token)
    authentication_classes = (TokenAuthentication,)
    # this line adds authorizations capablities to our API viewset
    permission_classes = (permissions.UpdateOwnProfile,)    # This is the line that calls the has_object_permission()
    # This 2 lines adds searchfilter capability to our view (user the fields name and email)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens
        So, if we go to /api/login, and enter email+pwd, we'll get the auth token
        This auth token need to be set in the "authorization" header of the HTTP request
        Authorization: Token <token_value>
    """
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# NEXT: We'll build a feed item API
# /api/feed ----> list all feed items; GET (list feed items); POST (create feed item for logged in user)
# /api/feed/<feed_item_id> ---> manage specific feed items; GET (feed items); PUT/PATCH (update); DELETE feed item

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    # Limit the feed to only authenticated users
    permission_classes = (permissions.UpdateOwnStatus, IsAuthenticated)

    def perform_create(self, serializer):       # Gets called each time we do an HTTP POST to our viewset
        """Sets the user profile to the logged-in user"""
        serializer.save(user_profile=self.request.user)     # If the user is authenticated, it self.req.user returns that user



