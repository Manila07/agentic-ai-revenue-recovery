# Architecture Decisions

## ADR-001: Use FastAPI for Backend
- Status: Accepted
- Context: Need high-performance API with async support
- Decision: Use FastAPI

## ADR-002: Use RandomForest for Initial ML Model
- Status: Accepted
- Context: Need interpretable model for recovery prediction
- Decision: Use RandomForest, can later upgrade to XGBoost

## ADR-003: Use Tool-Calling Pattern for Agent
- Status: Accepted
- Context: LLM should not directly call APIs
- Decision: Agent selects from predefined tools