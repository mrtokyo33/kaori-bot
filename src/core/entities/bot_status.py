from dataclasses import dataclass

@dataclass(frozen=True)
class BotStatus:
    is_online: bool
    latency: float
    guild_count: int