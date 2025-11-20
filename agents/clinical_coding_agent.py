# from agents.base_agent import BaseAgent

# class ClinicalCodingAgent(BaseAgent):
#     def validate_codes(self, icd_list, cpt_list):
#         prompt = f"""
#         You are a medical coding expert.
#         Validate ICD-10 and CPT/HCPCS pairings.
#         Identify:

#         - invalid pairings
#         - missing codes
#         - missing modifiers
#         - upcoding / unbundling
#         - recommended corrections

#         Return JSON.

#         ICD codes: {icd_list}
#         CPT codes: {cpt_list}
#         """

#         return self.ask(prompt)

from agents.base_agent import BaseAgent

class ClinicalCodingAgent(BaseAgent):
    def validate_codes(self, icd_list, cpt_list):
        prompt = f"""
        Validate ICD-10 and CPT pairings.

        Return JSON only:
        {{
            "pairing_validity": "",
            "invalid_pairings": [],
            "missing_modifiers": [],
            "missing_codes": [],
            "recommended_corrections": []
        }}

        ICD: {icd_list}
        CPT: {cpt_list}
        """

        return self.ask(prompt)
