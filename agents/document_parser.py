# from agents.base_agent import BaseAgent

# class DocumentParserAgent(BaseAgent):
#     def parse_document(self, text: str):
#         prompt = f"""
#         You are a medical document parser.
#         Extract the following fields from the document:

#         - patient_name
#         - patient_dob
#         - provider_name
#         - date_of_service
#         - diagnoses (ICD-10)
#         - procedures (CPT/HCPCS)
#         - amounts, charges, totals
#         - insurance info

#         Return JSON only.
#         Document:
#         {text}
#         """

#         response = self.ask(prompt)
#         return response
from agents.base_agent import BaseAgent

class DocumentParserAgent(BaseAgent):
    def parse_document(self, text: str):
        prompt = f"""
        Extract fields from the medical document.

        REQUIRED OUTPUT FORMAT:
        {{
            "patient_name": "",
            "patient_dob": "",
            "provider_name": "",
            "date_of_service": "",
            "diagnoses": [],
            "procedures": [],
            "amounts": {{}},
            "insurance_info": {{}}
        }}

        Return *valid JSON only*. No explanations.
        Document: {text}
        """
        return self.ask(prompt)
