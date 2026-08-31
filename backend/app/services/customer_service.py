from sqlalchemy.orm import Session
from typing import Optional
from app.database.models import Customer

class CustomerService:
    @staticmethod
    def get_customer(db: Session, customer_id: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.id == customer_id).first()

    @staticmethod
    def create_customer(db: Session, customer_data: dict) -> Customer:
        customer = Customer(
            id=customer_data["id"],
            email=customer_data["email"],
            name=customer_data["name"],
            segment=customer_data.get("segment", "standard"),
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer