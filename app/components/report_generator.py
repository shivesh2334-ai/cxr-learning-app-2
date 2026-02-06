"""
Structured Report Generator Module
Generates professional radiology reports
"""

import streamlit as st
from PIL import Image
import sys
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent.parent))

from models.gemini_client import get_gemini_client

def generate_structured_report():
    """Generate structured radiology reports"""
    
    st.markdown('<p class="section-header">📄 Structured Report Generator</p>', 
                unsafe_allow_html=True)
    
    st.info("""
    **Purpose:** Create professional, structured radiology reports
    
    Learn the standard format and components of chest X-ray reports.
    """)
    
    # Two modes
    mode = st.radio(
        "Select Mode:",
        ["🤖 AI-Assisted Report", "✍️ Manual Template"],
        horizontal=True
    )
    
    if mode == "🤖 AI-Assisted Report":
        ai_assisted_report()
    else:
        manual_template_report()

def ai_assisted_report():
    """AI-assisted report generation"""
    
    st.markdown("### 🤖 AI-Assisted Report Generation")
    
    # Upload section
    uploaded_file = st.file_uploader(
        "Upload Chest X-Ray",
        type=['jpg', 'jpeg', 'png'],
        key="report_upload"
    )
    
    # Clinical information
    st.markdown("#### Clinical Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        patient_age = st.number_input("Age", min_value=0, max_value=120, value=50)
        patient_sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    
    with col2:
        exam_date = st.date_input("Exam Date", datetime.now())
        exam_type = st.selectbox(
            "Exam Type",
            ["Chest X-ray 2 views", "Chest X-ray PA only", "Portable AP"]
        )
    
    with col3:
        comparison = st.selectbox(
            "Comparison",
            ["None available", "Prior from 1 week ago", "Prior from 1 month ago", "Prior from 1 year ago"]
        )
    
    clinical_history = st.text_area(
        "Clinical History/Indication",
        placeholder="e.g., Fever and cough, rule out pneumonia"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, caption="X-Ray Image", use_container_width=True)
        
        with col2:
            st.markdown("#### Report Options")
            
            include_tech = st.checkbox("Include technical assessment", value=True)
            include_comparison = st.checkbox("Include comparison section", value=True)
            detail_level = st.select_slider(
                "Detail Level",
                options=["Concise", "Standard", "Detailed"],
                value="Standard"
            )
            
            generate_btn = st.button(
                "📝 Generate Report",
                type="primary",
                use_container_width=True
            )
        
        if generate_btn:
            with st.spinner("Generating structured report..."):
                try:
                    client = get_gemini_client()
                    
                    clinical_context = f"""
                    Patient: {patient_age} year old {patient_sex}
                    Exam: {exam_type}
                    Date: {exam_date}
                    Comparison: {comparison}
                    Clinical History: {clinical_history}
                    """
                    
                    report = client.generate_radiology_report(image, clinical_context)
                    
                    # Display report
                    st.markdown("---")
                    st.markdown("### 📄 Generated Report")
                    
                    # Report in a nice container
                    st.markdown("""
                    <div style='background-color: white; padding: 2rem; border-radius: 0.5rem; border: 1px solid #ddd;'>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(report)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Download options
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.download_button(
                            "📥 Download as TXT",
                            report,
                            file_name=f"cxr_report_{exam_date}.txt",
                            mime="text/plain"
                        )
                    
                    with col2:
                        # Create formatted report
                        formatted_report = format_report_for_export(
                            report, patient_age, patient_sex, exam_date, 
                            exam_type, clinical_history
                        )
                        st.download_button(
                            "📥 Download Formatted",
                            formatted_report,
                            file_name=f"cxr_report_{exam_date}_formatted.txt",
                            mime="text/plain"
                        )
                    
                    # Educational feedback
                    st.markdown("---")
                    st.success("""
                    **💡 Report Writing Tips:**
                    - Always start with technical quality
                    - Use systematic approach for findings
                    - Be specific about locations (RUL, RML, RLL, etc.)
                    - Include measurements when relevant (CTR, lesion size)
                    - Rank impressions by clinical importance
                    - Suggest follow-up or additional imaging when appropriate
                    """)
                    
                except Exception as e:
                    st.error(f"Error generating report: {str(e)}")
    
    else:
        st.info("👆 Upload a chest X-ray image to generate a report")
        display_report_template_guide()

def manual_template_report():
    """Manual report writing with templates"""
    
    st.markdown("### ✍️ Manual Report Template")
    
    st.info("""
    Use this template to practice writing structured reports. Fill in each section systematically.
    """)
    
    # Report template sections
    st.markdown("#### EXAMINATION")
    examination = st.text_input(
        "Examination Type",
        value="Chest radiograph, PA and lateral views"
    )
    
    st.markdown("#### COMPARISON")
    comparison = st.text_input(
        "Comparison Studies",
        placeholder="None available / Prior chest X-ray dated MM/DD/YYYY"
    )
    
    st.markdown("#### CLINICAL INDICATION")
    indication = st.text_area(
        "Clinical Indication",
        placeholder="e.g., Fever and productive cough"
    )
    
    st.markdown("#### TECHNICAL FACTORS")
    technical = st.text_area(
        "Technical Assessment",
        value="The examination is adequate for interpretation. Patient positioning is satisfactory. Adequate inspiration. No motion artifact.",
        height=100
    )
    
    st.markdown("#### FINDINGS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Lines/Tubes/Devices:**")
        devices = st.text_area(
            "Support Devices",
            placeholder="None / Describe any present",
            height=80,
            key="devices"
        )
        
        st.markdown("**Chest Wall:**")
        chest_wall = st.text_area(
            "Chest Wall",
            placeholder="Soft tissues are unremarkable. Osseous structures are intact.",
            height=80,
            key="chest_wall"
        )
        
        st.markdown("**Mediastinum:**")
        mediastinum = st.text_area(
            "Mediastinum",
            placeholder="Heart size is normal. Mediastinal and hilar contours are normal.",
            height=80,
            key="mediastinum"
        )
    
    with col2:
        st.markdown("**Lungs:**")
        lungs = st.text_area(
            "Lung Fields",
            placeholder="The lungs are clear. No focal consolidation, pleural effusion, or pneumothorax.",
            height=150,
            key="lungs"
        )
        
        st.markdown("**Pleura:**")
        pleura = st.text_area(
            "Pleural Spaces",
            placeholder="No pleural effusion or pneumothorax.",
            height=80,
            key="pleura"
        )
    
    st.markdown("#### IMPRESSION")
    impression = st.text_area(
        "Impression (numbered list)",
        placeholder="1. [Most important finding]\n2. [Secondary findings]\n3. [Recommendations if any]",
        height=120
    )
    
    # Preview and save
    if st.button("📋 Preview Complete Report", type="primary"):
        st.markdown("---")
        st.markdown("### 📄 Report Preview")
        
        complete_report = f"""
EXAMINATION: {examination}

COMPARISON: {comparison}

CLINICAL INDICATION: {indication}

TECHNICAL FACTORS:
{technical}

FINDINGS:

Lines/Tubes/Devices:
{devices if devices else "None."}

Chest Wall:
{chest_wall if chest_wall else "Soft tissues and osseous structures are unremarkable."}

Mediastinum:
{mediastinum if mediastinum else "Heart size and mediastinal contours are normal."}

Lungs:
{lungs if lungs else "The lungs are clear bilaterally."}

Pleura:
{pleura if pleura else "No pleural effusion or pneumothorax."}

IMPRESSION:
{impression if impression else "No acute cardiopulmonary process."}
        """
        
        st.code(complete_report, language=None)
        
        st.download_button(
            "📥 Download Report",
            complete_report,
            file_name="chest_xray_report.txt",
            mime="text/plain"
        )

def format_report_for_export(report, age, sex, exam_date, exam_type, history):
    """Format report for professional export"""
    
    header = f"""
{'='*80}
RADIOLOGY REPORT - EDUCATIONAL CASE
{'='*80}

Patient Information:
  Age: {age} years
  Sex: {sex}

Study Information:
  Exam: {exam_type}
  Date: {exam_date}
  
Clinical History:
  {history}

{'='*80}

"""
    
    footer = f"""

{'='*80}
Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DISCLAIMER: This report is AI-generated for educational purposes only.
Not for clinical use. Requires review by qualified radiologist.
{'='*80}
"""
    
    return header + report + footer

def display_report_template_guide():
    """Display guide for report writing"""
    
    st.markdown("### 📖 Report Writing Guide")
    
    with st.expander("Standard Report Structure", expanded=False):
        st.markdown("""
        A well-structured chest X-ray report includes:
        
        1. **EXAMINATION**: Type of study performed
        2. **COMPARISON**: Reference to prior studies
        3. **CLINICAL INDICATION**: Why the study was ordered
        4. **TECHNICAL FACTORS**: Quality assessment
        5. **FINDINGS**: Systematic review of all structures
        6. **IMPRESSION**: Summary and recommendations
        """)
    
    with st.expander("Standard Phrases", expanded=False):
        st.markdown("""
        **Normal findings:**
        - "The lungs are clear bilaterally."
        - "Heart size is normal."
        - "No focal consolidation, pleural effusion, or pneumothorax."
        - "Osseous structures are intact."
        - "No acute cardiopulmonary process."
        
        **Abnormal findings:**
        - "Focal opacity in the [location] concerning for [diagnosis]."
        - "Cardiomegaly with cardiothoracic ratio of [X]%."
        - "Bilateral interstitial opacities consistent with [pattern]."
        - "[Size] pleural effusion, [side]."
        - "Recommend correlation with [imaging/clinical info]."
        """)
    
    with st.expander("Common Mistakes to Avoid", expanded=False):
        st.markdown("""
        ❌ **Don't:**
        - Use vague terms like "abnormal" without description
        - Make diagnoses without differential
        - Ignore technical quality issues
        - Forget to mention all major anatomic areas
        - Use abbreviations without defining them first
        
        ✅ **Do:**
        - Be specific about locations and sizes
        - Provide measurements when relevant
        - Suggest appropriate follow-up
        - Use consistent medical terminology
        - Correlate with clinical history
        """)

if __name__ == "__main__":
    generate_structured_report()
