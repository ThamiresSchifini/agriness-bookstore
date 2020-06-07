from datetime import datetime, timedelta
from Livraria.Books.models import book, TAX_LT_3_DAYS, TAX_GT_3_DAYS, TAX_GT_5_DAYS
from Livraria.Accounts.models import User
from Livraria.Books.serializers import BookSerializer
from rest_framework import viewsets
from django.http import HttpResponseNotFound, JsonResponse


# Create your views here.

class BooksViewSet(viewsets.ModelViewSet):                  # modelviewset = todos métodos http
    queryset = book.objects.all()
    serializer_class = BookSerializer

def book_by_user_id(request, id_client=0):
    if id_client < 0:
        return HttpResponseNotFound()
    if not User.objects.filter(id=id_client).exists():
        return HttpResponseNotFound()
    user_instance = User.objects.get(id=id_client)

    book_list = []
    for b in book.objects.filter(user=user_instance):
        book_dict = BookSerializer(b).data
        book_dict['tax [%]'] = tax_by_book(b.dia_locacao)
        book_dict['day_location'] = b.dia_locacao

        book_list.append(book_dict)

    return JsonResponse(book_list, safe=False)

def reserve_by_id_client(request, id_book=0, id_client=0):
    if id_book < 0:
        return HttpResponseNotFound()
    if not book.objects.filter(id=id_book).exists():
        return HttpResponseNotFound('livro n existe')
    book_instance = book.objects.get(id=id_book)
    if not book_instance.status == book.AVAILABLE:
        return HttpResponseNotFound('livro n disponivel')
    if not User.objects.filter(id=id_client).exists():
        return HttpResponseNotFound('usuario n existe')
    user_instance = User.objects.get(id=id_client)
    book_instance.user = user_instance
    book_instance.status = book.BORROWED
    book_instance.dia_locacao = datetime.now().date()
    book_instance.save()
    serializer = BookSerializer(book_instance)
    return JsonResponse(serializer.data)

def tax_by_book(data_locacao_book):
    date_now = datetime.now().date()
    date_atraso = date_now - data_locacao_book
    delta_days = date_atraso.days - 3

    if delta_days <= 0:
        total_tax = 0

    elif delta_days <= 3:
        total_tax = (TAX_LT_3_DAYS+(0.2*delta_days))

    elif delta_days <= 5:
        total_tax = (TAX_GT_3_DAYS+(0.4*delta_days))

    elif delta_days > 5:
        total_tax =(TAX_GT_5_DAYS+(0.6*delta_days))

    return total_tax


#def books(request):
 #   if request.method == 'GET':
  #      the_books = book.objects.first()
   #     serializer = BookSerializer(the_books)
    #    return JsonResponse(serializer.data)
    #return HttpResponse(JSONResponse)
