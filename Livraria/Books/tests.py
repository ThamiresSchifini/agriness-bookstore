from datetime import datetime, timedelta

from django.test import TestCase, Client

from Livraria.Accounts.models import User
from .models import Book
from .views import tax_by_book

BOOK_NAME1 = 'book_name_1'
BOOK_NAME2 = 'book_name_1'
AUTHOR1 = 'some_author_2'
AUTHOR2 = 'some_author_2'
USER_NAME = 'user'
BOOK_AVAILABLE = 'Disponível'
BOOK_BORROWED = 'Emprestado'
KEY_NAME = 'name'
KEY_AUTHOR = 'author'
KEY_DAY_LOCATION = 'day_location'
KEY_TAX = 'tax [%]'
KEY_STATUS = 'status'
SCHOOLING_STUDENT = 'student'
SCHOOLING_GRADUATE = 'Graduate'
URL_RESERVE_BOOK_1_USER_1 = '/books/1/reserve/1'
URL_BOOKS_BY_USER = '/client/1/books'
URL_BOOKS = '/Books/'
MSG_USER_NOT_FOUND = b'User not found'
MSG_BOOK_NOT_FOUND = b'Book not found'


class BookTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_given_2_books_when_get_books_then_expect_2_books(self):
        # Arrange
        Book.objects.create(id=1, name=BOOK_NAME1, author=AUTHOR1)
        Book.objects.create(id=2, name=BOOK_NAME2, author=AUTHOR2)
        serialized_book_1 = {KEY_STATUS:BOOK_AVAILABLE, KEY_NAME: BOOK_NAME1, KEY_AUTHOR: AUTHOR1}
        serialized_book_2 = {KEY_STATUS:BOOK_AVAILABLE, KEY_NAME:BOOK_NAME2, KEY_AUTHOR:AUTHOR2}
        expected_content = [serialized_book_1, serialized_book_2]

        # Act
        response = self.client.get(URL_BOOKS)

        # Assert
        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(response.content, expected_content)

    def test_given_user_1_when_get_books_by_user_then_assert_books_by_user_user_equal_user_1(self):
        # Arrange
        user_1 = User.objects.create(id=1, name=USER_NAME, schooling=SCHOOLING_GRADUATE)
        today = datetime.now().date()
        Book.objects.create(id=1, name=BOOK_NAME1, author=AUTHOR1, user=user_1, pickup_date=today)
        Book.objects.create(id=2, name=BOOK_NAME2, author=AUTHOR2)
        book_1_serializer = [{KEY_NAME: BOOK_NAME1, KEY_AUTHOR: AUTHOR1,
                             KEY_TAX: 0, KEY_DAY_LOCATION: str(today), KEY_STATUS: BOOK_AVAILABLE}]

        # Act
        response = self.client.get(URL_BOOKS_BY_USER)

        # Assert
        self.assertJSONEqual(response.content, book_1_serializer)

    def test_given_http_verb_when_get_books_by_user_and_http_verb_not_get_then_assert_405(self):
        # Arrange

        # Act
        response = self.client.put(URL_BOOKS_BY_USER)

        # Assert
        self.assertEqual(response.status_code, 405)

    def test_given_no_users_when_get_books_by_user_then_assert_404(self):
        # Arrange

        # Act
        response = self.client.get(URL_BOOKS_BY_USER)

        # Assert
        self.assertEqual(response.status_code, 404)

    def test_given_user_1_when_reserve_book_1_then_assert_book_1_user_equal_user_1(self):
        # Arrange
        Book.objects.create(id=1, name=BOOK_NAME1, author=AUTHOR1)
        User.objects.create(id=1, name=USER_NAME, schooling=SCHOOLING_STUDENT)

        # Act
        response = self.client.patch(URL_RESERVE_BOOK_1_USER_1)

        # Assert
        self.assertEqual(response.status_code, 200)
        book_1 = Book.objects.get(name=BOOK_NAME1)
        self.assertEqual(book_1.user, User.objects.get(name=USER_NAME))
        self.assertEqual(book_1.status, Book.BORROWED)
        self.assertEqual(book_1.pickup_date, datetime.now().date())

    def test_given_no_books_when_reserve_book_1_then_assert_404_and_message(self):
        # Arrange

        # Act
        response = self.client.patch(URL_RESERVE_BOOK_1_USER_1)

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, MSG_BOOK_NOT_FOUND)

    def test_given_book_1_when_reserve_book_1_and_borrowed_then_assert_400(self):
        # Arrange
        Book.objects.create(id=1, name=BOOK_NAME1, author=AUTHOR1, status=Book.BORROWED)

        # Act
        response = self.client.patch(URL_RESERVE_BOOK_1_USER_1)

        # Assert
        self.assertEqual(response.status_code, 400)

    def test_given_no_users_when_reserve_book_1_then_assert_404_and_message(self):
        # Arrange
        Book.objects.create(id=1, name=BOOK_NAME1, author=AUTHOR1)

        # Act
        response = self.client.patch(URL_RESERVE_BOOK_1_USER_1)

        # Assert
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, MSG_USER_NOT_FOUND)

    def test_given_http_verb_when_reserve_book_1_and_http_verb_not_patch_then_assert_405(self):
        # Arrange

        # Act
        response = self.client.post(URL_RESERVE_BOOK_1_USER_1)

        # Assert
        self.assertEqual(response.status_code, 405)

    def test_given_date_when_tax_called_and_past_1_day_then_assert_result(self):
        # Arrange
        days_with_book = timedelta(days=1)
        pickup_book_date = datetime.now().date() - days_with_book
        tax = 0

        # Act
        result = tax_by_book(pickup_book_date)

        # Assert
        self.assertEqual(result, tax)

    def test_given_date_when_tax_called_and_past_4_day_then_assert_result(self):
        # Arrange
        days_with_book = timedelta(days=4)
        pickup_book_date = datetime.now().date() - days_with_book
        tax = 3.2

        # Act
        result = tax_by_book(pickup_book_date)

        # Assert
        self.assertEqual(result, tax)

    def test_given_date_when_tax_called_and_past_7_day_then_assert_result(self):
        # Arrange
        days_with_book = timedelta(days=7)
        pickup_book_date = datetime.now().date() - days_with_book
        tax = 6.6

        # Act
        result = tax_by_book(pickup_book_date)

        # Assert
        self.assertEqual(result, tax)

    def test_given_date_when_tax_called_and_past_10_day_then_assert_result(self):
        # Arrange
        days_with_book = timedelta(days=10)
        pickup_book_date = datetime.now().date() - days_with_book
        tax = 11.2

        # Act
        result = tax_by_book(pickup_book_date)

        # Assert
        self.assertEqual(result, tax)
