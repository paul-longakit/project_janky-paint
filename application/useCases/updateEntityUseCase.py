class UpdateEntitiesUseCase:

    def execute(self, entities, delta_time):

        for entity in entities:

            if entity.behavior:
                entity.behavior.update(
                    entity,
                    delta_time,
                )