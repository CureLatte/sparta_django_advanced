from datetime import datetime
from time import sleep

from django.db import connection
from django.test import TestCase

from tabom.models import User


class TestAutoNow(TestCase):
    def test_auto_now_field_is_set_when_save(self) -> None:
        user = User(name="test")
        user.save()
        self.assertIsNotNone(user.updated_at)
        self.assertIsNotNone(user.created_at)

    def test_auto_now_field_not_set_when_row_sql_update_executed(self) -> None:
        # Given
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO tabom_user(id, name, created_at, updated_at)"
                "VALUES (1, 'hihi', '1999-01-01 10:10:10','1999-01-01 10:10:10')"
            )

            # When
            sleep(1)
            cursor.execute("UPDATE tabom_user SET name='changed' WHERE id=1")

        # Then
        user = User.objects.filter(id=1).get()
        self.assertEqual(user.updated_at, datetime(year=1999, month=1, day=1, hour=10, minute=10, second=10))
