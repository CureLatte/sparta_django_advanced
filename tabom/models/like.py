from django.db import models

from tabom.models.article import Article
from tabom.models.base_model import BaseModel
from tabom.models.user import User


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "article"], name="unique_user_article")]
