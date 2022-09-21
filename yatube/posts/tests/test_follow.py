from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from posts.models import Post, Follow

User = get_user_model()


class FollowersViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='follower', password='284'
        )
        cls.subscribed_user = Client()
        cls.subscribed_user.force_login(cls.user)
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.follower = Client()
        cls.follower.force_login(cls.user)
        cls.user2 = User.objects.create_user(
            username='author', password='482'
        )
        cls.author = Client()
        cls.author.force_login(cls.user2)
        cls.post = Post.objects.create(
            text='Test_text',
            author=cls.user2,
        )

    def test_follower_can_follow(self):
        """пользователь может подписываться
        на других
        """
        self.follower.get(
            reverse('posts:profile_follow', kwargs={
                'username': self.user2.username}
            )
        )
        self.assertTrue(
            Follow.objects.filter(
                user=self.user,
                author=self.user2).exists()
        )
        self.assertEqual(Follow.objects.count(), 1)

    def test_new_post_appears_for_subscribed_users_only(self):
        """Новая запись появляется в ленте подписчиков."""
        Follow.objects.create(
            user=self.user,
            author=self.user2,
        )
        response = self.authorized_client.get(reverse('posts:follow_index'))
        objects = list(response.context['page_obj'])
        self.assertIn(objects[0].text, self.post.text)

    def test_content_for_follower_and_unfollow(self):
        """Подписанный пользователь видит посты и может отписаться."""
        self.follower = Follow.objects.create(
            user=self.user, author=self.user2
        )
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertEqual(len(response.context['page_obj']), 1)
        self.follower.delete()
        response1 = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertNotEqual(response.content, response1.content)

    def test_follow_no(self):
        """нельзя подписаться на самого себя"""
        self.follower.get(
            reverse('posts:profile_follow', kwargs={
                'username': self.user.username}
            )
        )
        self.assertFalse(
            Follow.objects.filter(
                user=self.user,
                author=self.user).exists()
        )
        self.assertNotEqual(Follow.objects.count(), 1)
