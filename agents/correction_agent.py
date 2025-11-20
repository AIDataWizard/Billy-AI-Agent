from agents.base_agent import BaseAgent

class CorrectionAgent(BaseAgent):
    def correct(self, parsed_doc):
        prompt = f"""
        You are a billing correction agent.
        Produce corrected claim fields including:

        - corrected ICD-10
        - corrected CPT
        - correct modifiers
        - fixed insurance info
        - corrected totals
        - corrected PDF fields (JSON)

        Also generate:
        - an appeal justification paragraph

        Document: {parsed_doc}
        """

        return self.ask(prompt)