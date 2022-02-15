from django.test import TestCase

from tabom.models import Like, User
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