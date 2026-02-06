"""
Gemini API Client for CXR Analysis
Handles all interactions with Google's Gemini Vision API
"""

import google.generativeai as genai
import streamlit as st
from typing import Optional, Dict, Any
import io
from PIL import Image

class GeminiClient:
    """Client for interacting with Google Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client
        
        Args:
            api_key: Google Gemini API key. If None, will try to get from secrets
        """
        if api_key is None:
            try:
                api_key = st.secrets["GEMINI_API_KEY"]
            except Exception:
                raise ValueError(
                    "GEMINI_API_KEY not found. Please set it in .streamlit/secrets.toml"
                )
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def analyze_image(
        self, 
        image: Image.Image, 
        prompt: str,
        temperature: float = 0.4,
        max_tokens: int = 2048
    ) -> str:
        """
        Analyze a chest X-ray image with a custom prompt
        
        Args:
            image: PIL Image object of the chest X-ray
            prompt: Analysis prompt for Gemini
            temperature: Model temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            
        Returns:
            Analysis text from Gemini
        """
        try:
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }
            
            response = self.model.generate_content(
                [prompt, image],
                generation_config=generation_config
            )
            
            return response.text
        
        except Exception as e:
            raise Exception(f"Error analyzing image: {str(e)}")
    
    def analyze_technical_quality(self, image: Image.Image) -> Dict[str, Any]:
        """
        Analyze technical quality of chest X-ray
        
        Args:
            image: PIL Image of chest X-ray
            
        Returns:
            Dictionary with technical quality assessment
        """
        prompt = """
        You are an expert radiologist evaluating the technical quality of a chest X-ray.
        
        Please assess the following technical parameters:
        
        1. POSITIONING:
           - Is the patient properly centered?
           - Are spinous processes midline between clavicular heads?
           - Are scapulae adequately rotated laterally?
           - Rate: Excellent/Good/Fair/Poor
        
        2. PENETRATION:
           - Are vertebral bodies faintly visible through the mediastinum?
           - Are lung fields appropriately gray (not too dark or light)?
           - Can you see vascular markings clearly?
           - Rate: Excellent/Good/Fair/Poor
        
        3. INSPIRATION:
           - Is the right hemidiaphragm at the 6th anterior rib?
           - Or at the 10th posterior rib at mid-clavicular line?
           - Is there adequate lung expansion?
           - Rate: Excellent/Good/Fair/Poor
        
        4. MOTION:
           - Are rib cortices sharp?
           - Are vessel margins well-defined?
           - Are diaphragm contours sharp?
           - Rate: Excellent/Good/Fair/Poor
        
        Provide your assessment in a structured format with overall quality rating and 
        specific recommendations for improvement if needed.
        """
        
        response = self.analyze_image(image, prompt)
        return {"raw_analysis": response}
    
    def analyze_anatomy_systematic(self, image: Image.Image, region: str) -> str:
        """
        Perform systematic anatomic analysis of specific region
        
        Args:
            image: PIL Image of chest X-ray
            region: Anatomic region to analyze
            
        Returns:
            Analysis text for the specified region
        """
        prompts = {
            "chest_wall": """
            Analyze the CHEST WALL on this chest X-ray:
            - Rib integrity (fractures, lesions)
            - Soft tissue abnormalities
            - Breast shadows (if visible)
            - Subcutaneous emphysema
            - Surgical clips or hardware
            Provide detailed findings.
            """,
            
            "mediastinum": """
            Analyze the MEDIASTINUM on this chest X-ray:
            - Heart size (cardiothoracic ratio)
            - Heart borders and contours
            - Aortic arch contour
            - Mediastinal width
            - Tracheal position
            - Any masses or widening
            Provide detailed findings.
            """,
            
            "hila": """
            Analyze the HILA on this chest X-ray:
            - Hilar size (enlarged, normal, small)
            - Hilar density
            - Hilar position (right should be lower than left)
            - Lymphadenopathy
            - Mass vs vascular structures
            Provide detailed findings.
            """,
            
            "lungs": """
            Analyze the LUNGS on this chest X-ray:
            - Lung volumes
            - Parenchymal opacities (air space vs interstitial)
            - Distribution pattern
            - Nodules or masses
            - Cavitations
            - Hyperinflation or atelectasis
            Provide detailed findings with differential diagnosis.
            """,
            
            "airways": """
            Analyze the AIRWAYS on this chest X-ray:
            - Trachea position and caliber
            - Bronchi visualization
            - Air bronchograms
            - Bronchial wall thickening
            - Evidence of bronchiectasis
            Provide detailed findings.
            """,
            
            "pleura": """
            Analyze the PLEURA AND DIAPHRAGM on this chest X-ray:
            - Pleural effusions (blunting, meniscus sign)
            - Pneumothorax (pleural line, deep sulcus)
            - Pleural thickening or calcification
            - Diaphragm position and contour
            - Costophrenic angles
            Provide detailed findings.
            """
        }
        
        prompt = prompts.get(region.lower().replace(" ", "_"), prompts["lungs"])
        return self.analyze_image(image, prompt)
    
    def identify_patterns(self, image: Image.Image) -> str:
        """
        Identify radiographic patterns and provide differential diagnosis
        
        Args:
            image: PIL Image of chest X-ray
            
        Returns:
            Pattern analysis with differential diagnosis
        """
        prompt = """
        You are an expert radiologist analyzing a chest X-ray for diagnostic patterns.
        
        Identify the PRIMARY RADIOGRAPHIC PATTERN(S):
        
        1. INTERSTITIAL PATTERNS:
           - Reticular (fine lines, honeycombing)
           - Nodular (small nodules)
           - Reticulonodular (combination)
        
        2. AIR SPACE PATTERNS:
           - Consolidation (air bronchograms)
           - Ground glass
           - Cavitation
        
        3. DISTRIBUTION:
           - Upper vs lower zones
           - Central vs peripheral
           - Focal vs diffuse
           - Unilateral vs bilateral
        
        4. PROVIDE DIFFERENTIAL DIAGNOSIS:
           - List 3-5 most likely diagnoses
           - Rank by probability
           - Explain key distinguishing features
        
        5. SUGGEST ADDITIONAL WORKUP:
           - CT scan
           - Laboratory tests
           - Clinical correlation needed
        
        Format your response clearly with headings for each section.
        """
        
        return self.analyze_image(image, prompt, temperature=0.5)
    
    def generate_radiology_report(
        self, 
        image: Image.Image,
        clinical_history: str = ""
    ) -> str:
        """
        Generate a structured radiology report
        
        Args:
            image: PIL Image of chest X-ray
            clinical_history: Optional clinical information
            
        Returns:
            Formatted radiology report
        """
        prompt = f"""
        Generate a comprehensive radiology report for this chest X-ray.
        
        Clinical History: {clinical_history if clinical_history else "Not provided"}
        
        Use the following structure:
        
        EXAMINATION: Chest X-ray, PA and lateral views
        
        COMPARISON: [State if comparison available]
        
        TECHNICAL FACTORS:
        - Quality assessment (positioning, penetration, inspiration)
        
        FINDINGS:
        
        Support Devices/Lines:
        [Describe any tubes, lines, devices]
        
        Chest Wall:
        [Evaluate soft tissues, bones]
        
        Mediastinum:
        - Heart size: [CTR measurement if possible]
        - Mediastinal contours: [Normal/abnormal]
        
        Hila:
        [Describe hilar structures]
        
        Lungs:
        [Detailed lung parenchyma description]
        - Right lung:
        - Left lung:
        
        Pleura:
        [Effusion, pneumothorax, thickening]
        
        Diaphragm:
        [Position, contour]
        
        IMPRESSION:
        1. [Primary finding]
        2. [Secondary findings]
        3. [Recommendations]
        
        Use professional medical terminology and be specific in measurements when possible.
        """
        
        return self.analyze_image(image, prompt, temperature=0.3, max_tokens=3000)
    
    def analyze_with_custom_prompt(
        self, 
        image: Image.Image, 
        custom_prompt: str
    ) -> str:
        """
        Analyze image with user-provided custom prompt
        
        Args:
            image: PIL Image of chest X-ray
            custom_prompt: User's custom analysis prompt
            
        Returns:
            Analysis based on custom prompt
        """
        return self.analyze_image(image, custom_prompt, temperature=0.5)


# Convenience function for streamlit integration
@st.cache_resource
def get_gemini_client() -> GeminiClient:
    """Get cached Gemini client instance"""
    return GeminiClient()
