from rest_framework.test import APITestCase
from.models import Book
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from api.views import *
from django.forms.models import model_to_dict

class Booktestcase(APITestCase):
    def setUp(self):
        self.normal_user= User.objects.create_user(username='normaluser', password='password')
        self.admin_user= User.objects.create_superuser(username='adminuser', password='password')
        
        self.author= Author.objects.create(name= 'Miracle Fasola')
        self.book1 = Book.objects.create(
            title="The Long Road", publication_year=2004, author=self.author
        )
        self.book2 = Book.objects.create(
            title="Time out", publication_year=2008, author=self.author
        )
        self.book3 = Book.objects.create(
            title="A fool for thought", publication_year=2014, author=self.author
        )
        self.list_url= reverse('book_list')
        self.post_url=reverse('book_create')
        self.update_url= reverse('book_update', args=[self.book1.id])
        self.delete_url= reverse('book_delete', args=[self.book3.id])




    def test_unauthenticated_access(self):
        response= self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_authenticated_can_view(self):
        
        self.client.force_authenticate(user= self.normal_user)
        
        response= self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_bookcreate_non_admin(self):
        data = {
        "title": "New Unique Book",
        "author": self.author.id,
        "publication_year": 2030
        }
        self.client.force_authenticate(user= self.normal_user)
        response= self.client.post(self.post_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bookcreate_future_year_invalid(self):
        data = {
        "title": "Invalid Book",
        "author": self.author.id,
        "publication_year": 2030
        }
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(self.post_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("publication_year", response.data)

    def test_bookcreate_admin(self):
        data = {
        "title": "New Unique Book",
        "author": self.author.id,
        "publication_year": 2020
        }
        self.client.force_authenticate(user= self.admin_user)
        response= self.client.post(self.post_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(response.data)

    def test_update_book(self):

        data = {
        "title": "Updated Title",
        "author": self.author.id,
        "publication_year": 2022
    }
        self.client.force_authenticate(user= self.admin_user)
        response= self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
        self.assertEqual(response.data['publication_year'], 2022)

    def test_partial_update(self):
        data = {
        "title": "Patched Title",
        "publication_year": 2014
        }
        self.client.force_authenticate(user= self.admin_user)
        response= self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Patched Title')
        self.assertEqual(response.data['publication_year'], 2014)
    def test_delete(self):
        self.client.force_authenticate(user= self.admin_user)
        response= self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book3.id).exists())

        
