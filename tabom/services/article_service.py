from django.core.paginator import Page, Paginator
from django.db.models import Prefetch, QuerySet

from tabom.models import Article, Like


def get_an_article(article_id: int) -> Article:
    return Article.objects.filter(id=article_id).get()


def get_article_list(user_id: int, offset: int, limit: int) -> QuerySet[Article]:
    return (
        Article.objects.order_by("-id")
        .prefetch_related("like_set")[offset : offset + limit]
        .prefetch_related(Prefetch("like_set", queryset=Like.objects.filter(user_id=user_id), to_attr="my_likes"))[
            offset : offset + limit
        ]
    )
