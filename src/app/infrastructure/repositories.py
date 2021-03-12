import os
import sys
from typing import Optional
from typing import List

import dotenv

from src.app.core.entities import EnvItemEntity
from src.app.core.repositories import BaseReadOnlyRepository
from src.app.core.repositories import BaseManageableRepository
from src.app.infrastructure.databases import AbstractBaseDBClient


class EnvironRepository(BaseReadOnlyRepository):
    def __init__(self, basedir):
        dotenv.load_dotenv(os.path.join(basedir, ".env"))

    def get_one(self, key) -> Optional[EnvItemEntity]:
        if sys.platform == "win32":
            key = key.upper()  # pragma: no cover
        val = os.getenv(key)

        return None if val is None else EnvItemEntity(uuid=key, val=val)

    def get_all(self, limit: int = None, offset: int = None) -> List[EnvItemEntity]:  # type: ignore
        items = dict(os.environ).items()
        return [EnvItemEntity(uuid=k, val=v) for k, v in items]

    def filter(self, key: str, condition: str, value: str):
        pass


class CustomersRepository(BaseManageableRepository):

    NODE_NAME = "Customer"

    def __init__(self, db: AbstractBaseDBClient):
        self._db = db

    @property
    def db(self):
        return self._db

    async def get_all(self, limit: int = None, offset: int = None) -> List[EnvItemEntity]:
        data = await self.db.select_all(self.NODE_NAME)
        return data

    async def filter(self, key: str, condition: str, value: str):
        data = await self.db.filter(self.NODE_NAME, key, condition, value)
        return data

    async def insert(self, data: dict):
        await self.db.insert(self.NODE_NAME, data)

    async def update(self, uuid: str, data: dict):
        pass

    async def delete(self, uuid: str):
        pass

    async def graph_view(self):
        return await self.db.graph_view()


class CountriesRepository(BaseManageableRepository):

    NODE_NAME = "Country"

    def __init__(self, db: AbstractBaseDBClient):
        self._db = db

    @property
    def db(self):
        return self._db

    async def get_all(self, limit: int = None, offset: int = None) -> List[EnvItemEntity]:
        data = await self.db.select_all(self.NODE_NAME)
        return data

    async def filter(self, key: str, condition: str, value: str):
        data = await self.db.filter(self.NODE_NAME, key, condition, value)
        return data

    async def insert(self, data: dict):
        await self.db.insert(self.NODE_NAME, data)

    async def update(self, uuid: str, data: dict):
        pass

    async def delete(self, uuid: str):
        pass


class CitiesRepository(BaseManageableRepository):

    NODE_NAME = "City"

    def __init__(self, db: AbstractBaseDBClient):
        self._db = db

    @property
    def db(self):
        return self._db

    async def get_all(self, limit: int = None, offset: int = None) -> List[EnvItemEntity]:
        data = await self.db.select_all(self.NODE_NAME)
        return data

    async def filter(self, key: str, condition: str, value: str):
        data = await self.db.filter(self.NODE_NAME, key, condition, value)
        return data

    async def insert(self, data: dict):
        await self.db.insert(self.NODE_NAME, data)

    async def update(self, uuid: str, data: dict):
        pass

    async def delete(self, uuid: str):
        pass


class CompaniesRepository(BaseManageableRepository):

    NODE_NAME = "Company"

    def __init__(self, db: AbstractBaseDBClient):
        self._db = db

    @property
    def db(self):
        return self._db

    async def get_all(self, limit: int = None, offset: int = None) -> List[EnvItemEntity]:
        data = await self.db.select_all(self.NODE_NAME)
        return data

    async def filter(self, key: str, condition: str, value: str):
        data = await self.db.filter(self.NODE_NAME, key, condition, value)
        return data

    async def insert(self, data: dict):
        await self.db.insert(self.NODE_NAME, data)

    async def update(self, uuid: str, data: dict):
        pass

    async def delete(self, uuid: str):
        pass
