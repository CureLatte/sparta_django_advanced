from django.test import TestCase

from tabom.models import User
from tabom.models.article import Article
from tabom.services.article_service import create_an_article
from tabom.services.like_service import do_like


class TestArticleRouter(TestCase):
    def test_create_article(self) -> None:
        # Given
        title = "test_title"

        # When
        response = self.client.post(
            f"/api/v1/articles/",
            data={"title": title},
            content_type="application/json",
        )

        # Then
        self.assertEqual(201, response.status_code)
        self.assertEqual(title, response.json()["title"])

    def test_get_article(self) -> None:
        # Given
        title = "test_title"
        user = User.objects.create(name="test_user")
        article = create_an_article(title)
        like = do_like(user.id, article.id)

        # When
        response = self.client.get(f"/api/v1/articles/{article.id}", {"user_id": user.id})

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(title, response.json()["title"])
        self.assertEqual(like.id, response.json()["my_likes"][0]["id"])

    def test_get_articles(self) -> None:
        # Given
        title = "test_title"
        user = User.objects.create(name="test_user")
        article1 = create_an_article(title)
        create_an_article(title)
        like = do_like(user.id, article1.id)

        # When
        response = self.client.get(f"/api/v1/articles/", {"user_id": user.id})

        # Then
        self.assertEqual(200, response.status_code)
        self.assertEqual(title, response.json()[0]["title"])
        self.assertEqual(like.id, response.json()[1]["my_likes"][0]["id"])

    def test_delete_article(self) -> None:
        # Given
        article = create_an_article("test_title")

        # When
        response = self.client.delete(f"/api/v1/articles/{article.id}")

        self.assertEqual(204, response.status_code)
        self.assertFalse(Article.objects.filter(id=article.id).exists())