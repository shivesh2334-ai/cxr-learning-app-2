"""
Pattern Recognition Module
Identifies radiographic patterns and provides differential diagnosis
"""

import streamlit as st
from PIL import Image
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from models.gemini_client import get_gemini_client

def pattern_analysis():
    """Pattern-based analysis and differential diagnosis"""
    
    st.markdown('<p class="section-header">🎯 Pattern Recognition & Differential Diagnosis</p>', 
                unsafe_allow_html=True)
    
    st.info("""
    **Purpose:** Identify radiographic patterns and generate differential diagnoses
    
    Pattern recognition is key to narrowing down differential diagnoses in chest radiology.
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Chest X-Ray for Pattern Analysis",
        type=['jpg', 'jpeg', 'png'],
        key="pattern_upload"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            st.subheader("Chest X-Ray Image")
            st.image(image, use_container_width=True)
        
        with col2:
            st.subheader("Analysis Options")
            
            analysis_type = st.radio(
                "Select Analysis Type:",
                [
                    "🔍 AI Pattern Recognition",
                    "📋 Manual Pattern Selection",
                    "🎓 Pattern Learning Mode"
                ]
            )
            
            if "AI Pattern" in analysis_type:
                if st.button("🤖 Analyze Patterns", type="primary", use_container_width=True):
                    analyze_patterns_ai(image)
            
            elif "Manual Pattern" in analysis_type:
                manual_pattern_selection()
            
            else:
                learning_mode()
    
    else:
        st.info("👆 Upload a chest X-ray to begin pattern analysis")
        display_pattern_reference()

def analyze_patterns_ai(image):
    """AI-powered pattern analysis"""
    
    with st.spinner("Analyzing radiographic patterns with AI..."):
        try:
            client = get_gemini_client()
            analysis = client.identify_patterns(image)
            
            st.markdown("### 🎯 AI Pattern Analysis Results")
            st.markdown(analysis)
            
            # Additional resources
            st.markdown("---")
            st.success("""
            💡 **Next Steps:**
            1. Correlate with clinical history
            2. Consider additional imaging (CT, lateral view)
            3. Review with attending physician
            4. Follow appropriate guidelines for management
            """)
            
        except Exception as e:
            st.error(f"Analysis error: {str(e)}")

def manual_pattern_selection():
    """Manual pattern selection for learning"""
    
    st.markdown("### 📋 Manual Pattern Assessment")
    
    st.markdown("**Select the predominant pattern(s) you observe:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Interstitial Patterns:**")
        reticular = st.checkbox("Reticular (linear opacities)")
        nodular = st.checkbox("Nodular (small nodules)")
        reticulonodular = st.checkbox("Reticulonodular (mixed)")
        honeycombing = st.checkbox("Honeycombing")
        
        st.markdown("**Air Space Patterns:**")
        consolidation = st.checkbox("Consolidation")
        ground_glass = st.checkbox("Ground glass")
        
    with col2:
        st.markdown("**Distribution:**")
        upper = st.checkbox("Upper zone predominant")
        lower = st.checkbox("Lower zone predominant")
        peripheral = st.checkbox("Peripheral")
        perihilar = st.checkbox("Perihilar/central")
        
        st.markdown("**Special Patterns:**")
        cavitation = st.checkbox("Cavitation")
        miliary = st.checkbox("Miliary (tiny nodules)")
    
    if st.button("Generate Differential Diagnosis", type="primary"):
        generate_manual_differential(
            reticular, nodular, reticulonodular, honeycombing,
            consolidation, ground_glass, upper, lower,
            peripheral, perihilar, cavitation, miliary
        )

def generate_manual_differential(
    reticular, nodular, reticulonodular, honeycombing,
    consolidation, ground_glass, upper, lower,
    peripheral, perihilar, cavitation, miliary
):
    """Generate differential based on manual pattern selection"""
    
    st.markdown("---")
    st.markdown("### 🎯 Differential Diagnosis")
    
    differentials = []
    
    # Pattern-based differential logic
    if reticular and lower:
        differentials.extend([
            ("UIP/IPF", "Usual interstitial pneumonia - honeycombing, basal"),
            ("NSIP", "Non-specific interstitial pneumonia"),
            ("Asbestosis", "Occupational exposure history"),
            ("Collagen vascular disease", "RA, scleroderma, etc.")
        ])
    
    if reticular and upper:
        differentials.extend([
            ("Sarcoidosis", "Upper lobe, nodular, hilar LAD"),
            ("Tuberculosis", "Apical, cavitation possible"),
            ("Silicosis", "Occupational exposure")
        ])
    
    if nodular and upper:
        differentials.extend([
            ("Tuberculosis", "Apical location, may cavitate"),
            ("Sarcoidosis", "Perilymphatic distribution"),
            ("Silicosis", "Coal worker's pneumoconiosis"),
            ("Langerhans cell histiocytosis", "Cystic changes in smokers")
        ])
    
    if consolidation:
        differentials.extend([
            ("Pneumonia", "Bacterial - air bronchograms"),
            ("Pulmonary edema", "Perihilar, bilateral"),
            ("Hemorrhage", "Diffuse, often trauma/vasculitis"),
            ("ARDS", "Bilateral, hypoxemia")
        ])
    
    if perihilar:
        differentials.extend([
            ("Sarcoidosis", "Bilateral hilar LAD"),
            ("Pulmonary edema", "Bat wing pattern"),
            ("Lymphoma", "Mass effect")
        ])
    
    if miliary:
        differentials.extend([
            ("Miliary TB", "Immunocompromised, exposure"),
            ("Fungal infection", "Histoplasmosis, coccidioidomycosis"),
            ("Metastases", "Thyroid, melanoma, renal"),
            ("Sarcoidosis", "Less common presentation")
        ])
    
    if cavitation:
        differentials.extend([
            ("Tuberculosis", "Primary consideration"),
            ("Lung abscess", "Anaerobic, aspiration"),
            ("Squamous cell carcinoma", "Primary lung cancer"),
            ("Wegener's granulomatosis", "Multiple cavities")
        ])
    
    if differentials:
        for i, (diagnosis, description) in enumerate(differentials, 1):
            st.markdown(f"**{i}. {diagnosis}**")
            st.write(f"   {description}")
    else:
        st.warning("Please select at least one pattern to generate differential diagnosis")
    
    # Recommendations
    st.markdown("---")
    st.info("""
    **📋 Clinical Correlation Required:**
    - Patient age and demographics
    - Symptom onset and duration
    - Risk factors and exposures
    - Laboratory findings
    - Prior imaging
    """)

def learning_mode():
    """Interactive learning mode for pattern recognition"""
    
    st.markdown("### 🎓 Pattern Learning Mode")
    
    st.success("""
    **Learning Approach:**
    1. First, describe what you see without labels
    2. Then categorize the pattern
    3. Finally, generate differential diagnosis
    """)
    
    st.markdown("**Step 1: Describe the findings**")
    description = st.text_area(
        "What do you observe in the lungs?",
        placeholder="Example: I see fine linear opacities predominantly in the lower lung zones..."
    )
    
    st.markdown("**Step 2: Identify the distribution**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.selectbox("Zonal distribution", ["Upper", "Middle", "Lower", "Diffuse"])
    with col2:
        st.selectbox("Laterality", ["Unilateral", "Bilateral", "Asymmetric"])
    with col3:
        st.selectbox("Central vs Peripheral", ["Central", "Peripheral", "Both"])
    
    st.markdown("**Step 3: Clinical context**")
    clinical_info = st.text_area(
        "Relevant clinical information",
        placeholder="Age, symptoms, risk factors, exposures..."
    )
    
    if st.button("💡 Get Learning Feedback"):
        st.markdown("---")
        st.markdown("### 📚 Educational Feedback")
        st.info("""
        Great practice! In a real clinical scenario, you would now:
        
        1. **Correlate** your findings with the clinical history
        2. **Generate** a focused differential diagnosis
        3. **Recommend** appropriate next steps (CT, labs, consultation)
        4. **Discuss** with your attending or radiologist
        
        Continue practicing pattern recognition with multiple cases to build expertise!
        """)

def display_pattern_reference():
    """Display pattern recognition reference guide"""
    
    st.markdown("### 📖 Pattern Recognition Reference")
    
    tab1, tab2, tab3 = st.tabs([
        "Interstitial Patterns",
        "Air Space Patterns",
        "Special Patterns"
    ])
    
    with tab1:
        st.markdown("""
        ### Interstitial Patterns
        
        #### Reticular Pattern
        - **Appearance:** Fine linear opacities, network-like
        - **Causes:** Interstitial fibrosis, edema, lymphangitic carcinomatosis
        - **Distribution matters:** Upper vs lower, peripheral vs central
        
        #### Nodular Pattern
        - **Appearance:** Multiple small nodules (1-10mm)
        - **Perilymphatic:** Along bronchovascular bundles (sarcoid)
        - **Random:** Hematogenous spread (miliary TB, mets)
        - **Centrilobular:** Bronchiolar disease (hypersensitivity pneumonitis)
        
        #### Reticulonodular
        - **Appearance:** Combination of lines and nodules
        - **Causes:** Advanced interstitial disease, sarcoidosis
        
        #### Honeycombing
        - **Appearance:** Clustered cystic spaces, subpleural
        - **Significance:** End-stage pulmonary fibrosis
        - **Causes:** UIP/IPF, asbestosis, chronic HP
        """)
    
    with tab2:
        st.markdown("""
        ### Air Space Patterns
        
        #### Consolidation
        - **Appearance:** Homogeneous opacity, obscures vessels
        - **Air bronchograms:** Air-filled bronchi visible
        - **Silhouette sign:** Loss of adjacent borders
        - **Causes:** Pneumonia, edema, hemorrhage, contusion
        
        #### Ground Glass Opacity
        - **Appearance:** Hazy opacity, vessels still visible
        - **Better seen on CT**
        - **Causes:** Early pneumonia, edema, hemorrhage, pneumonitis
        
        #### Distribution Patterns
        - **Lobar:** Follows anatomic lobes (bacterial pneumonia)
        - **Segmental:** Limited to bronchopulmonary segments
        - **Multifocal:** Multiple discrete areas (bronchopneumonia)
        - **Diffuse:** Both lungs (ARDS, edema)
        """)
    
    with tab3:
        st.markdown("""
        ### Special Patterns
        
        #### Miliary Pattern
        - **Appearance:** Innumerable tiny nodules (1-3mm)
        - **Causes:** TB, fungal, metastases, sarcoid
        - **Distribution:** Diffuse, random
        
        #### Cavitation
        - **Appearance:** Air-filled space within opacity
        - **Thick wall (>4mm):** Abscess, cancer, Wegener's
        - **Thin wall (<4mm):** Pneumatocele, cyst, bulla
        
        #### Tree-in-Bud
        - **Appearance:** Branching opacities (better on CT)
        - **Causes:** Infectious bronchiolitis, aspiration
        
        #### Crazy Paving
        - **Appearance:** Ground glass + interlobular septal thickening
        - **Causes:** Pneumocystis, alveolar proteinosis, ARDS
        """)

if __name__ == "__main__":
    pattern_analysis()
