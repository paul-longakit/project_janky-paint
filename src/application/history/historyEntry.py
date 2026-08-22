from dataclasses import dataclass
from copy import deepcopy


@dataclass
class HistoryEntry:

    before: object
    after: object

    def restore_before(self) -> object:
        return deepcopy(self.before)

    def restore_after(self) -> object:
        return deepcopy(self.after)