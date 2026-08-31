from payments.simulator.transaction_generator import TransactionGenerator

if __name__ == "__main__":
    gen = TransactionGenerator()
    transactions = gen.generate_batch(100)
    print(f"Generated {len(transactions)} transactions")