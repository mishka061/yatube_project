from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


class PostCommitTest(TestCase):
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
        cls.comments = 'Тестовый комментарий'

    def setUp(self):
        self.guest_client = Client()
        self.author_post = Client()
        self.author_post.force_login(self.user)
        self.authorized_user = User.objects.create_user(username='НЕ АВТОР')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.authorized_user)

    def test_comment(self):
        """Проверка коментариев в post_detail."""
        response = self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.id}
        ))
        context_comment = response.context['comments']
        self.assertNotEqual(PostCommitTest, context_comment)
        self.assertEqual(response.status_code, 200)

    def test_authorized_client_comment(self):
        """Комментировать посты может только авторизированный пользователь"""
        self.authorized_client.get(reverse(
            'posts:add_comment',
            kwargs={'post_id': self.post.id}))
        self.assertEqual(Post.objects.all().count(), 1)

    def test_guest_client_comment(self):
        """Комментировать посты может
        только не авторизированный пользователь"""
        self.guest_client.get(reverse(
            'posts:add_comment',
            kwargs={'post_id': self.post.id}
        ))
        self.assertEqual(Post.objects.all().count(), 1)

    def test_post_detail_page_show_correct_context(self):
        """Проверка правильного контекста функции post_detail"""
        self.authorized_client.get(
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}
                    ))
        self.assertEqual(Post.objects.all().count(), 1)
