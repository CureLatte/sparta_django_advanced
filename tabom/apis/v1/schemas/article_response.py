from typing import List, Optional

from ninja import Schema

from tabom.apis.v1.schemas.like_response import LikeResponse


class ArticleResponse(Schema):
    id: int
    title: str
    my_likes: Optional[List[LikeResponse]]
