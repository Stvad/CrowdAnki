from dataclasses import dataclass
from typing import Any, Callable

from anki import hooks


@dataclass
class AnkiHookManager:
    hooks: Any = hooks

    def hook(self, hook_name: str, handler: Callable):
        self.hooks.addHook(hook_name, handler)

    def unhook(self, hook_name: str, handler: Callable):
        self.hooks.remHook(hook_name, handler)
