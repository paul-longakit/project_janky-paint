from abc import ABC, abstractmethod

from src.domain.entities.jankyEntity import LoreEntity


class EntityBehavior(ABC):

    @abstractmethod
    def update(self, entity: LoreEntity, delta_time: float) -> None:
        pass