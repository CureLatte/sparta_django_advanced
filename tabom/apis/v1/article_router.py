from typing import List, Tuple

from django.db.models import QuerySet
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from tabom.apis.v1.schemas.article_create_request import ArticleCreateRequest
from tabom.apis.v1.schemas.article_response import ArticleResponse
from tabom.models import Article
from tabom.services.article_service import (
    create_an_article,
    delete_an_article,
    get_an_article,
    get_article_list,
)

router = Router(tags=["articles"])


@router.post("/", response={201: ArticleResponse})
def create_article(request: HttpRequest, article_create_request: ArticleCreateRequest) -> Tuple[int, Article]:
    article = create_an_article(article_create_request.title)
    return 201, article


@router.get("/", response=List[ArticleResponse])
def get_articles(request: HttpRequest, user_id: int, offset: int = 0, limit: int = 10) -> QuerySet[Article]:
    articles = get_article_list(user_id, offset, limit)
    return articles


@router.get("/{article_id}", response=ArticleResponse)
def get_article(request: HttpRequest, user_id: int, article_id: int) -> Article:
    try:
        aritlcle = get_an_article(user_id, article_id)
    except Article.DoesNotExist:
        raise HttpError(404, f"Article #{article_id} Not Found")
    return aritlcle


@router.delete("/{article_id}", response={204: None})
def delete_article(request: HttpRequest, article_id: int) -> Tuple[int, None]:
    delete_an_article(article_id)
    return 204, None
