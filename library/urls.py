from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from library.views import (AuthorViewSet, BookViewSet, BorrowViewSet,
                           GenreViewSet, LoginView, RegisterView,
                           ReviewViewSet)

router = DefaultRouter()
router.register("books", BookViewSet)
router.register("authors", AuthorViewSet)
router.register("genres", GenreViewSet)
router.register("borrow", BorrowViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("token/", LoginView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("", include(router.urls)),
    path(
        "books/<int:book_id>/reviews/",
        ReviewViewSet.as_view({"get": "list", "post": "create"}),
    ),
]
