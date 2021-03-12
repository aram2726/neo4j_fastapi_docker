from abc import ABCMeta
from abc import abstractmethod
from typing import Dict
from typing import List

from neo4j import GraphDatabase

from src.app.infrastructure.filters import CONDITIONS_MAP


class AbstractBaseDBClient(metaclass=ABCMeta):

    @property
    @abstractmethod
    def connection(self):
        raise NotImplementedError

    @abstractmethod
    async def select_all(self, node: str, limit: int = None, after: int = None) -> List:
        raise NotImplementedError

    @abstractmethod
    async def filter(self, node: str, key: str, condition: str, value: str) -> List:
        raise NotImplementedError

    @abstractmethod
    async def insert(self, node: str, data: dict):
        raise NotImplementedError


class Neo4jDBClient(AbstractBaseDBClient):

    def __init__(self, host: str, port: int, username: str, password: str):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._connection = None

    @property
    def connection(self):
        if not self._connection:
            uri = f"{self._host}:{self._port}"
            self._connection = GraphDatabase.driver(
                uri=uri, auth=(self._username, self._password))
        return self._connection

    def close(self):
        self._connection.close()

    async def select_all(self, node: str, limit: int = None, after: int = None):
        with self.connection.session() as session:
            result = session.read_transaction(self._find_all, node)
        self.close()
        return result

    async def filter(self, node: str, key: str, condition: str, value: str) -> List:
        with self.connection.session() as session:
            result = session.read_transaction(self._filter, node, key, condition, value)
        self.close()
        return result

    async def insert(self, node: str, data: dict):
        with self.connection.session() as session:
            session.write_transaction(self._create, node, data)
        self.close()

    async def graph_view(self):
        with self.connection.session() as session:
            result = session.read_transaction(self._get_graph)
        self.close()
        return result

    async def update(self, uuid: str, data: dict):
        pass

    async def delete(self, uuid: str):
        pass

    async def create_relation(self, node_1: str, relation: str, node_2: str, where: Dict):
        with self.connection.session() as session:
            session.write_transaction(self._create_relation, node_1, relation, node_2, where)
        self.close()

    @staticmethod
    def _create_relation(tx, node_1: str, relation: str, node_2: str, where: Dict):
        query = f"""
        MATCH ({node_1[0].lower()}1:{node_1.capitalize()}), ({node_2[0].lower()}2:{node_2.capitalize()})
        WHERE {node_1[0].lower()}1.{where["key"]} {where["condition"]} {node_2[0].lower()}2.{where["value"]}
        CREATE ({node_1[0].lower()}1)-[r:{relation.upper()}]->({node_2[0].lower()}2)
        """
        result = tx.run(query)
        return result

    @staticmethod
    def _create(tx, node_name: str, data: dict):
        k_v_pairs = [f"{key}: ${key}" for key in data.keys()]
        values = []
        for pair in k_v_pairs:
            values.append(f"{pair}")
        query = f"""
        CREATE ({node_name[0].lower()}:{node_name.capitalize()}
        { {" ,".join(values)} } 
        ) RETURN {node_name[0].lower()}""".replace("'", "")
        result = tx.run(query, **data)
        return result

    @staticmethod
    def _find_all(tx, node_name: str):
        query = (
            f"MATCH ({node_name[0].lower()}:{node_name.capitalize()}) RETURN {node_name[0].lower()}"
        )
        result = tx.run(query)
        return [record for record in result]

    @staticmethod
    def _filter(tx, node_name: str, key: str, condition: str, value: str):
        condition_val = CONDITIONS_MAP.get(condition, "=")
        query = (
            f"MATCH ({node_name[0].lower()}:{node_name.capitalize()}) "
            f"WHERE {node_name[0].lower()}.{key} {condition_val} ${key} "
            f"RETURN {node_name[0].lower()}"
        )
        result = tx.run(query, **{key: value})
        return [record for record in result]

    @staticmethod
    def _get_graph(tx):
        query = "MATCH (c1:Country), (c2:City), (c3:Customer), (c4:Company) RETURN c1, c2, c3, c4"
        result = tx.run(query)
        return [record for record in result]
