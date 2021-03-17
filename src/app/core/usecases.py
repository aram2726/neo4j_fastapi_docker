from abc import ABCMeta
from abc import abstractmethod
from collections import namedtuple
from typing import Dict
from typing import List
from typing import Iterable

from src.app.core.repositories import BaseManageableRepository


class BaseUseCase(metaclass=ABCMeta):

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class GetCustomerUseCase(BaseUseCase):
    def __init__(self, key: str, condition: str, value: str, customers_repo: BaseManageableRepository):
        self._key = key
        self._condition = condition
        self._value = value
        self._customers_repo = customers_repo

    async def execute(self):
        data = await self._customers_repo.filter(self._key, self._condition, self._value)
        return data


class ListCustomersUseCase(BaseUseCase):
    def __init__(self, customers_repo: BaseManageableRepository):
        self._customers_repo = customers_repo

    async def execute(self):
        data = await self._customers_repo.get_all()
        return data


class SynchronizeUseCase(BaseUseCase):
    def __init__(self,
                 data: List[Dict],
                 customers_repo: BaseManageableRepository,
                 countries_repo: BaseManageableRepository,
                 cities_repo: BaseManageableRepository,
                 companies_repo: BaseManageableRepository,):
        self._data = data
        self._customers_repo = customers_repo
        self._countries_repo = countries_repo
        self._cities_repo = cities_repo
        self._companies_repo = companies_repo

    async def execute(self):
        countries = set()
        cities = set()
        companies = set()
        for customer in self._data:
            Country = namedtuple("Country", ["name"])
            City = namedtuple("City", ["name", "country"])
            Company = namedtuple("Company", ["name"])

            countries.add(Country(name=customer["country"]))
            cities.add(City(name=customer["city"], country=customer["country"]))
            companies.add(Company(name=customer["companyName"]))

        await self.sync_data(self.convert_set_nt_to_list_dict(countries), self._countries_repo)
        await self.sync_data(self.convert_set_nt_to_list_dict(cities), self._cities_repo)
        await self.sync_data(self.convert_set_nt_to_list_dict(companies), self._companies_repo)
        await self.sync_data(self._data, self._customers_repo)

        await self.create_relations()

    def convert_set_nt_to_list_dict(self, set_of_nt):
        data = []
        for item in set_of_nt:
            item_dict = {}
            for field in item._fields:
                item_dict[field] = getattr(item, field, None)
            data.append(item_dict)
        return data

    async def sync_data(self, items: List[Dict], repo: BaseManageableRepository):
        for item in items:
            await repo.insert(item)

    async def create_relations(self):
        await self._cities_repo.db.create_relation(
            "city", "located_in", "country", {"key": "country", "condition": "=", "value": "name"})

        await self._customers_repo.db.create_relation(
            "customer", "located_in", "city", {"key": "city", "condition": "=", "value": "name"})
        await self._customers_repo.db.create_relation(
            "customer", "works_in", "company",
            {"key": "companyName", "condition": "=", "value": "name"})


class CreateUserUseCase(BaseUseCase):

    def __init__(self, data: Dict, customers_repo: BaseManageableRepository):
        self._data = data
        self._customers_repo = customers_repo

    async def execute(self):
        await self._customers_repo.insert(self._data)


class GraphViewUseCase(BaseUseCase):
    def __init__(self, customers_repo: BaseManageableRepository):
        self._customers_repo = customers_repo

    async def execute(self):
        data = await self._customers_repo.graph_view()
        return data


class GetCountryUseCase(BaseUseCase):
    def __init__(self, key: str, condition: str, value: str, countries_repo: BaseManageableRepository):
        self._key = key
        self._condition = condition
        self._value = value
        self._countries_repo = countries_repo

    async def execute(self):
        data = await self._countries_repo.filter(self._key, self._condition, self._value)
        return data


class ListCountriesUseCase(BaseUseCase):
    def __init__(self, countries_repo: BaseManageableRepository):
        self._countries_repo = countries_repo

    async def execute(self):
        data = await self._countries_repo.get_all()
        return data


class GetCityUseCase(BaseUseCase):
    def __init__(self, key: str, condition: str, value: str, cities_repo: BaseManageableRepository):
        self._key = key
        self._condition = condition
        self._value = value
        self._cities_repo = cities_repo

    async def execute(self):
        data = await self._cities_repo.filter(self._key, self._condition, self._value)
        return data


class ListCitiesUseCase(BaseUseCase):
    def __init__(self, cities_repo: BaseManageableRepository):
        self._cities_repo = cities_repo

    async def execute(self):
        data = await self._cities_repo.get_all()
        return data


class GetCompanyUseCase(BaseUseCase):
    def __init__(self, key: str, condition: str, value: str, companies_repo: BaseManageableRepository):
        self._key = key
        self._condition = condition
        self._value = value
        self._companies_repo = companies_repo

    async def execute(self):
        data = await self._companies_repo.filter(self._key, self._condition, self._value)
        return data


class ListCompaniesUseCase(BaseUseCase):
    def __init__(self, companies_repo: BaseManageableRepository):
        self._companies_repo = companies_repo

    async def execute(self):
        data = await self._companies_repo.get_all()
        return data
