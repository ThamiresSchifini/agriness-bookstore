from django.test import TestCase, Client
from datetime import datetime, timedelta
from .models import book
from .views import book_by_user_id, reserve_by_id_client, tax_by_book
from Livraria.Accounts.models import User

NAME_1 = 'book_name_1'
NAME_2 = 'book_name_2'
NAME_3 = 'book_name_3'
AUTHOR = 'some_author'
USER_NAME = 'user'
SCHOOLING_STUDENT = 'student'
DATE_TODAY = datetime.now().date()
URL_RESERVE_BOOK_1_BOOK_1 = '/books/1/reserve/1'

class BookTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        #book.objects.create(name=NAME_1, author=AUTHOR)
        #book.objects.create(name=NAME_2, author=AUTHOR)
        #book.objects.create(name=NAME_3, author=AUTHOR)

    def test_given_2_books_when_get_books_then_expect_2_books(self):
        # Arrange
        book.objects.create(id=1, name='meu livro', author='thamires')
        book.objects.create(id=2, name='meu livro 2', author='patrícia')

        SERIALIZED_BOOK_1 = {'status': 'A', 'name': 'meu livro', 'author': 'thamires'}
        SERIALIZED_BOOK_2 = {'status':'A', 'name':'meu livro 2', 'author':'patrícia'}
        expected_content = [SERIALIZED_BOOK_1, SERIALIZED_BOOK_2]

        # Act
        response = self.client.get('/Books/')

        # Assert
        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(response.content, expected_content)

    def test_given_user_1_when_get_books_by_user_then_assert_books_by_user_user_equal_user_1(self):

        # Arrange
        USER_1 = User.objects.create(id=1, name='João', schooling='Graduate')
        DIA_LOCACAO_NOW = datetime.now().date()
        BOOK_1 = book.objects.create(id=1, name='A Cabana', author='Cristian', user=USER_1, dia_locacao=DIA_LOCACAO_NOW)
        BOOK_2 = book.objects.create(id=2, name='A Cabana', author='Cristian')
        BOOK_1_SERIALIZER = [{'name': 'A Cabana', 'author': 'Cristian',
                             'tax [%]': 0, 'day_location': str(DIA_LOCACAO_NOW), 'status': 'A'}]
        URL_BOOKS_BY_USER = '/client/1/books'

        pass

        # Act
        response = self.client.get(URL_BOOKS_BY_USER)

        # Assert

        self.assertJSONEqual(response.content, BOOK_1_SERIALIZER)

    def test_given_user_1_when_reserve_book_1_then_assert_book_1_user_equal_user_1(self):
        # Arrange
        book.objects.create(id=1, name=NAME_1, author=AUTHOR)
        User.objects.create(id=1, name=USER_NAME, schooling=SCHOOLING_STUDENT)

        # Act
        response = self.client.get(URL_RESERVE_BOOK_1_BOOK_1)

        # Assert
        self.assertEqual(response.status_code, 200)
        book_1 = book.objects.get(name=NAME_1)
        self.assertEqual(book_1.user, User.objects.get(name=USER_NAME))
        self.assertEqual(book_1.status, book.BORROWED)
        self.assertEqual(book_1.dia_locacao, datetime.now().date())

    def test_given_date_when_tax_called_and_past_1_day_then_assert_result(self):
        # Arrange
        atraso = timedelta(days=1)
        date = datetime.now().date() + atraso
        tax = 0

        # Act
        result = tax_by_book(date)

        # Assert
        self.assertEqual(result, tax)