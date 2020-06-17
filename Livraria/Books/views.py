from datetime import datetime

from django.http import HttpResponseNotFound, HttpResponseBadRequest, JsonResponse
from rest_framework import viewsets

from Livraria.Accounts.models import User
from Livraria.Books.models import Book, TAX_LT_3_DAYS, TAX_GT_3_DAYS, TAX_GT_5_DAYS
from Livraria.Books.serializers import BookSerializer
from Livraria.Books.utils import allowed_method

class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@allowed_method('GET')
def book_by_user_id(request, id_client=0):
    """ Function to show borrowed books by user
    :param request: http method
    :param id_client: the user id
    :return: book borrowed by user
    """
    if id_client <= 0:
        return HttpResponseBadRequest('Id must be positive')
    if not User.objects.filter(id=id_client).exists():
        return HttpResponseNotFound('User not found')
    user_instance = User.objects.get(id=id_client)

    book_list = []
    for b in Book.objects.filter(user=user_instance):
        book_dict = BookSerializer(b).data
        book_dict['tax [%]'] = tax_by_book(b.pickup_date)
        book_dict['day_location'] = b.pickup_date

        book_list.append(book_dict)

    return JsonResponse(book_list, safe=False)

@allowed_method('PATCH')
def reserve_by_id_client(request, id_book=0, id_client=0):
    """ Function to reserve book by user
    :param request: http method
    :param id_book: the book id
    :param id_client: the user id
    :return: the book reserved
    """
    if id_book <= 0 or id_client <= 0:
        return HttpResponseBadRequest('Id must be positive')
    if not Book.objects.filter(id=id_book).exists():
        return HttpResponseNotFound('Book not found')
    book_instance = Book.objects.get(id=id_book)
    if not book_instance.status == Book.AVAILABLE:
        return HttpResponseBadRequest('Book not available')
    if not User.objects.filter(id=id_client).exists():
        return HttpResponseNotFound('User not found')
    user_instance = User.objects.get(id=id_client)
    book_instance.user = user_instance
    book_instance.status = Book.BORROWED
    book_instance.pickup_date = datetime.now().date()
    book_instance.save()
    serializer = BookSerializer(book_instance)
    return JsonResponse(serializer.data)

@allowed_method('PATCH')
def return_by_id_client(request, id_book=0, id_client=0):
    if id_book <= 0 or id_client <= 0:
        return HttpResponseBadRequest('Id must be positive')
    if not Book.objects.filter(id=id_book).exists():
        return HttpResponseNotFound('Book not found')
    book_instance = Book.objects.get(id=id_book)
    if not book_instance.status == Book.BORROWED:
        return HttpResponseBadRequest
    if not User.objects.filter(id=id_client).exists():
        return HttpResponseNotFound('User not found')
    user_instance = User.objects.get(id=id_client)
    if not book_instance.user == user_instance:
        return HttpResponseBadRequest
    book_instance.status = Book.AVAILABLE
    book_instance.user = None
    book_instance.save()
    serializer = BookSerializer(book_instance)
    return JsonResponse(serializer.data)

def tax_by_book(pickup_book_date):
    """Function to calculate return tax
    :param pickup_book_date: the date the book was taken
    :return: tax value
    """
    date_now_return = datetime.now().date()
    date_delay = date_now_return - pickup_book_date
    delta_days = date_delay.days - 3
    total_tax = 0

    if delta_days <= 0:
        total_tax = 0

    elif delta_days <= 3:
        total_tax = (TAX_LT_3_DAYS+(0.2*delta_days))

    elif delta_days <= 5:
        total_tax = (TAX_GT_3_DAYS+(0.4*delta_days))

    elif delta_days > 5:
        total_tax =(TAX_GT_5_DAYS+(0.6*delta_days))

    return total_tax
