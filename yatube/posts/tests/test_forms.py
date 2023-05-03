from posts.models import Post
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class PostCreateEditFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         password='testpass')
        self.post = Post.objects.create(text='Тестовый текст',
                                        author=self.user)

    def test_create_post(self):
        """Создание записи в БД при отправке валидной формы."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('posts:post_create')
        data = {'text': 'Тестовый текст'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('posts:profile',
                                               args=(self.user.username,)))
        self.assertEqual(Post.objects.first().text, 'Тестовый текст')

    def test_edit_post(self):
        """Тест отправки валидной формы при редактировании поста."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('posts:post_edit', args=(self.post.id,))
        data = {'text': 'Измененный текст'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('posts:post_detail',
                                               args=(self.post.id,)))
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, 'Измененный текст')
