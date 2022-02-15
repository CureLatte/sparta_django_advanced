from django.db import models

from tabom.models.base_model import BaseModel


class User(BaseModel):
    name = models.CharField(max_length=50)
