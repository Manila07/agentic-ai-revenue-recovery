import importlib
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
for path in (PROJECT_ROOT, os.path.join(PROJECT_ROOT, "src")):
    if os.path.isdir(path) and path not in sys.path:
        sys.path.insert(0, path)

# Import the database layer lazily so the runtime can resolve the module regardless of
# whether the repository is laid out as a flat package or under src/.
try:
    db_module = importlib.import_module("app.database.database")
    seed_module = importlib.import_module("app.database.seed")
except ModuleNotFoundError:  # pragma: no cover - fallback for repos with src/ layout
    db_module = importlib.import_module("src.app.database.database")
    seed_module = importlib.import_module("src.app.database.seed")

Base = db_module.Base
engine = db_module.engine
SessionLocal = db_module.SessionLocal
seed_database = seed_module.seed_database

# Simulate a failed payment flow
from payments.simulator.payment_simulator import PaymentSimulator

# The project may expose the service beneath either the root package or the src package.
# Import lazily so the runtime can resolve the module regardless of the repository layout.
# Avoid static imports for alternate package layouts because VS Code/Pylance may not
# resolve them when the repo is organized under src/.
for module_name in ("app.services.payment_service", "src.app.services.payment_service"):
    try:
        PaymentService = importlib.import_module(module_name).PaymentService
        break
    except ModuleNotFoundError:
        continue
else:
    PaymentService = None

for module_name in ("app.services.recovery_service", "src.app.services.recovery_service"):
    try:
        recovery_service_module = importlib.import_module(module_name)
        RecoveryService = recovery_service_module.RecoveryService
        break
    except ModuleNotFoundError:
        continue
else:
    RecoveryService = None

Base.metadata.create_all(bind=engine)
db = SessionLocal()
sim = PaymentSimulator()
payment_data = sim.generate_failed_transaction()
if PaymentService is None:
    raise RuntimeError("PaymentService could not be imported. Check the project layout or package name.")
payment = PaymentService.create_payment(db, payment_data)
if RecoveryService is not None:
    analysis = RecoveryService.analyze_payment(db, payment)
    print("Analysis:", analysis)
else:
    print("Recovery service unavailable; skipping analysis.")
db.close()