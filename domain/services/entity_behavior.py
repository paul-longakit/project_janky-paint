from abc import ABC, abstractmethod

from domain.entities.lore_entity import LoreEntity


class EntityBehavior(ABC):

    @abstractmethod
    def update(self, entity: LoreEntity, delta_time: float) -> None:
        pass