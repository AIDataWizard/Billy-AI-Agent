from agents.base_agent import BaseAgent

class DenialPredictorAgent(BaseAgent):
    def predict(self, parsed_doc):
        prompt = f"""
        You are a claim denial prediction system.
        Predict:
        - denial_likelihood (0-100%)
        - reasons for denial
        - fields causing the risk
        - what to fix

        Return JSON.
        Document: {parsed_doc}
        """

        return self.ask(prompt)
