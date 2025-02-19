from backend.models import Payment
from backend.repositories import SqlAlchemyRepository


class PaymentRepository(SqlAlchemyRepository):
    model = Payment

    async def create(self, instance: Payment) -> Payment:
        self.session.add(instance)
        await self.session.flush()
        return instance
