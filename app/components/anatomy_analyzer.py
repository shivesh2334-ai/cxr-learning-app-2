"""
Anatomy Systematic Review Module
Guides through systematic anatomic evaluation
"""

import streamlit as st
from PIL import Image
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from models.gemini_client import get_gemini_client

def anatomy_systematic_review():
    """Systematic anatomic review of chest X-ray"""
    
    st.markdown('<p class="section-header">🔍 Systematic Anatomy Review</p>', 
                unsafe_allow_html=True)
    
    st.info("""
    **Purpose:** Ensure comprehensive evaluation of all anatomic structures
    
    Follow the systematic approach to avoid missing important findings.
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Chest X-Ray for Systematic Review",
        type=['jpg', 'jpeg', 'png'],
        key="anatomy_upload"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Display image
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.subheader("Chest X-Ray Image")
            st.image(image, use_container_width=True)
        
        with col2:
            st.subheader("Select Region to Analyze")
            
            region = st.selectbox(
                "Anatomic Region:",
                [
                    "Chest Wall",
                    "Mediastinum",
                    "Hila",
                    "Lungs",
                    "Airways",
                    "Pleura"
                ]
            )
            
            analyze_btn = st.button(
                f"🔬 Analyze {region}",
                type="primary",
                use_container_width=True
            )
        
        # Analysis section
        if analyze_btn:
            with st.spinner(f"Analyzing {region}..."):
                try:
                    client = get_gemini_client()
                    
                    # Map region names
                    region_map = {
                        "Chest Wall": "chest_wall",
                        "Mediastinum": "mediastinum",
                        "Hila": "hila",
                        "Lungs": "lungs",
                        "Airways": "airways",
                        "Pleura": "pleura"
                    }
                    
                    analysis = client.analyze_anatomy_systematic(
                        image, 
                        region_map[region]
                    )
                    
                    # Display results
                    st.markdown(f"### 📊 {region} Analysis")
                    st.markdown(analysis)
                    
                    # Region-specific learning points
                    display_learning_points(region)
                    
                except Exception as e:
                    st.error(f"Analysis error: {str(e)}")
        
        # Systematic checklist
        st.markdown("---")
        st.subheader("📋 Systematic Review Checklist")
        
        with st.expander("Complete Systematic Review", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.checkbox("✓ Technical quality assessed")
                st.checkbox("✓ Support devices/lines identified")
                st.checkbox("✓ Chest wall evaluated")
                st.checkbox("✓ Mediastinum reviewed")
            
            with col2:
                st.checkbox("✓ Hila assessed")
                st.checkbox("✓ Lungs examined")
                st.checkbox("✓ Airways checked")
                st.checkbox("✓ Pleura and diaphragm reviewed")
    
    else:
        st.info("👆 Upload a chest X-ray to begin systematic anatomic review")
        
        # Educational content
        display_systematic_approach_guide()

def display_learning_points(region: str):
    """Display region-specific learning points"""
    
    learning_points = {
        "Chest Wall": {
            "common_findings": [
                "Rib fractures (acute vs old)",
                "Lytic lesions (metastases, myeloma)",
                "Blastic lesions (prostate mets, Paget's)",
                "Soft tissue emphysema",
                "Asymmetric breast shadows"
            ],
            "pitfalls": [
                "Missing subtle rib fractures",
                "Confusing companion shadows with lesions",
                "Not correlating with clinical history"
            ]
        },
        "Mediastinum": {
            "common_findings": [
                "Cardiomegaly (CTR >50%)",
                "Mediastinal widening",
                "Aortic abnormalities",
                "Hiatal hernia",
                "Anterior mediastinal mass"
            ],
            "pitfalls": [
                "False cardiomegaly on AP films",
                "Missing lymphadenopathy",
                "Not recognizing aortic dissection"
            ]
        },
        "Hila": {
            "common_findings": [
                "Hilar lymphadenopathy",
                "Hilar masses",
                "Vascular enlargement",
                "Asymmetric hila"
            ],
            "pitfalls": [
                "Confusing vessels with lymph nodes",
                "Missing unilateral enlargement",
                "Not using lateral view for confirmation"
            ]
        },
        "Lungs": {
            "common_findings": [
                "Consolidation (air space disease)",
                "Interstitial patterns",
                "Nodules and masses",
                "Atelectasis",
                "Hyperinflation"
            ],
            "pitfalls": [
                "Missing subtle infiltrates",
                "Confusing atelectasis with infiltrate",
                "Not describing distribution pattern"
            ]
        },
        "Airways": {
            "common_findings": [
                "Tracheal deviation",
                "Bronchial wall thickening",
                "Air bronchograms",
                "Bronchiectasis"
            ],
            "pitfalls": [
                "Missing tracheal narrowing",
                "Not recognizing air trapping",
                "Overlooking foreign bodies"
            ]
        },
        "Pleura": {
            "common_findings": [
                "Pleural effusion",
                "Pneumothorax",
                "Pleural thickening",
                "Pleural calcification"
            ],
            "pitfalls": [
                "Missing small pneumothorax",
                "Confusing fissures with pneumothorax",
                "Not identifying loculated effusions"
            ]
        }
    }
    
    if region in learning_points:
        st.markdown("---")
        st.markdown("### 📚 Learning Points")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Common Findings:**")
            for finding in learning_points[region]["common_findings"]:
                st.write(f"• {finding}")
        
        with col2:
            st.markdown("**Common Pitfalls:**")
            for pitfall in learning_points[region]["pitfalls"]:
                st.write(f"⚠️ {pitfall}")

def display_systematic_approach_guide():
    """Display guide for systematic approach"""
    
    st.markdown("### 📖 Systematic Approach Guide")
    
    st.markdown("""
    The systematic approach ensures you don't miss important findings. 
    Follow this sequence every time:
    """)
    
    with st.expander("1️⃣ Technical Quality (PRIM)", expanded=False):
        st.markdown("""
        - **P**ositioning
        - **R**otation/Penetration
        - **I**nspiration
        - **M**otion
        """)
    
    with st.expander("2️⃣ Support Devices & Lines", expanded=False):
        st.markdown("""
        - Endotracheal tubes
        - Central venous catheters
        - Nasogastric tubes
        - Chest tubes
        - Pacemakers/ICDs
        - Surgical clips/hardware
        """)
    
    with st.expander("3️⃣ Chest Wall", expanded=False):
        st.markdown("""
        - Soft tissues (emphysema, masses)
        - Ribs (fractures, lesions)
        - Clavicles
        - Scapulae
        - Breast shadows
        """)
    
    with st.expander("4️⃣ Mediastinum", expanded=False):
        st.markdown("""
        - Heart size (CTR)
        - Heart borders
        - Aortic arch
        - Mediastinal width
        - Hiatus
        """)
    
    with st.expander("5️⃣ Hila", expanded=False):
        st.markdown("""
        - Size (normal, enlarged)
        - Position (right lower than left)
        - Density
        - Contour
        """)
    
    with st.expander("6️⃣ Lungs", expanded=False):
        st.markdown("""
        - Volumes
        - Symmetry
        - Vascularity
        - Opacities (location, pattern)
        - Cavities
        - Masses/nodules
        """)
    
    with st.expander("7️⃣ Airways", expanded=False):
        st.markdown("""
        - Trachea (position, caliber)
        - Carina
        - Main bronchi
        - Air bronchograms
        """)
    
    with st.expander("8️⃣ Pleura & Diaphragm", expanded=False):
        st.markdown("""
        - Pleural effusion
        - Pneumothorax
        - Pleural thickening
        - Diaphragm position
        - Costophrenic angles
        - Free air under diaphragm
        """)

if __name__ == "__main__":
    anatomy_systematic_review()
