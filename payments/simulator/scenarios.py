from payments.simulator.failure_generator import FailureGenerator

class ScenarioRunner:
    def __init__(self):
        self.generator = FailureGenerator()

    def run(self, scenario: str):
        return self.generator.generate(scenario)