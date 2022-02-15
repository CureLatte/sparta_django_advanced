from ninja import Schema


class ArticleCreateRequest(Schema):
    title: str
