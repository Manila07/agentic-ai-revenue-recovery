import random
from typing import List, Dict

class TransactionGenerator:
    def generate_batch(self, n: int = 100) -> List[Dict]:
        from payments.simulator.payment_simulator import PaymentSimulator
        simulator = PaymentSimulator()
        transactions = []
        for _ in range(n):
            if random.random() < 0.7:
                transactions.append(simulator.generate_failed_transaction())
            else:
                transactions.append(simulator.generate_successful_transaction())
        return transactions