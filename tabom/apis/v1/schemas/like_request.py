from ninja import Schema


class LikeRequest(Schema):
    article_id: int
    user_id: int
