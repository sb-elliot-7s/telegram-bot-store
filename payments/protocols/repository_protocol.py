from abc import ABC, abstractmethod

from schemas import PaymentResponseSchema


class PaymentsRepositoryProtocol(ABC):
    @abstractmethod
    async def save_payments_data(self, payment_data: PaymentResponseSchema):
        pass
