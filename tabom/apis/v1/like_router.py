from typing import Tuple

from django.db import IntegrityError
from django.http import HttpRequest
from ninja import Router
from ninja.errors import HttpError

from tabom.apis.v1.schemas.like_request import LikeRequest
from tabom.apis.v1.schemas.like_response import LikeResponse
from tabom.models import Article, Like, User
from tabom.services.like_service import do_like, undo_like

router = Router(tags=["likes"])


@router.post("/", response={201: LikeResponse})
def post_like(request: HttpRequest, like_request: LikeRequest) -> Tuple[int, Like]:

    try:
        # 좋아요 갯수 추가
        like = do_like(like_request.user_id, like_request.article_id)

    except User.DoesNotExist:
        # 유저가 존재하지 않을 경우
        raise HttpError(404, f"User #{like_request.user_id} Not Found")

    except Article.DoesNotExist:
        # 기사가 존재하지 않을 경우
        raise HttpError(404, f"Article id #{like_request.article_id} Not Found")

    except IntegrityError:
        # 두번 누를 경우
        raise HttpError(400, "duplicate like")

    return 201, like


@router.delete("/", response={204: None})
def delete_like(request: HttpRequest, user_id: int, article_id: int) -> Tuple[int, None]:
    undo_like(user_id, article_id)
    return 204, None
