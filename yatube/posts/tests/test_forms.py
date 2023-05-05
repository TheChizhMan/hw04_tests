from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostCreateEditFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.post = Post.objects.create(text='Тестовый текст',
                                        author=self.user)
        self.group = Group.objects.create(title='Тестовая группа',
                                          slug='test-slug')

    def test_create_post(self):
        """Создание записи в БД при отправке валидной формы."""
        url = reverse('posts:post_create')
        data = {'text': 'Тестовый текст'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('posts:profile',
                                               args=(self.user.username,)))
        self.assertEqual(Post.objects.first().text, data['text'])

    def test_edit_post(self):
        """Тест отправки валидной формы при редактировании поста."""
        url = reverse('posts:post_edit', args=(self.post.id,))
        data = {'text': 'Измененный текст'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('posts:post_detail',
                                               args=(self.post.id,)))
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, data['text'])

    def test_edit_post_with_group_anonymous(self):
        """Тест создания иредактирования анонимным пользователем."""
        self.client.logout()
        url = reverse('posts:post_edit', args=(self.post.id,))
        data = {'text': 'Измененный текст', 'group': self.group.id}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_anonymous_create_post(self):
        """Проверка, что анонимный пользователь не может создать пост."""
        self.client.logout()
        url = reverse('posts:post_create')
        data = {'text': 'Тестовый текст'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('login') + '?next=' + url)
