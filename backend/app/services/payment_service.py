from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from app.database.models import Payment, Customer
from app.core.constants import PaymentStatus, FailureCategory

class PaymentService:
    @staticmethod
    def get_payments(db: Session, status: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[Payment]:
        query = db.query(Payment)
        if status:
            query = query.filter(Payment.status == status)
        return query.order_by(Payment.created_at.desc()).offset(offset).limit(limit).all()

    @staticmethod
    def get_payment(db: Session, payment_id: str) -> Optional[Payment]:
        return db.query(Payment).filter(Payment.id == payment_id).first()

    @staticmethod
    def create_payment(db: Session, payment_data: dict) -> Payment:
        payment = Payment(
            id=payment_data.get("id", f"pay_{uuid.uuid4().hex[:12]}"),
            customer_id=payment_data["customer_id"],
            amount=payment_data["amount"],
            currency=payment_data.get("currency", "INR"),
            method=payment_data.get("method", "card"),
            status=payment_data.get("status", "FAILED"),
            failure_reason=payment_data.get("failure_reason"),
            failure_category=payment_data.get("failure_category"),
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)

        customer = db.query(Customer).filter(Customer.id == payment.customer_id).first()
        if customer:
            failed_payments = getattr(customer, "failed_payments", 0) or 0
            setattr(customer, "failed_payments", failed_payments + 1)
            db.commit()

        return payment

    @staticmethod
    def process_failed_payment_webhook(db: Session, payload: dict) -> Optional[Payment]:
        event = payload.get("event", "")
        if event != "payment.failed":
            return None

        data = payload.get("payload", {}).get("payment", {})
        payment_id = data.get("id", f"pay_{uuid.uuid4().hex[:12]}")

        payment = Payment(
            id=payment_id,
            customer_id=data.get("customer_id", "cust_unknown"),
            amount=data.get("amount", 0),
            currency=data.get("currency", "INR"),
            method=data.get("method", "card"),
            status="FAILED",
            failure_reason=data.get("failure_reason", "UNKNOWN"),
            failure_category=data.get("failure_category", "UNKNOWN"),
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def update_payment_status(db: Session, payment_id: str, status: PaymentStatus | str):
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        if payment:
            normalized_status = PaymentStatus(status) if isinstance(status, str) else status
            payment.status = (
                normalized_status.value
                if isinstance(normalized_status, PaymentStatus)
                else str(normalized_status)
            )
            db.commit()
            db.refresh(payment)
        return payment