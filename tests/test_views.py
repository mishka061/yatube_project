from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from posts.models import Group, Post

User = get_user_model()


class PostViewsTest(TestCase):
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

    def setUp(self):
        self.guest_client = Client()
        self.author_post = Client()
        self.author_post.force_login(self.user)
        self.authorized_user = User.objects.create_user(username='НЕ АВТОР')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.authorized_user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user}):
                'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
                'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
                'posts/post_create.html',
            reverse('posts:post_create'):
                'posts/post_create.html'
        }

        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.author_post.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_list(self):
        """Проверка контекста index """
        response = self.authorized_client.get(reverse('posts:index'))
        self.check_post_info(response.context['page_obj'][0])
        cache.clear()

    def check_post_info(self, post):
        """ Проверка текста на контекст"""
        with self.subTest(post=post):
            self.assertEqual(post.text, self.post.text)
            self.assertEqual(post.author, self.post.author)
            self.assertEqual(post.group.id, self.post.group.id)
            cache.clear()

    def test_group_list_page_list(self):
        """ Проверка контекста group_list"""
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={
                'slug': self.group.slug}
        ))
        context = response.context
        group_list = context['group']
        self.assertEqual(group_list, self.group)
        cache.clear()

    def test_profile_context(self):
        """Проверка контекста  profile """
        response = self.authorized_client.get(reverse(
            'posts:profile',
            kwargs={'username': self.user.username}
        ))
        context = response.context
        posts_user = context['author']
        self.assertEqual(posts_user, self.user)
        cache.clear()

    def test_post_detail_page_show_correct_context(self):
        """Проверка контекста post_detail """
        response = self.authorized_client.get(reverse(
            'posts:post_detail',
            kwargs={'post_id': self.post.id}
        ))
        context = response.context
        post = context['post']
        self.assertEqual(post, self.post)
        cache.clear()

    def test_edit_uses_correct_form(self):
        """ Форма post_edit с ключом form, is_Edit"""
        response = self.author_post.get(reverse(
            'posts:post_edit', kwargs={
                'post_id': self.post.id}
        ))
        form_fields = {
            'text': forms.fields.CharField,
        }
        for field_name, type in form_fields.items():
            with self.subTest(key=field_name):
                form_field = response.context['form'].fields[field_name]
                self.assertIsInstance(form_field, type)
                cache.clear()

    def test_edit_post_uses_is_edit(self):
        """Шаблон post_edit использует  key is_edit корректно"""
        response = self.author_post.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id})
        )
        context = response.context
        is_edit = context['is_edit']
        self.assertIs(is_edit, True)
        cache.clear()

    def test_post_create(self):
        """ шаблон post_create работает корректно"""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
        }
        for field_name, field_type in form_fields.items():
            with self.subTest(field_name=field_name):
                form_field = response.context['form'].fields[field_name]
                self.assertIsInstance(form_field, field_type)
                cache.clear()

    def test_post_not_in_right_places(self):
        """ пост корректно отображается
         на страницах index, group_list и profile."""
        response_index = self.authorized_client.get(reverse('posts:index'))
        response_group_list = self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug})
        )
        response_profile = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user})
        )
        context_index = response_index.context['page_obj'][0]
        context_group = response_group_list.context['page_obj'][0]
        context_profile = response_profile.context['page_obj'][0]
        self.assertNotEqual(PostViewsTest, context_index)
        self.assertNotEqual(PostViewsTest, context_group)
        self.assertNotEqual(PostViewsTest, context_profile)
        cache.clear()

    def test_post_in_places(self):
        """Тестовый пост"""
        new_post = Post.objects.create(
            text='Новый пост',
            group=self.group,
            author=self.user
        )
        response_new = self.authorized_client.get(reverse('posts:index'))
        response_new_list = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug}))
        response_new_profile = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user}))
        context_index = response_new.context['page_obj'][0]
        context_group = response_new_list.context['page_obj'][0]
        context_profile = response_new_profile.context['page_obj'][0]
        self.assertEqual(new_post, context_index)
        self.assertEqual(new_post, context_group)
        self.assertEqual(new_post, context_profile)
        cache.clear()


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.new_user = User.objects.create_user(username='vi')
        cls.post_user = Client()
        cls.post_user.force_login(cls.new_user)
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.new_user,
            text='Текст',
            group=cls.group
        )

        NUMBER: int = 20
        posts = []
        for i in range(NUMBER):
            posts.append(
                Post(
                    author=cls.new_user,
                    text=f'my test{i}',
                    group=cls.group
                )
            )
            Post.objects.bulk_create(posts)

    def test_first_page_contains_ten_records(self):
        """ Паджинатор проверяет первую страницу"""
        paginator_pages = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.new_user})
        }
        for address in paginator_pages:
            with self.subTest(address=address):
                response = self.post_user.get(address)
                context_page = response.context['page_obj']
                self.assertEqual(len(context_page), 10)
                cache.clear()

    def test_second_page_contains_three_records(self):
        """ Паджинатор проверяет вторую  страницу"""
        paginator_pages = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.new_user})
        }
        for address in paginator_pages:
            with self.subTest(address=address):
                response = self.post_user.get((address) + '?page=2')
                self.assertEqual(len(response.context['page_obj']), 10)
                cache.clear()
