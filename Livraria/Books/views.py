from Livraria.Books.models import book
from Livraria.Accounts.models import User
from Livraria.Books.serializers import BookSerializer
from rest_framework import viewsets
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse


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
    serializer = BookSerializer(book.objects.filter(user=user_instance), many=True)
    return JsonResponse(serializer.data, safe=False)

def reserve_by_id_client(request, id_book=0, id_client=0):
    if id_book < 0:
        return HttpResponseNotFound()
    if not book.objects.filter(id=id_book).exists():
        return HttpResponseNotFound()
    book_instance = book.objects.get(id=id_book)
    if not book_instance.status == book.AVAILABLE:
        return HttpResponseNotFound('sdf')
    if not User.objects.filter(id=id_client).exists():
        return HttpResponseNotFound()
    user_instance = User.objects.get(id=id_client)
    book_instance.user = user_instance
    book_instance.status = book.BORROWED
    book_instance.save()
    serializer = BookSerializer(book_instance)
    return JsonResponse(serializer.data)


#def books(request):
 #   if request.method == 'GET':
  #      the_books = book.objects.first()
   #     serializer = BookSerializer(the_books)
    #    return JsonResponse(serializer.data)
    #return HttpResponse(JSONResponse)
