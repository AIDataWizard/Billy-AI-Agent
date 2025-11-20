# from agents.base_agent import BaseAgent

# class ComplianceAgent(BaseAgent):
#     def check_compliance(self, parsed_doc):
#         prompt = f"""
#         You are a US healthcare billing compliance auditor.
#         Check:

#         - Modifier rules (26,59,TC,RT,LT)
#         - NCCI bundling edits
#         - Duplicate claims
#         - Payer-specific rules (Medicare/Medicaid/private)
#         - Out-of-network detection
#         - Fraud indicators

#         Return JSON.

#         Document: {parsed_doc}
#         """

#         return self.ask(prompt)

from agents.base_agent import BaseAgent

class ComplianceAgent(BaseAgent):
    def check_compliance(self, payload):
        prompt = f"""
        Run Medicare/Medicaid compliance checks.

        Return JSON only:
        {{
            "modifier_rules": {{}},
            "ncci_bundling_edits": "",
            "payer_specific_rules": {{}},
            "fraud_indicators": "",
            "recommendations": []
        }}

        Payload: {payload}
        """

        return self.ask(prompt)
