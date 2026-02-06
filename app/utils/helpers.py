"""
Helper Utilities
General utility functions for the application
"""

import streamlit as st
from typing import Any, Dict, List
import json
from datetime import datetime

def load_json_file(filepath: str) -> Dict[str, Any]:
    """
    Load JSON file
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        Dictionary from JSON
    """
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return {}

def save_json_file(data: Dict[str, Any], filepath: str) -> bool:
    """
    Save dictionary to JSON file
    
    Args:
        data: Dictionary to save
        filepath: Output file path
    
    Returns:
        True if successful
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return False

def format_timestamp() -> str:
    """Get formatted timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate_ctr(heart_width: float, chest_width: float) -> float:
    """
    Calculate cardiothoracic ratio
    
    Args:
        heart_width: Maximum cardiac width in cm
        chest_width: Maximum thoracic width in cm
    
    Returns:
        CTR as percentage
    """
    if chest_width == 0:
        return 0
    return (heart_width / chest_width) * 100

def categorize_ctr(ctr: float) -> str:
    """
    Categorize CTR value
    
    Args:
        ctr: Cardiothoracic ratio percentage
    
    Returns:
        Category string
    """
    if ctr < 50:
        return "Normal"
    elif ctr < 55:
        return "Borderline"
    elif ctr < 60:
        return "Mild cardiomegaly"
    elif ctr < 70:
        return "Moderate cardiomegaly"
    else:
        return "Severe cardiomegaly"

def get_anatomic_regions() -> List[str]:
    """Get list of anatomic regions for systematic review"""
    return [
        "Chest Wall",
        "Mediastinum",
        "Hila",
        "Lungs",
        "Airways",
        "Pleura and Diaphragm"
    ]

def get_technical_parameters() -> List[str]:
    """Get list of technical quality parameters"""
    return [
        "Positioning",
        "Penetration",
        "Inspiration",
        "Motion"
    ]

def create_finding_template() -> Dict[str, str]:
    """Create template for documenting findings"""
    return {
        "region": "",
        "finding": "",
        "location": "",
        "size": "",
        "description": "",
        "impression": ""
    }

def validate_image_upload(uploaded_file) -> bool:
    """
    Validate uploaded image file
    
    Args:
        uploaded_file: Streamlit uploaded file object
    
    Returns:
        True if valid
    """
    if uploaded_file is None:
        return False
    
    # Check file size (max 200MB)
    if uploaded_file.size > 200 * 1024 * 1024:
        st.error("File size exceeds 200MB limit")
        return False
    
    # Check file type
    allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
    if uploaded_file.type not in allowed_types:
        st.error("Invalid file type. Please upload JPG or PNG")
        return False
    
    return True

def generate_case_id() -> str:
    """Generate unique case ID"""
    return f"CASE_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

def format_medical_term(term: str) -> str:
    """
    Format medical terminology consistently
    
    Args:
        term: Medical term
    
    Returns:
        Formatted term
    """
    # Common abbreviations
    abbreviations = {
        'rll': 'RLL',
        'rul': 'RUL',
        'rml': 'RML',
        'lll': 'LLL',
        'lul': 'LUL',
        'ctr': 'CTR',
        'pa': 'PA',
        'ap': 'AP',
        'cxr': 'CXR',
        'ct': 'CT'
    }
    
    return abbreviations.get(term.lower(), term)

def create_differential_diagnosis(
    findings: List[str],
    distribution: str = "",
    patient_age: int = None
) -> List[str]:
    """
    Generate differential diagnosis based on findings
    
    Args:
        findings: List of radiographic findings
        distribution: Pattern distribution
        patient_age: Patient age for age-specific considerations
    
    Returns:
        List of differential diagnoses
    """
    differentials = []
    
    # This is a simplified example - in practice, this would be much more comprehensive
    finding_keywords = ' '.join(findings).lower()
    
    if 'consolidation' in finding_keywords:
        differentials.extend(['Pneumonia', 'Pulmonary edema', 'Hemorrhage'])
    
    if 'nodular' in finding_keywords:
        if patient_age and patient_age > 50:
            differentials.extend(['Metastases', 'Primary lung cancer'])
        differentials.extend(['Tuberculosis', 'Fungal infection', 'Sarcoidosis'])
    
    if 'reticular' in finding_keywords:
        differentials.extend(['Interstitial lung disease', 'Pulmonary fibrosis'])
    
    if 'pleural effusion' in finding_keywords:
        differentials.extend(['CHF', 'Pneumonia', 'Malignancy'])
    
    return differentials

def display_educational_tip(category: str):
    """
    Display educational tips based on category
    
    Args:
        category: Category of tip to display
    """
    tips = {
        "positioning": """
        💡 **Quick Tip - Positioning:**
        Check if spinous processes are equidistant from medial clavicles. 
        If not, the patient is rotated, which can simulate or hide pathology.
        """,
        "inspiration": """
        💡 **Quick Tip - Inspiration:**
        Count the ribs! You should see at least 6 anterior ribs or 10 posterior ribs.
        Poor inspiration can make the heart look bigger (false cardiomegaly).
        """,
        "silhouette": """
        💡 **Quick Tip - Silhouette Sign:**
        When a normal border disappears, look for adjacent pathology:
        - Right heart border → RML
        - Left heart border → Lingula  
        - Diaphragm → Lower lobes
        """,
        "air_bronchogram": """
        💡 **Quick Tip - Air Bronchograms:**
        Visible air-filled bronchi in consolidated lung = AIR SPACE disease.
        If you see air bronchograms, it's NOT purely interstitial.
        """
    }
    
    if category in tips:
        st.info(tips[category])

def create_progress_tracker() -> Dict[str, bool]:
    """Create progress tracker for systematic review"""
    return {
        "technical_quality": False,
        "devices_lines": False,
        "chest_wall": False,
        "mediastinum": False,
        "hila": False,
        "lungs": False,
        "airways": False,
        "pleura": False
    }
