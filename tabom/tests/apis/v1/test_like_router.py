from django.test import TestCase

from tabom.models import Article, Like, User
from tabom.services.article_service import create_an_article
from tabom.services.like_service import do_like


class TestLikeRouter(TestCase):
    def test_post_like(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        article = create_an_article("test_title")

        # When
        response = self.client.post(
            "/api/v1/likes/",
            data={
                "user_id": user.id,
                "article_id": article.id,
            },
            content_type="application/json",
        )

        # Then
        self.assertEqual(201, response.status_code)
        self.assertEqual(user.id, response.json()["user_id"])

    def test_post_like_User_is_None(self) -> None:
        # Given
        user_id = 9988
        article = create_an_article("test_title")

        # When
        response = self.client.post(
            "/api/v1/likes/",
            data={
                "user_id": user_id,
                "article_id": article.id,
            },
            content_type="application/json",
        )

        # Then
        self.assertEqual(404, response.status_code)
        self.assertEqual(f"User #{user_id} Not Found", response.json()["detail"])

    def test_post_like_Article_is_None(self) -> None:
        # Given
        article_id = 9988
        user = User.objects.create(name="test_name")

        # When
        response = self.client.post(
            "/api/v1/likes/",
            data={
                "user_id": user.id,
                "article_id": article_id,
            },
            content_type="application/json",
        )

        # Then
        self.assertEqual(404, response.status_code)
        self.assertEqual(f"Article id #{article_id} Not Found", response.json()["detail"])

    def test_post_like_duplicate_do_like(self) -> None:
        # Given
        user = User.objects.create(name="test_name")
        article = create_an_article("test_title")
        do_like(user.id, article.id)

        # When
        response = self.client.post(
            "/api/v1/likes/",
            data={
                "user_id": user.id,
                "article_id": article.id,
            },
            content_type="application/json",
        )

        # Then
        self.assertEqual(400, response.status_code)
        self.assertEqual("duplicate like", response.json()["detail"])

    def test_delete_like(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = create_an_article("test_title")
        like = do_like(user.id, article.id)

        # When
        response = self.client.delete(f"/api/v1/likes/?user_id={user.id}&article_id={article.id}")

        # Then
        self.assertEqual(204, response.status_code)
        self.assertFalse(Like.objects.filter(id=like.id).exists())

    def test_delete_non_existing_like(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = create_an_article("test_title")

        # When
        response = self.client.delete(f"/api/v1/likes/?user_id={user.id}&article_id={article.id}")

        # Then
        self.assertEqual(204, response.status_code)
        self.assertEqual(0, Article.objects.filter(id=article.id).get().like_count)
