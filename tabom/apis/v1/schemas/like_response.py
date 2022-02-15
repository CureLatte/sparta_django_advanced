from ninja import Schema


class LikeResponse(Schema):
    id: int
    user_id: int
    article_id: int
