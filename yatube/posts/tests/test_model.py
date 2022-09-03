from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Group, Post

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

    def tests_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        expected_object_name = post.text
        self.assertEqual(expected_object_name, str(post))

        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_post_text_help_text(self):
        """help_text post поля text совпадает с ожидаемым."""
        post = PostModelTest.post
        help_text = post._meta.get_field('text').help_text
        self.assertEqual(help_text, 'Введите текст поста')

    def test_post_text_verbose_name(self):
        """verbose_name post поля text совпадает с ожидаемым."""
        post = PostModelTest.post
        verbose_name = post._meta.get_field('text').verbose_name
        self.assertEqual(verbose_name, 'Текст поста')

    def test_post_pub_date_verbose_name(self):
        """verbose_name post поля pub_date совпадает с ожидаемым."""
        post = PostModelTest.post
        verbose_name = post._meta.get_field('pub_date').verbose_name
        self.assertEqual(verbose_name, 'Дата публикации')

    def test_post_author_verbose_name(self):
        """verbose_name post поля author совпадает с ожидаемым."""
        post = PostModelTest.post
        verbose_name = post._meta.get_field('author').verbose_name
        self.assertEqual(verbose_name, 'Автор поста')

    def test_group_title_help_text(self):
        """help_text title поля group совпадает с ожидаемым."""
        group = PostModelTest.group
        help_text = group._meta.get_field('title').help_text
        self.assertEqual(help_text, 'Выберите группу')

    def test_group_title_verbose_name(self):
        """verbose_name title поля group совпадает с ожидаемым."""
        group = PostModelTest.group
        verbose_name = group._meta.get_field('title').verbose_name
        self.assertEqual(verbose_name, 'Название группы')

    def test_group_slug_help_text(self):
        """help_text slug поля group совпадает с ожидаемым."""
        group = PostModelTest.group
        help_text = group._meta.get_field('slug').help_text
        self.assertEqual(help_text, 'Выберите адрес группы')

    def test_group_slug_verbose_name(self):
        """verbose_name slug поля group совпадает с ожидаемым."""
        group = PostModelTest.group
        verbose_name = group._meta.get_field('slug').verbose_name
        self.assertEqual(verbose_name, 'Адрес группы')

    def test_description_group_help_text(self):
        """help_text description поля group совпадает с ожидаемым."""
        group = PostModelTest.group
        help_text = group._meta.get_field('description').help_text
        self.assertEqual(help_text, 'Выберите описание группы')

    def test_description_group_verbose_name(self):
        """verbose_name description поля group совпадает с ожидаемым."""
        group = PostModelTest.group
        verbose_name = group._meta.get_field('description').verbose_name
        self.assertEqual(verbose_name, 'Описание группы')
