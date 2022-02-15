# from django.db import connection
# from django.test import TestCase
# from django.test.utils import CaptureQueriesContext
#
# from tabom.models import Article, Like, User
#
#
# class TestCascade(TestCase):
#     def test_capture_what_queries_excuted_when_cascade(self) -> None:
#         user = User.objects.create(name="user1")
#         article = Article.objects.create(title="artice1")
#         like = Like.objects.create(user_id=user.id, article_id=article.id)
#         with CaptureQueriesContext(connection) as ctx:
#             article.delete()
#             print(ctx)
