from dataclasses import dataclass

from motor.motor_asyncio import AsyncIOMotorCollection

from protocols.repository_protocol import PaymentsRepositoryProtocol
from schemas import PaymentResponseSchema


@dataclass
class PaymentsRepository(PaymentsRepositoryProtocol):
    payment_collection: AsyncIOMotorCollection

    async def save_payments_data(self, payment_data: PaymentResponseSchema):
        await self.payment_collection.insert_one(document=payment_data.dict(exclude_none=True))
