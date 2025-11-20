from agents.base_agent import BaseAgent

class ComplianceAgent(BaseAgent):
    def check_compliance(self, parsed_doc):
        prompt = f"""
        You are a US healthcare billing compliance auditor.
        Check:

        - Modifier rules (26,59,TC,RT,LT)
        - NCCI bundling edits
        - Duplicate claims
        - Payer-specific rules (Medicare/Medicaid/private)
        - Out-of-network detection
        - Fraud indicators

        Return JSON.

        Document: {parsed_doc}
        """

        return self.ask(prompt)
