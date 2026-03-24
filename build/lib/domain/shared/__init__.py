"""共享内核模块"""
from .events.domain_event import DomainEvent
from .value_objects.result import Result
from .value_objects.timestamp import Timestamp

__all__ = ["DomainEvent", "Result", "Timestamp"]
