from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostCreateForm(TestCase):
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
        cls.form = PostCreateForm()

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Проверка создания новой записи"""
        posts_count = Post.objects.count()
        form_data = {
            'group': PostCreateForm.group.id,
            'text': 'Тестовый текст',
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': 'author'}))

        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Тестовый текст',
                group=PostCreateForm.group,
            ).exists()
        )
        new_post = Post.objects.last()
        self.assertEqual(new_post.author, self.user)
        self.assertEqual(new_post.group, self.group)

    def test_post_edit(self):
        """Проверка страницы редактирования поста"""
        reverse_url = reverse(
            'posts:post_edit', kwargs={'post_id': self.post.id}
        )
        posts_count = Post.objects.count()
        from_data = {
            'text': 'Измененённое сообщение',
            'group': self.group.id
        }
        response = self.authorized_client.post(
            reverse_url,
            data=from_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(text='Измененённое сообщение').exists()
        )
        old_group_response = self.authorized_client.get(
            reverse('posts:group_list', args=(self.group.slug,))
        )
        self.assertEqual(
            old_group_response.context['page_obj'].paginator.count, 1
        )
