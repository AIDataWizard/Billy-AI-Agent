from agents.base_agent import BaseAgent

class MedicalNecessityAgent(BaseAgent):
    def check_necessity(self, clinical_text, diagnoses, procedures):
        prompt = f"""
        Evaluate medical necessity.

        Return valid JSON only:
        {{
            "is_medically_necessary": "",
            "missing_documentation": [],
            "required_additional_notes": [],
            "justification_summary": ""
        }}

        Clinical Notes: {clinical_text}
        Diagnoses: {diagnoses}
        Procedures: {procedures}
        """

        return self.ask(prompt)
