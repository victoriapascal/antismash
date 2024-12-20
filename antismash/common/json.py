# License: GNU Affero General Public License v3 or later
# A copy of GNU AGPL v3 should have been included in this software package in LICENSE.txt.

""" JSON-friendly classes explicitly for use by the javascript drawing libraries
"""

from dataclasses import dataclass, field
from typing import Any, Iterator, List, Tuple, IO, Union, Dict, Callable

from antismash.common.secmet.features import CDSFeature
from antismash.common.secmet.qualifiers import NRPSPKSQualifier
from antismash.common.secmet.record import Seq
from orjson import (
    loads,  # pylint: disable=unused-import  # used by others
    OPT_NON_STR_KEYS as _OPT_CONVERT_NON_STR_KEYS,
    OPT_SORT_KEYS as _OPT_SORT_KEYS,
    OPT_INDENT_2 as _OPT_INDENT_2,
    dumps as _dumps,
)


JSONBase = Union[int, float, str, bool, None]
JSONCompatible = Union[
    Dict[str, Union["JSONCompatible"]],
    List["JSONCompatible"],
    Tuple["JSONCompatible"],
    JSONBase
]


def _base_convertor(obj: Any) -> Any:
    # handles any conversion methods for classes that aren't default types or dataclasses
    if isinstance(obj, Seq):
        return str(obj)
    if hasattr(obj, "to_json"):
        return obj.to_json()
    if hasattr(obj, "__json__"):
        return obj.__json__()
    # but if no conversion method is found, then an error must be raised for orjson (and stdlib json, for that matter)
    raise TypeError


def _convert_std_to_orson(*, sort_keys: bool = False, option: int = 0, indent: bool = True) -> int:
    # always match stdlib JSON's default behaviour, where non-string keys are converted to string
    option |= _OPT_CONVERT_NON_STR_KEYS
    if sort_keys:
        option |= _OPT_SORT_KEYS
    if indent:
        option |= _OPT_INDENT_2
    return option


def dumps(obj: Any, *, default: Callable[[Any], Any] = _base_convertor, indent: bool = False,
          sort_keys: bool = False, option: int = 0,
          ) -> str:
    """ Converts the given object to a JSON string

        Arguments:
            obj: the object to convert
            default: an optional override of the usual class convertor handler for non-standard types
            indent: a boolean indicating whether to use indents in the string conversion (always 2 spaces if used)
            sort_keys: whether the child attributes should be sorted by key
            option: an orjson option value (see orjson documentation for possible values)

        Returns:
            the string generated
    """
    option = _convert_std_to_orson(indent=indent, sort_keys=sort_keys, option=option)
    return _dumps(obj, default=default, option=option).decode()


def load(handle: IO) -> dict[str, Any]:
    """ Reads in JSON text from the given file handle and returns the information using
        standard types.

        Arguments:
            handle: the file handle to read from

        Returns:
            a dictionary mapping loaded key-value pairs
    """
    return loads(handle.read())


class JSONBase(dict):
    """ A base class for JSON-serialisable objects """
    def __init__(self, keys: List[str]) -> None:
        super().__init__()
        self._keys = keys

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def items(self) -> Iterator[Tuple[str, Any]]:  # type: ignore
        for key in self._keys:
            yield (key, getattr(self, key))

    def values(self) -> Iterator[Any]:  # type: ignore
        for key in self._keys:
            yield getattr(self, key)

    def __len__(self) -> int:
        return len(self._keys)


class JSONDomain(JSONBase):
    """ A JSON-serialisable object for simplifying domain datatypes throughout this file """
    def __init__(self, domain: NRPSPKSQualifier.Domain, predictions: List[Tuple[str, str]], napdos_link: str,
                 blast_link: str, sequence: str, dna: str) -> None:
        super().__init__(['type', 'start', 'end', 'predictions', 'napdoslink',
                          'blastlink', 'sequence', 'dna_sequence'])
        self.type = str(domain.name)
        self.start = int(domain.start)
        self.end = int(domain.end)
        self.predictions = predictions
        self.napdoslink = str(napdos_link)
        self.blastlink = str(blast_link)
        self.sequence = str(sequence)
        self.dna_sequence = str(dna)


class JSONOrf(JSONBase):
    """ A JSON-serialisable object for simplifying ORF datatypes throughout this file """
    def __init__(self, feature: CDSFeature) -> None:
        super().__init__(['id', 'sequence', 'domains'])
        self.sequence = feature.translation
        self.id = feature.get_name()
        self.domains = []  # type: List[JSONDomain]

    def add_domain(self, domain: JSONDomain) -> None:
        """ Add a JSONDomain to the list of domains in this ORF """
        assert isinstance(domain, JSONDomain)
        self.domains.append(domain)
