from agents.base_agent import BaseAgent

class MedicalNecessityAgent(BaseAgent):
    def check_necessity(self, clinical_text, diagnoses, procedures):
        prompt = f"""
        You are a Medicare medical necessity checker.
        Evaluate if the clinical evidence supports the billed procedures.

        Return:
        - is_medically_necessary: yes/no
        - missing documentation
        - required additional chart notes
        - justification summary

        Clinical Notes: {clinical_text}
        Diagnoses: {diagnoses}
        Procedures: {procedures}
        """

        return self.ask(prompt)
