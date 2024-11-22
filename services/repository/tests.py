from typing import List
import unittest
from repository import BaseItemRepository
from services.models import RoomType, Item, ItemType
from sqlite_repository import SqlItemRepository
from pathlib import Path

class RepositoryTestCase(unittest.TestCase):

    def setUp(self) -> None:
        sql_relative_path = Path("../../storage/testbase.db")
        sql_abs_path = Path.resolve(sql_relative_path)
        test_sql_repo = SqlItemRepository(sql_abs_path)
        pass
