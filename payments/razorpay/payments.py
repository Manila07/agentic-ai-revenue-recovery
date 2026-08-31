from typing import Any, cast

from payments.razorpay.client import RazorpayClient


class PaymentAPI:
    def __init__(self):
        self.client: Any = cast(Any, RazorpayClient())

    async def get_payment(self, payment_id: str):
        return await cast(Any, self.client).get_payment(payment_id)

    async def retry_payment(self, payment_id: str):
        return await cast(Any, self.client).retry_payment(payment_id)