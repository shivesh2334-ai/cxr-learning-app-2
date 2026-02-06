"""
Interactive Case Study Module
Educational cases with progressive disclosure
"""

import streamlit as st
from PIL import Image
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from models.gemini_client import get_gemini_client

def interactive_case_study():
    """Interactive case studies for learning"""
    
    st.markdown('<p class="section-header">📚 Interactive Case Studies</p>', 
                unsafe_allow_html=True)
    
    st.info("""
    **Purpose:** Learn through structured case-based education
    
    Work through cases with progressive revelation of clinical information and findings.
    """)
    
    # Case selection
    case_mode = st.radio(
        "Select Mode:",
        ["📖 Guided Cases", "🎯 Self-Assessment", "📤 Upload Custom Case"],
        horizontal=True
    )
    
    if case_mode == "📖 Guided Cases":
        guided_cases()
    elif case_mode == "🎯 Self-Assessment":
        self_assessment_mode()
    else:
        custom_case_upload()

def guided_cases():
    """Pre-built guided teaching cases"""
    
    st.markdown("### 📖 Teaching Cases")
    
    # List of teaching cases
    cases = {
        "Case 1: Right Lower Lobe Pneumonia": {
            "presentation": "67-year-old male with fever, cough, and right-sided chest pain for 3 days.",
            "history": "History of COPD, current smoker (40 pack-years)",
            "vitals": "T: 38.9°C, HR: 105, RR: 24, O2 sat: 91% on room air",
            "labs": "WBC 15,000, CRP elevated",
            "findings": [
                "Right lower lobe consolidation",
                "Air bronchograms present",
                "Silhouette sign - right heart border preserved, diaphragm obscured",
                "Small right pleural effusion"
            ],
            "diagnosis": "Right lower lobe pneumonia with parapneumonic effusion",
            "learning_points": [
                "RLL pneumonia affects posterior segment more than lateral",
                "Air bronchograms confirm air space disease",
                "Preserved right heart border rules out RML involvement",
                "Consider CURB-65 score for admission decision"
            ]
        },
        "Case 2: Congestive Heart Failure": {
            "presentation": "72-year-old female with progressive dyspnea and leg swelling over 1 week.",
            "history": "Known heart failure, medication non-compliance",
            "vitals": "T: 37.1°C, HR: 98, RR: 28, O2 sat: 88% on room air",
            "labs": "BNP 1250, Cr 1.8",
            "findings": [
                "Cardiomegaly (CTR >60%)",
                "Bilateral perihilar opacities ('bat wing' pattern)",
                "Cephalization of pulmonary vessels",
                "Bilateral pleural effusions",
                "Kerley B lines at bases"
            ],
            "diagnosis": "Acute decompensated heart failure with pulmonary edema",
            "learning_points": [
                "Cardiogenic vs non-cardiogenic edema",
                "Perihilar distribution suggests cardiogenic",
                "Pleural effusions more common with heart failure",
                "Look for previous films to assess acuity"
            ]
        },
        "Case 3: Spontaneous Pneumothorax": {
            "presentation": "24-year-old tall, thin male with sudden onset left chest pain and SOB.",
            "history": "Previously healthy, non-smoker",
            "vitals": "T: 37.0°C, HR: 110, RR: 24, O2 sat: 93% on room air",
            "labs": "Normal",
            "findings": [
                "Left pneumothorax (~30% collapse)",
                "Visible visceral pleural line",
                "Absent lung markings peripherally",
                "Trachea midline (no tension)",
                "No mediastinal shift"
            ],
            "diagnosis": "Primary spontaneous pneumothorax",
            "learning_points": [
                "Common in tall, thin young males",
                "Look for pleural line parallel to chest wall",
                "Assess size: measure at hilum level",
                "Tension PTX: tracheal deviation, hemidiaphragm depression"
            ]
        }
    }
    
    selected_case = st.selectbox(
        "Select a case:",
        list(cases.keys())
    )
    
    case = cases[selected_case]
    
    # Progressive disclosure
    st.markdown("---")
    st.markdown(f"### {selected_case}")
    
    # Step 1: Clinical Presentation
    with st.expander("📋 Step 1: Clinical Presentation", expanded=True):
        st.write("**Chief Complaint:**")
        st.info(case["presentation"])
        
        if st.button("Show History & Vitals"):
            st.write("**History:**", case["history"])
            st.write("**Vitals:**", case["vitals"])
            st.write("**Labs:**", case["labs"])
    
    # Step 2: Image Review
    with st.expander("🔍 Step 2: Review the Image"):
        st.warning("""
        **Note:** This demo uses text descriptions. In production, actual 
        de-identified case images would be displayed here.
        """)
        
        st.write("Imagine you're looking at a PA chest X-ray. What systematic approach will you use?")
        
        approach = st.text_area(
            "Your systematic approach:",
            placeholder="List the anatomic regions you'll review..."
        )
    
    # Step 3: Your Interpretation
    with st.expander("💭 Step 3: Your Interpretation"):
        st.write("What are your findings?")
        
        user_findings = st.text_area(
            "Document your findings:",
            placeholder="Use systematic approach: Technical quality, chest wall, mediastinum..."
        )
        
        user_diagnosis = st.text_input(
            "Your differential diagnosis:",
            placeholder="List 2-3 diagnoses in order of likelihood"
        )
        
        if st.button("Compare with Expert Interpretation"):
            st.markdown("#### Expert Findings:")
            for finding in case["findings"]:
                st.write(f"✓ {finding}")
            
            st.markdown("#### Diagnosis:")
            st.success(case["diagnosis"])
    
    # Step 4: Learning Points
    with st.expander("📚 Step 4: Learning Points", expanded=False):
        st.markdown("**Key Teaching Points:**")
        for i, point in enumerate(case["learning_points"], 1):
            st.write(f"{i}. {point}")
        
        st.markdown("---")
        st.info("""
        **Additional Resources:**
        - Review similar cases in your case log
        - Discuss with attending radiologist
        - Read relevant chapters in radiology texts
        - Practice on more cases!
        """)

def self_assessment_mode():
    """Self-assessment quiz mode"""
    
    st.markdown("### 🎯 Self-Assessment Quiz")
    
    st.info("""
    Test your knowledge with these questions. Try to answer before revealing the explanation!
    """)
    
    questions = [
        {
            "q": "What is the normal cardiothoracic ratio on a PA chest X-ray?",
            "options": ["<40%", "<50%", "<60%", "<70%"],
            "correct": 1,
            "explanation": "The normal CTR on a PA view is <50%. On AP views, the heart may appear larger due to magnification, so CTR <55% is acceptable."
        },
        {
            "q": "Which of the following suggests good inspiration on a chest X-ray?",
            "options": [
                "Right hemidiaphragm at 4th anterior rib",
                "Right hemidiaphragm at 6th anterior rib",
                "Right hemidiaphragm at 8th anterior rib",
                "Right hemidiaphragm at 10th anterior rib"
            ],
            "correct": 1,
            "explanation": "Good inspiration is indicated by the right hemidiaphragm at the 6th anterior rib, or the 10th posterior rib at the mid-clavicular line."
        },
        {
            "q": "The silhouette sign with loss of the right heart border suggests pathology in which location?",
            "options": [
                "Right upper lobe",
                "Right middle lobe",
                "Right lower lobe",
                "Left lingula"
            ],
            "correct": 1,
            "explanation": "Loss of the right heart border indicates right middle lobe pathology. The RML is anatomically adjacent to the right heart border."
        },
        {
            "q": "Which pattern is most characteristic of interstitial pulmonary edema?",
            "options": [
                "Consolidation with air bronchograms",
                "Perihilar opacity with Kerley B lines",
                "Multiple cavitary lesions",
                "Miliary nodules"
            ],
            "correct": 1,
            "explanation": "Interstitial edema classically shows perihilar bat-wing opacity, cephalization of vessels, and Kerley B lines (short horizontal lines at lung bases)."
        }
    ]
    
    # Quiz interface
    score = 0
    total = len(questions)
    
    for i, q_data in enumerate(questions, 1):
        st.markdown(f"#### Question {i}/{total}")
        st.write(q_data["q"])
        
        user_answer = st.radio(
            "Select your answer:",
            q_data["options"],
            key=f"q{i}"
        )
        
        if st.button(f"Check Answer #{i}", key=f"check{i}"):
            if q_data["options"].index(user_answer) == q_data["correct"]:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Incorrect. The correct answer is: {q_data['options'][q_data['correct']]}")
            
            st.info(f"**Explanation:** {q_data['explanation']}")
        
        st.markdown("---")
    
    if st.button("Submit Quiz"):
        st.markdown(f"### 📊 Your Score: {score}/{total}")
        
        percentage = (score / total) * 100
        
        if percentage >= 80:
            st.success("🎉 Excellent! You have a strong understanding.")
        elif percentage >= 60:
            st.info("👍 Good work! Review the explanations for missed questions.")
        else:
            st.warning("📚 Keep studying! Review the learning materials and try again.")

def custom_case_upload():
    """Upload custom cases for analysis"""
    
    st.markdown("### 📤 Upload Custom Case")
    
    st.info("""
    Upload your own chest X-ray case for AI-assisted analysis and learning.
    """)
    
    # Clinical information
    st.markdown("#### Clinical Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Patient Age", min_value=0, max_value=120, value=50)
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    
    with col2:
        chief_complaint = st.text_input("Chief Complaint", placeholder="e.g., Shortness of breath")
    
    history = st.text_area(
        "Relevant History",
        placeholder="Medical history, medications, exposures..."
    )
    
    # Image upload
    st.markdown("#### Upload Image")
    uploaded_file = st.file_uploader(
        "Select chest X-ray image",
        type=['jpg', 'jpeg', 'png'],
        key="custom_case"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Case", use_container_width=True)
        
        if st.button("🤖 Generate AI Analysis", type="primary"):
            with st.spinner("Analyzing case..."):
                try:
                    client = get_gemini_client()
                    
                    clinical_context = f"""
                    Age: {age} years
                    Sex: {sex}
                    Chief Complaint: {chief_complaint}
                    History: {history}
                    """
                    
                    report = client.generate_radiology_report(image, clinical_context)
                    
                    st.markdown("### 📄 AI-Generated Analysis")
                    st.markdown(report)
                    
                    st.markdown("---")
                    st.warning("""
                    ⚠️ **Educational Use Only**
                    
                    This AI analysis is for educational purposes. Always:
                    - Correlate with clinical findings
                    - Discuss with supervising physician
                    - Follow institutional protocols
                    - Never use for direct patient care without expert review
                    """)
                    
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")

if __name__ == "__main__":
    interactive_case_study()
