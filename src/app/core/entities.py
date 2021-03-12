from abc import ABCMeta


class BaseEntity(metaclass=ABCMeta):
    def __init__(self, uuid=None):
        self._uuid = uuid

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        self._uuid = uuid


class ItemEntity(BaseEntity, metaclass=ABCMeta):
    def __init__(self, uuid=None, val=None):
        super().__init__(uuid)

        self._val = val

    @property
    def value(self):
        return self._val

    @value.setter
    def value(self, value):
        self._val = value


class EnvItemEntity(ItemEntity):
    pass


class LocationEntity(BaseEntity):

    def __init__(self, uuid: str = None, country: str = None):
        super().__init__(uuid)
        self._country = country

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country: str):
        self._country = country


class CompanyEntity(BaseEntity):
    def __init__(self, uuid: str = None, company: str = None):
        super().__init__(uuid)
        self._company = company

    @property
    def company(self):
        return self._company

    @company.setter
    def country(self, company: str):
        self._company = company


class CustomerEntity(BaseEntity):
    pass
