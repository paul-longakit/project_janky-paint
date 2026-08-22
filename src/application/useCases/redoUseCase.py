from src.application.history.historyManager import HistoryManager


class RedoUseCase:

    def execute(
        self,
        paint,
        history: HistoryManager,
    ) -> bool:

        snapshot = history.redo()

        if snapshot is None:
            return False

        paint.__dict__.clear()

        paint.__dict__.update(
            snapshot.__dict__
        )

        return True