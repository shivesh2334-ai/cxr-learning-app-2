"""
Technical Quality Assessment Module
Evaluates chest X-ray technical parameters
"""

import streamlit as st
from PIL import Image
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from models.gemini_client import get_gemini_client

def technical_quality_assessor():
    """Main function for technical quality assessment"""
    
    st.markdown('<p class="section-header">📋 Technical Quality Assessment</p>', 
                unsafe_allow_html=True)
    
    st.info("""
    **Purpose:** Ensure diagnostic quality before interpretation
    
    A technically adequate chest X-ray must satisfy the "PRIM" criteria:
    - **P**ositioning
    - **R**otation (or Penetration)
    - **I**nspiration
    - **M**otion
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Chest X-Ray Image",
        type=['jpg', 'jpeg', 'png'],
        help="Supported formats: JPG, PNG"
    )
    
    if uploaded_file is not None:
        # Display image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
            
            # Image info
            st.caption(f"Size: {image.size[0]}x{image.size[1]} pixels")
        
        with col2:
            st.subheader("Technical Checklist")
            
            # Manual checklist for learning
            with st.expander("✅ Self-Assessment Checklist", expanded=True):
                st.markdown("**Before AI analysis, try to assess yourself:**")
                
                positioning = st.checkbox("Proper positioning (spinous processes midline)")
                penetration = st.checkbox("Adequate penetration (vertebrae visible)")
                inspiration = st.checkbox("Good inspiration (right diaphragm at 6th rib)")
                motion = st.checkbox("No motion artifact (sharp borders)")
                
                if all([positioning, penetration, inspiration, motion]):
                    st.success("✅ All criteria met - Proceed with interpretation!")
                else:
                    st.warning("⚠️ Review technical quality before interpretation")
        
        # AI Analysis Section
        st.markdown("---")
        st.subheader("🤖 AI-Powered Analysis")
        
        col3, col4 = st.columns([2, 1])
        
        with col4:
            analyze_button = st.button(
                "🔍 Analyze Technical Quality",
                type="primary",
                use_container_width=True
            )
        
        if analyze_button:
            with st.spinner("Analyzing image with Gemini AI..."):
                try:
                    # Get Gemini client
                    client = get_gemini_client()
                    
                    # Analyze technical quality
                    result = client.analyze_technical_quality(image)
                    
                    # Display results
                    st.markdown("### AI Assessment Results")
                    
                    # Parse and display results
                    st.markdown(result['raw_analysis'])
                    
                    # Educational tips
                    st.markdown("---")
                    st.markdown("### 📚 Learning Points")
                    
                    tips_col1, tips_col2 = st.columns(2)
                    
                    with tips_col1:
                        st.markdown("""
                        **Common Technical Errors:**
                        - Patient rotation → Asymmetric rib spacing
                        - Poor inspiration → <6 ribs visible
                        - Overpenetration → Too dark/burned out
                        - Underpenetration → Too white
                        - Motion → Blurred cardiac borders
                        """)
                    
                    with tips_col2:
                        st.markdown("""
                        **Clinical Impact:**
                        - Poor positioning → Miss subtle lesions
                        - Underpenetration → Overestimate infiltrates
                        - Poor inspiration → False cardiomegaly
                        - Motion → Miss fine detail
                        """)
                    
                    # Recommendations
                    st.info("""
                    **💡 Pro Tip:** Always assess technical quality FIRST before 
                    attempting diagnostic interpretation. A poor quality film may 
                    need to be repeated rather than interpreted.
                    """)
                    
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    st.info("""
                    **Troubleshooting:**
                    1. Check if GEMINI_API_KEY is set in `.streamlit/secrets.toml`
                    2. Ensure image is a valid chest X-ray
                    3. Try a different image format
                    """)
        
        # Reference guide
        st.markdown("---")
        with st.expander("📖 Detailed Technical Reference Guide"):
            st.markdown("""
            ### Positioning Assessment
            
            **Ideal PA View:**
            - Patient upright, chest against detector
            - Shoulders rotated forward
            - Scapulae outside lung fields
            - Spinous processes equidistant from medial clavicles
            
            **Rotation Detection:**
            - Compare medial clavicular heads to spinous processes
            - Should be equidistant
            - Asymmetry indicates rotation
            
            ---
            
            ### Penetration Assessment
            
            **Adequate Penetration:**
            - See vertebral bodies through heart
            - Intervertebral disc spaces visible
            - Lung vessels visible behind heart
            
            **Overpenetration:**
            - Lungs appear too dark/black
            - Loss of soft tissue detail
            - Bones appear too bright
            
            **Underpenetration:**
            - Mediastinum appears too white
            - Cannot see through heart
            - May simulate infiltrate
            
            ---
            
            ### Inspiration Assessment
            
            **Adequate Inspiration (PA view):**
            - Right hemidiaphragm at 6th anterior rib OR
            - 10th posterior rib at mid-clavicular line
            - Costophrenic angles visible
            
            **Poor Inspiration:**
            - <6 anterior ribs visible
            - Heart appears enlarged (false cardiomegaly)
            - Lung bases appear hazy
            - Crowded lung markings
            
            ---
            
            ### Motion Assessment
            
            **No Motion:**
            - Sharp cardiac borders
            - Sharp diaphragm contours
            - Sharp vessel margins
            - Distinct rib cortices
            
            **Motion Present:**
            - Blurred borders
            - Indistinct vessels
            - Double diaphragm contour
            - Film should be repeated
            """)
    
    else:
        # Instructions when no image uploaded
        st.info("""
        👆 Upload a chest X-ray image to begin technical quality assessment.
        
        **Accepted formats:** JPG, JPEG, PNG
        
        **Recommended:** PA (posteroanterior) or AP (anteroposterior) views
        """)
        
        # Sample image section
        st.markdown("---")
        st.markdown("### 📚 Sample Images for Practice")
        
        st.warning("""
        **Note:** For privacy and ethical reasons, this repository does not include 
        actual patient X-rays. 
        
        **To practice:**
        1. Use public datasets (NIH ChestX-ray14, MIMIC-CXR)
        2. Use educational resources from RadiologyAssistant.nl
        3. Use synthetic/phantom images
        4. Always ensure proper consent and de-identification
        """)

if __name__ == "__main__":
    technical_quality_assessor()
      
