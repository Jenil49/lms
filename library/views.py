from django.core.mail import send_mail
from django.db import transaction
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from utils.email_utils import send_borrow_email
from utils.permissions import IsLibrarian

from .models import Author, Book, BookReview, BorrowRequest, Genre
from .serializers import (AuthorSerializer, BookCreateSerializer,
                          BookSerializer, BorrowSerializer, LoginSerializer,
                          RegisterSerializer, ReviewSerializer)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: LoginSerializer},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.validated_data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related("author").prefetch_related("genres")
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["author", "genres"]
    search_fields = ["title"]
    ordering_fields = ["title", "available_copies"]

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return BookCreateSerializer
        return BookSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [IsAuthenticated(), IsLibrarian()]
        return [IsAuthenticated()]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            return [IsLibrarian()]
        return []


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            return [IsLibrarian()]
        return []


class BorrowThrottle(UserRateThrottle):
    scope = "borrow"


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = BorrowRequest.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [BorrowThrottle]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.role == "LIBRARIAN":
            return BorrowRequest.objects.all()
        return BorrowRequest.objects.filter(user=self.request.user)

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsAuthenticated, IsLibrarian],
    )
    @transaction.atomic
    def approve(self, request, pk=None):
        obj = self.get_object()

        if obj.status != "PENDING":
            return Response({"error": "Request already processed"}, status=400)

        if obj.book.available_copies <= 0:
            return Response({"error": "No copies available"}, status=400)

        obj.status = "APPROVED"
        obj.approved_at = now()

        obj.book.available_copies -= 1
        obj.book.save()
        obj.save()
        send_borrow_email(obj.user, obj.book, "APPROVED")
        return Response({"msg": "Approved"})

    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsAuthenticated, IsLibrarian],
    )
    def reject(self, request, pk=None):
        obj = self.get_object()

        if obj.status != "PENDING":
            return Response({"error": "Request already processed"}, status=400)

        obj.status = "REJECTED"
        obj.save()
        send_borrow_email(obj.user, obj.book, "REJECTED")
        return Response({"msg": "Rejected"})

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    @transaction.atomic
    def return_book(self, request, pk=None):
        obj = self.get_object()

        if obj.status != "APPROVED":
            return Response(
                {"error": "Only approved books can be returned"}, status=400
            )

        obj.status = "RETURNED"
        obj.returned_at = now()

        obj.book.available_copies += 1
        obj.book.save()
        obj.save()

        return Response({"msg": "Returned"})


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BookReview.objects.filter(book_id=self.kwargs["book_id"])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, book_id=self.kwargs["book_id"])
