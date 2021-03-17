from abc import ABCMeta
from typing import Any
from typing import Dict
from typing import List

from fastapi.requests import Request

import src.app.infrastructure as config

from src.app.core import usecases
from src.app.core.entities import EnvItemEntity
from src.app.infrastructure.exceptions import AppException
from src.app.infrastructure.repositories import CustomersRepository
from src.app.infrastructure.repositories import CitiesRepository
from src.app.infrastructure.repositories import CountriesRepository
from src.app.infrastructure.repositories import CompaniesRepository
from src.app.infrastructure.repositories import EnvironRepository
from src.app.infrastructure.databases import Neo4jDBClient


class BaseController(metaclass=ABCMeta):
    def __init__(self):
        self._env: EnvironRepository = None  # type: ignore
        self._database: Neo4jDBClient = None  # type: ignore
        self._customers: CustomersRepository = None  # type: ignore
        self._countries: CountriesRepository = None  # type: ignore
        self._cities: CitiesRepository = None  # type: ignore
        self._companies: CompaniesRepository = None  # type: ignore

    @property
    def env(self) -> EnvironRepository:
        if self._env is None:
            self._env = EnvironRepository(config.BASE_DIR)
        return self._env

    def _get_env(self, key: str) -> Any:
        item: EnvItemEntity = self.env.get_one(key)  # type: ignore
        if item is None:
            raise AppException(f"Missing environment variable {key}")
        return item.value

    @property
    def database(self) -> Neo4jDBClient:
        if not self._database:
            self._database = Neo4jDBClient(
                self._get_env(config.NEO4J_HOST),
                self._get_env(config.NEO4J_PORT),
                self._get_env(config.NEO4J_USER),
                self._get_env(config.NEO4J_PASSWORD),
            )

        return self._database

    @property
    def customers(self) -> CustomersRepository:
        if self._customers is None:
            self._customers = CustomersRepository(self.database)

        return self._customers

    @property
    def countries(self) -> CountriesRepository:
        if self._countries is None:
            self._countries = CountriesRepository(self.database)

        return self._countries

    @property
    def cities(self) -> CitiesRepository:
        if self._cities is None:
            self._cities = CitiesRepository(self.database)

        return self._cities

    @property
    def companies(self) -> CompaniesRepository:
        if self._companies is None:
            self._companies = CompaniesRepository(self.database)

        return self._companies


class BaseHTTPController(BaseController):
    def __init__(self, request: Request):
        self._request: Request = request
        self._request_headers: Dict = None  # type: ignore
        super().__init__()

    @property
    def request(self) -> Request:
        return self._request

    @property
    def request_headers(self) -> Dict:
        if self._request_headers is None:
            self._request_headers = dict(self._request.headers)
        return self._request_headers


class APIController(BaseHTTPController):

    async def list_customers(self):
        uc = usecases.ListCustomersUseCase(self.customers)
        data = await uc.execute()
        return data

    async def get_customer(self, key: str, condition: str, value: str):
        uc = usecases.GetCustomerUseCase(key, condition, value, self.customers)
        data = await uc.execute()
        return data

    async def list_companies(self):
        uc = usecases.ListCompaniesUseCase(self.companies)
        data = await uc.execute()
        return data

    async def get_companies(self, key: str, condition: str, value: str):
        uc = usecases.GetCompanyUseCase(key, condition, value, self.companies)
        data = await uc.execute()
        return data

    async def list_countries(self):
        uc = usecases.ListCountriesUseCase(self.countries)
        data = await uc.execute()
        return data

    async def get_countries(self, key: str, condition: str, value: str):
        uc = usecases.GetCountryUseCase(key, condition, value, self.countries)
        data = await uc.execute()
        return data

    async def list_cities(self):
        uc = usecases.ListCitiesUseCase(self.cities)
        data = await uc.execute()
        return data

    async def get_cities(self, key: str, condition: str, value: str):
        uc = usecases.GetCityUseCase(key, condition, value, self.cities)
        data = await uc.execute()
        return data

    async def get_graph_view(self):
        uc = usecases.GraphViewUseCase(self.customers)
        data = await uc.execute()
        return data


class CLIController(BaseController):

    async def create_user(self, data: Dict):
        uc = usecases.CreateUserUseCase(data, self.customers)
        await uc.execute()

    async def synchronize(self, data: List[Dict]):
        uc = usecases.SynchronizeUseCase(
                data,
                self.customers,
                self.countries,
                self.cities,
                self.companies)
        await uc.execute()
