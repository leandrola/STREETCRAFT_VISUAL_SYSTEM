"""In-memory, append-only simulation log. Every real execution quota is zero."""
from dataclasses import dataclass
from types import MappingProxyType


class LedgerError(ValueError):
    """Invalid static reservation or transition."""


@dataclass(frozen=True)
class Entry:
    reservation_id: str
    status: str
    units: tuple
    reason: str
    static_only: bool = True


class Ledger:
    """No configurable positive budget, persistence, dispatch or retry path."""
    @property
    def caps(self):
        return MappingProxyType({"model_calls": 0, "attempts": 0, "images": 0,
                                 "training_steps": 0, "spend": 0})

    def __init__(self):
        self._events = []

    @property
    def events(self):
        return tuple(self._events)

    def reserve(self, reservation_id, units):
        if type(reservation_id) is not str or not reservation_id.strip():
            raise LedgerError("Reservation ID required")
        if any(e.reservation_id == reservation_id for e in self._events):
            raise LedgerError("ID already used; retry forbidden")
        if type(units) is not dict or set(units) != set(self.caps):
            raise LedgerError("Exact reservation units required")
        if any(type(v) is not int or v != 0 for v in units.values()):
            raise LedgerError("Zero cap exceeded or invalid unit")
        entry = Entry(reservation_id, "RESERVED_STATIC", tuple(sorted(units.items())), "")
        self._events.append(entry)
        return entry

    def fail(self, reservation_id, reason):
        previous = [e for e in self._events if e.reservation_id == reservation_id]
        if not previous or previous[-1].status != "RESERVED_STATIC":
            raise LedgerError("Only an existing static reservation may fail once")
        if type(reason) is not str or not reason.strip():
            raise LedgerError("Failure reason required")
        entry = Entry(reservation_id, "FAILED_STATIC", previous[-1].units, reason)
        self._events.append(entry)
        return entry
