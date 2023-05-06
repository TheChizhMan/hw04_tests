from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post, Comment

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        expected_group_name = self.group.title
        expected_post_name = self.post.text[:settings.COUNT_TEXT]
        self.assertEqual(str(self.group), expected_group_name)
        self.assertEqual(str(self.post), expected_post_name)

    def test_verbose_name_and_help_text(self):
        """Проверяем verbose_name и help_text у полей модели Post."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа'}
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост'}

        for field, expected_verbose in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name,
                    expected_verbose)

        for field, expected_help_text in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text,
                    expected_help_text)


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = User.objects.create(username='testuser')
        post = Post.objects.create(text='Test post',
                                   author=author)
        cls.comment = Comment.objects.create(post=post,
                                             text='Test comment',
                                             author=author)

    def test_text_label(self):
        comment = self.comment
        field_label = comment._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'Текст коментария')

    def test_text_help_text(self):
        comment = self.comment
        help_text = comment._meta.get_field('text').help_text
        self.assertEqual(help_text, 'Введите текст коментария')

    def test_ordering(self):
        self.assertEqual(Comment._meta.ordering, ['-created'])
