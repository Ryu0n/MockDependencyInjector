import abc
import random
import dataclasses
from typing import List
from dependency_injector import containers, providers


class AbstractCacheClient(metaclass=abc.ABCMeta):
    ...


@dataclasses.dataclass
class RedisCacheClient(AbstractCacheClient):
    host: str
    port: int
    db: int


@dataclasses.dataclass
class MemcachedCacheClient(AbstractCacheClient):
    hosts: List[str]
    port: int
    prefix: str


@dataclasses.dataclass
class Service:
    cache: AbstractCacheClient


class Container(containers.DeclarativeContainer):
    cache_client_factory = providers.AbstractFactory(AbstractCacheClient)
    
    service_factory = providers.Factory(
        Service,
        cache=cache_client_factory
    )


if __name__ == "__main__":
    container = Container()
    
    cache_type = random.choice(["redis", "memcached"])
    
    if cache_type == "redis":
        container.cache_client_factory.override(
            providers.Factory(
                RedisCacheClient,
                host="localhost",
                port=6379,
                db=0
            )
        )
    elif cache_type == "memcached":
        container.cache_client_factory.override(
            providers.Factory(
                MemcachedCacheClient,
                hosts=["10.0.0.1"],
                port=11211,
                prefix="my_app"
            )
        )
    
    service = container.service_factory()
    print(service.cache)