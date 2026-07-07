"""Core wrapping machinery shared by all rhapsody_cli element wrappers.

``call_com`` translates COM failures into ``RhapsodyRuntimeException``.
``RPModelElement`` is the base class for every wrapped Rhapsody model
element, mirroring ``com.telelogic.rhapsody.core.IRPModelElement``.
``wrap()`` (added in Task 5) dispatches a raw COM object to its matching
wrapper class using a registry populated by each element module.
"""

from __future__ import annotations

from typing import Any, Callable, Iterator, TypeVar

from rhapsody_cli.exceptions import RhapsodyRuntimeException

try:
    import pywintypes
except ImportError:  # pragma: no cover - pywintypes is Windows-only
    pywintypes = None

T = TypeVar("T")

#: Maps a Rhapsody ``getMetaClass()`` string (e.g. "Class", "Package") to the
#: wrapper class that should represent it. Populated by each element module
#: at import time via ``register_wrapper``. Unmapped meta classes fall back
#: to ``RPModelElement`` in ``wrap()`` (Task 5).
_WRAPPER_REGISTRY: dict[str, type[RPModelElement]] = {}


def register_wrapper(meta_class: str, wrapper_cls: type[RPModelElement]) -> None:
    """Register ``wrapper_cls`` as the wrapper for COM objects of ``meta_class``."""
    _WRAPPER_REGISTRY[meta_class] = wrapper_cls


def call_com(func: Callable[[], T]) -> T:
    """Invoke a COM call, translating COM errors into RhapsodyRuntimeException."""
    try:
        return func()
    except Exception as exc:
        # pywintypes is Windows-only; on other platforms there is no live COM
        # connection so a com_error cannot occur here.
        if pywintypes is not None and isinstance(exc, pywintypes.com_error):
            raise RhapsodyRuntimeException(str(exc)) from exc
        raise


def _wrap_if_element(value: Any) -> Any:
    """Wrap ``value`` if it looks like a Rhapsody model element."""
    if hasattr(value, "getMetaClass") or hasattr(value, "metaClass"):
        return wrap(value)
    return value


def wrap(com_obj: Any) -> RPModelElement:
    """Wrap a raw Rhapsody COM model element in its matching wrapper class."""
    meta_class = str(_get_method_or_property(com_obj, "getMetaClass", "metaClass"))
    wrapper_cls = _WRAPPER_REGISTRY.get(meta_class, RPModelElement)
    return wrapper_cls(com_obj)


def _get_method_or_property(com_obj: Any, method_name: str, prop_name: str) -> Any:
    """Read a value from ``com_obj``, preferring the Java-style method.

    Some Rhapsody COM automation Prog IDs (e.g. the Java-mirroring
    ``Rhapsody.Application``) expose model element attributes as methods
    (``getName()``, ``getGUID()``, ...), while others (e.g.
    ``Rhapsody2.Application.1``) expose the same data as bare COM
    properties (``name``, ``GUID``, ...). Prefer the method when present,
    and fall back to the bare property otherwise.
    """
    if hasattr(com_obj, method_name):
        return call_com(lambda: getattr(com_obj, method_name)())
    return call_com(lambda: getattr(com_obj, prop_name))


def _set_method_or_property(com_obj: Any, method_name: str, prop_name: str, value: Any) -> None:
    """Write a value to ``com_obj``, preferring the Java-style setter method.

    See :func:`_get_method_or_property` for why both forms exist.
    """
    if hasattr(com_obj, method_name):
        call_com(lambda: getattr(com_obj, method_name)(value))
    else:
        call_com(lambda: setattr(com_obj, prop_name, value))


class RPModelElement:
    """Wraps ``IRPModelElement``: the base interface for all model elements.

    Method names mirror the Rhapsody Java API exactly (``getName``,
    ``setName``, ``getMetaClass``, ``getGUID``, ...). Some Rhapsody COM Prog
    IDs expose these as bare properties instead of methods; see
    :func:`_get_method_or_property`.
    """

    def __init__(self, com_obj: Any) -> None:
        self._com = com_obj

    def getName(self) -> str:
        return str(_get_method_or_property(self._com, "getName", "name"))

    def setName(self, name: str) -> None:
        _set_method_or_property(self._com, "setName", "name", name)

    def getMetaClass(self) -> str:
        return str(_get_method_or_property(self._com, "getMetaClass", "metaClass"))

    def getGUID(self) -> str:
        return str(_get_method_or_property(self._com, "getGUID", "GUID"))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RPModelElement):
            return NotImplemented
        return bool(self._com == other._com)

    def __hash__(self) -> int:
        return hash(id(self._com))

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.getName()!r})"


class RPUnit(RPModelElement):
    """Wraps ``IRPUnit``: model elements that can be saved as separate files."""

    def save(self) -> None:
        call_com(lambda: self._com.save())

    def getFilename(self) -> str:
        return str(_get_method_or_property(self._com, "getFilename", "filename"))

    def setFilename(self, filename: str) -> None:
        _set_method_or_property(self._com, "setFilename", "filename", filename)

    def isReadOnly(self) -> bool:
        return call_com(lambda: bool(self._com.isReadOnly()))

    def setReadOnly(self, read_only: bool) -> None:
        call_com(lambda: self._com.setReadOnly(1 if read_only else 0))


class RPCollection:
    """Wraps ``IRPCollection``: an iterable/indexable container of elements."""

    def __init__(self, com_obj: Any) -> None:
        self._com = com_obj

    def getCount(self) -> int:
        return int(_get_method_or_property(self._com, "getCount", "Count"))

    def getItem(self, index: int) -> Any:
        if hasattr(self._com, "getItem"):
            raw_item = call_com(lambda: self._com.getItem(index))
        else:
            raw_item = call_com(lambda: self._com.Item(index))
        return _wrap_if_element(raw_item)

    def addItem(self, element: RPModelElement) -> None:
        call_com(lambda: self._com.addItem(element._com))

    def __len__(self) -> int:
        return self.getCount()

    def __getitem__(self, index: int) -> Any:
        if index < 0:
            raise IndexError("negative indices are not supported")
        return self.getItem(index + 1)

    def __iter__(self) -> Iterator[Any]:
        for index in range(1, len(self) + 1):
            yield self.getItem(index)
