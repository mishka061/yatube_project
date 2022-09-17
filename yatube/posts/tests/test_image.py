import shutil
import tempfile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from posts.models import Post, Group, User

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ImgageViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )

        cls.post = Post.objects.create(
            text='Текст поста',
            author=cls.user,
            group=cls.group,
            pub_date='Дата публикации',
            image=cls.uploaded
        )
    cache.clear()

    def setUp(self):
        """ПРОСТО ПОЛЬЗОВАТЕЛЬ"""
        self.guest_client = Client()
        """АВТОР ПОСТОВ"""
        self.author_post = Client()
        self.author_post.force_login(self.user)
        """БЕЗ ПОСТОВ"""
        self.authorized_user = User.objects.create_user(username='Автор')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.authorized_user)
    cache.clear()

    def test_image_post_detail(self):
        response = self.authorized_client.get(reverse
                                              ('posts:post_detail',
                                               kwargs={'post_id': self.post.id}
                                               ))
        self.assertEqual(response.context['post'].image,
                         f'posts/{self.uploaded}')
    cache.clear()

    def test_create_post_form(self):
        """Валидная форма создает запись в Post с картинкой."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
            'image': self.uploaded,
        }
        self.client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), posts_count, 1)
        self.assertTrue(
            Post.objects.filter(image='posts/small.gif').exists())
    cache.clear()

    def test_image_templates(self):
        """Возвращает адреса"""
        used_templates = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.user}),
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        }
        for address in used_templates:
            with self.subTest(address=address):
                self.authorized_client.get(address)
                self.assertTrue(Post.objects.filter(
                    image='posts/small.gif').exists())
    cache.clear()


@classmethod
def tearDownClass(cls):
    shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
    super().tearDownClass()
