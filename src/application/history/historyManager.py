from copy import deepcopy

from src.application.history.historyEntry import HistoryEntry


class HistoryManager:

    def __init__(
        self,
        max_history: int = 50,
    ):
        self.max_history = max_history

        self.undo_stack: list[HistoryEntry] = []
        self.redo_stack: list[HistoryEntry] = []

    # =============================================================
    # RECORD
    # =============================================================

    def record(
        self,
        before,
        after,
    ) -> None:

        entry = HistoryEntry(
            before=deepcopy(before),
            after=deepcopy(after),
        )

        self.undo_stack.append(entry)

        self.redo_stack.clear()

        if len(self.undo_stack) > self.max_history:
            self.undo_stack.pop(0)

    # =============================================================
    # UNDO
    # =============================================================

    def undo(
        self,
    ):

        if not self.undo_stack:
            return None

        entry = self.undo_stack.pop()

        self.redo_stack.append(
            entry
        )

        return entry.restore_before()

    # =============================================================
    # REDO
    # =============================================================

    def redo(
        self,
    ):

        if not self.redo_stack:
            return None

        entry = self.redo_stack.pop()

        self.undo_stack.append(
            entry
        )

        return entry.restore_after()

    # =============================================================
    # STATE
    # =============================================================

    def can_undo(self) -> bool:

        return bool(
            self.undo_stack
        )

    def can_redo(self) -> bool:

        return bool(
            self.redo_stack
        )

    def clear(self) -> None:

        self.undo_stack.clear()
        self.redo_stack.clear()