from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='testuser')
        Post.objects.create(id=46, text='Тестовый заголовок',
                            author=cls.user)

        Group.objects.create(title='Тестовый тайтл',
                             slug='test-slug')

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = PostURLTests.user
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        # Шаблоны по адресам
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/test-slug/',
            'posts/profile.html': '/profile/testuser/',
            'posts/post_detail.html': '/posts/46/',
        }

        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)

    def test_create_post_page(self):
        """Страница создания доступна только для авторизованных."""
        # Попытка доступа неавторизованного пользователя
        response = self.guest_client.get('/create/')
        # Проверка перенаправления на страницу входа
        self.assertRedirects(response, '/auth/login/?next=/create/')
        # Попытка доступа авторизованного пользователя
        response = self.authorized_client.get('/create/')
        # Проверка доступности страницы
        self.assertEqual(response.status_code, 200)

    def test_edit_post_page(self):
        """Страница редактирования доступна только для автора публикации."""
        # Создаем пост
        post = Post.objects.create(text='Тестовый текст', author=self.user)
        # Попытка доступа неавторизованного пользователя
        response = self.guest_client.get(f'/posts/{post.id}/edit/')
        # Проверка перенаправления на страницу входа
        self.assertRedirects(response,
                             f'/auth/login/?next=/posts/{post.id}/edit/')
        # Создаем второго пользователя
        other_user = User.objects.create_user(username='otheruser')
        # Создаем третий клиент
        other_authorized_client = Client()
        # Авторизуем второго пользователя
        other_authorized_client.force_login(other_user)
        # Попытка доступа пользователя, который не автор публикации
        response = other_authorized_client.get(f'/posts/{post.id}/edit/')
        # Попытка доступа авторизованного автора публикации
        response = self.authorized_client.get(f'/posts/{post.id}/edit/')
        # Проверка доступности страницы
        self.assertEqual(response.status_code, 200)
