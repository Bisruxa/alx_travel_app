from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from listings.models import Booking, Listing, Review
from listings.serializers import UserSerializer, BookingSerializer, ListingSerializer, UserRegisterSerializer

from listings.permissions import IsAdminOrAnonymous, IsAdminOrUserOwner

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user accounts.
    Only authenticated users can access this endpoint.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAdminOrAnonymous]
        if self.action in ['update','partial_update', 'destroy']:
            self.permission_classes = [IsAdminOrUserOwner]
        return super().get_permissions()
    
    def get_serializer_class(self): # type: ignore
        if self.action == 'create':
            return UserRegisterSerializer
        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class BookingViewSet(viewsets.ModelViewSet):
    """
    Handles confirmed bookings.
    Authenticated users can create; others can read.
    """
    queryset = Booking.objects.filter(status=Booking.BookingStatus.CONFIRMED)
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Automatically set the booking's customer to the logged-in user.
        """
        serializer.save(customer=self.request.user)

    def get_queryset(self): # type: ignore
        if self.request.user.is_authenticated:
            return Booking.objects.filter(customer=self.request.user)
        return super().get_queryset()


class ListingViewSet(viewsets.ModelViewSet):
    """
    Manages listings. Anyone can read; only authenticated users can create/edit.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]