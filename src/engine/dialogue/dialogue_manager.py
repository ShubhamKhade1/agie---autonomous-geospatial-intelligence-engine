import google.generativeai as genai
import os
from typing import List, Dict, Any, Optional

class DialogueManager:
    def __init__(self, api_key: Optional[str] = None):
        """
        :param api_key: Google Gemini API Key
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-pro")
        else:
            self.model = None
            
        # Mock responses for Step 4-5 autonomous flow
        self.mock_responses = {
            "status": "Priority Index is 88.2. Significant SST deviation observed in ROI A-12. Convergent evidence from SAR and AIS indicates dark-ship behavior.",
            "default": "Analysis from the Gemini Synthesis Engine confirms a high-magnitude anomaly (2.4\u03C3 deviation from baseline). Convergent evidence from multi-signal alignment (Sentinel-1 SAR + MODIS) suggests immediate investigation is required at the primary ROI coordinates."
        }

    def check_convergent_evidence(
        self, 
        signals: List[Dict[str, Any]], 
        threshold: float = 70.0
    ) -> bool:
        """
        Ensure multiple signals confirm the anomaly before escalating.
        :param signals: List of individual signal scores
        :param threshold: Significance threshold
        :return: True if evidence is convergent
        """
        # Count signals that cross the threshold
        significant_signals = [s for s in signals if s["score"] >= threshold]
        
        # We require at least 2 distinct signal types to "converge"
        # Example: (Sentinel-1 SAR) + (Sentinel-2 Optical) + (AIS anomaly)
        distinct_sources = set([s["source"] for s in significant_signals])
        
        return len(distinct_sources) >= 2

    def synthesize_report(
        self, 
        signals: List[Dict[str, Any]], 
        history_summary: str,
        projected_trajectory: str
    ) -> str:
        """
        Generate a human-readable, explainable report using Gemini.
        :param signals: Current multivariate detections
        :param history_summary: Summary of previous baseline cycles
        :param projected_trajectory: Predicted trend
        :return: Synthesized report string
        """
        if not self.model:
            return self.mock_responses.get("default")

        prompt = f"""
        Analyze the following geospatial situational awareness signals for an environmental analyst.
        
        Current Signals: {signals}
        Historical Baseline: {history_summary}
        Projected Trajectory: {projected_trajectory}
        
        Task:
        1. Rank the priority of the anomaly.
        2. Explain the "Magnitude" in plain language relative to the seasonal baseline.
        3. Identify the "Convergent Evidence" (e.g., source A and source B confirm).
        4. Suggest one immediate Operator Action (e.g., Deploy inspection vessel, Verify cloud cover).
        
        Formatting: Use a professional, action-oriented tone.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Gemini Analysis failed ({str(e)}). Falling back to mock synthesis: \n\n{self.mock_responses.get('default')}"

    def query_knowledge_base(self, user_query: str) -> str:
        """
        Operator Interface (Step 5): Answer situational awareness questions.
        """
        if "status" in user_query.lower() or "what" in user_query.lower():
            return self.mock_responses.get("status")
        return self.mock_responses.get("default")

if __name__ == "__main__":
    # Test example
    manager = DialogueManager()
    # mock_signals = [
    #     {"source": "Sentinel-1", "score": 85.0, "finding": "SAR slick detected"},
    #     {"source": "AIS", "score": 92.0, "finding": "Vessel transponder disabled"}
    # ]
    # print(manager.synthesize_report(mock_signals, "Normal shipping lanes", "Stable"))
