from domain.entities.lore_entity import LoreEntity
from domain.services.entity_behavior import EntityBehavior


class JankySlideRight(EntityBehavior):

    def update(
        self,
        entity: LoreEntity,
        delta_time: float
    ) -> None:

        entity.x += 180 * delta_time

        if entity.x > 850:
            entity.x = -100