from django.core.cache import cache
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostCacheTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            text='Текст поста',
            author=cls.user,
            group=cls.group,
            pub_date='Дата публикации',

        )
        cls.caches = 'Тестовый кеш'

    def setUp(self):
        self.guest_client = Client()
        self.author_post = Client()
        self.author_post.force_login(self.user)
        self.authorized_user = User.objects.create_user(username='НЕ АВТОР')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.authorized_user)
    cache.clear()

    def test_cache_index(self):
        """Проверка хранения и очищения кэша для index."""
        response = self.authorized_client.get(reverse('posts:index'))
        post_cache = response.content
        Post.objects.create(
            text='test_new_post',
            author=self.user
        )
        response_old = self.authorized_client.get(reverse('posts:index'))
        old_posts = response_old.content
        self.assertEqual(old_posts, post_cache)
        cache.clear()
        response_new = self.authorized_client.get(reverse('posts:index'))
        new_post = response_new.content
        self.assertNotEqual(old_posts, new_post)
    cache.clear()
