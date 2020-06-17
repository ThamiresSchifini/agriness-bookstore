from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from Livraria.Accounts.views import AccountsViewSet
from Livraria.Books.views import BooksViewSet, book_by_user_id, reserve_by_id_client, return_by_id_client

router = routers.DefaultRouter()
router.register(r'Books', BooksViewSet)
router.register(r'Accounts', AccountsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('client/<int:id_client>/books', book_by_user_id),
    path('books/<int:id_book>/reserve/<int:id_client>', csrf_exempt(reserve_by_id_client)),
    path('books/<int:id_book>/return/<int:id_client>', csrf_exempt(return_by_id_client)),
    path('', include(router.urls)),
]