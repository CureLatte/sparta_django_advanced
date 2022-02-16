from typing import Any, List

from django.db import models

from tabom.models.base_model import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=255)
    like_count = models.IntegerField(default=0)

    my_likes: List[Any]
