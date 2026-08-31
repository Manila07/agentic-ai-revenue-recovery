class MockCustomerAPI:
    def get_customer(self, customer_id: str):
        return {"customer_id": customer_id, "name": "John Doe", "segment": "standard"}