from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class PwnResult:
    service: str
    status: str  # "Pwned", "Read-Only", "Denied"
    summary: str
    can_escalate: bool = False
    metadata: Dict = field(default_factory=dict)
