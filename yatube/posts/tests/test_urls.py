from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post, Group

User = get_user_model()

class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)


    def guest_client(self):
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/<slug>/',
            'posts/profile.html': '/posts/post_id',
            'posts/create_post.html': '/posts/post_id/edit',
             'not found 404': '/unexisting_page/',

        }

        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def authorized_client(self):
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': '/group/<slug>/',
            'posts/profile.html': '/posts/post_id',
            'posts/create_post.html': '/create/',
            'not found 404': '/unexisting_page/',
        }

        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
