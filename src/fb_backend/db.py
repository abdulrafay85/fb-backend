from dataclasses import dataclass, field
from typing import Any, List
import time
from datetime import datetime

@dataclass
class BufferItem:
    data: Any
    user_id: str
    run_id: str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d%H:%M:%S"))

@dataclass
class ShortTermMemory:
    buffer: List[BufferItem] = field(default_factory=list)

    def add_memory(self, data: Any, *, user_id: str, run_id: str) -> None:
        item = BufferItem(data=data, user_id=user_id, run_id=run_id)
        self.buffer.append(item)

    def get_memory(self, user_id: str) -> List[BufferItem]:
        """Return all BufferItems for the given user_id."""
        return [item for item in self.buffer if item.user_id == user_id]

