from dataclasses import dataclass, field
from typing import Any, Generic, List, Mapping, Optional, Protocol, TypeVar

from solr_manager.parameters import unparse_params
from solr_manager.utils import decamelize_keys

_ResponseType = TypeVar("_ResponseType", bound=Mapping[str, Any])


@dataclass(kw_only=True)
class SolrResponseHeader:
    q_time: int
    status: int
    zk_connected: bool

    #: The params that were sent to the request in python format
    params: Mapping[str, Any]

    #: The params that were sent to the request in solr format
    raw_params: Mapping[str, Any] = field(init=False)

    def __post_init__(self):
        self.raw_params = self.params
        self.params = unparse_params(self.params)


@dataclass(frozen=True)
class SolrResponseError:
    msg: str
    code: int
    metadata: List[str]


class SolrResponseProtocol(Protocol, Generic[_ResponseType]):
    raw: Mapping[str, Any]
    docs: List[_ResponseType]
    start: int
    num_found: int
    max_score: float

    error: Optional[SolrResponseError] = None
    header: Optional[SolrResponseHeader] = None


class SolrResponse(SolrResponseProtocol[_ResponseType]):
    def __init__(self, response: Mapping[str, Any]) -> None:
        self.raw = response
        self._response = decamelize_keys(response.get("response", {}))

        self.header = response.get("responseHeader")
        if self.header:
            self.header = SolrResponseHeader(**decamelize_keys(self.header))

        self.error = response.get("error")
        if self.error:
            self.error = SolrResponseError(**self.error)

    def __getattr__(self, name):
        if name not in self._response.keys():
            raise AttributeError(f"Response object has no attribute {name}")

        return self._response[name]
