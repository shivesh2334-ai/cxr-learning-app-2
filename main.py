import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from app.components.technical_quality import technical_quality_assessor
from app.components.anatomy_analyzer import anatomy_systematic_review
from app.components.pattern_recognizer import pattern_analysis
from app.components.case_study import interactive_case_study
from app.components.report_generator import generate_structured_report

# Page configuration
st.set_page_config(
    page_title="CXR Learning & Diagnosis System",
    page_icon="🫁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    .main-header { 
        font-size: 2.5rem; 
        font-weight: bold; 
        color: #1f77b4; 
        margin-bottom: 0.5rem;
    }
    .section-header { 
        font-size: 1.5rem; 
        font-weight: bold; 
        color: #2c3e50; 
        margin-top: 1rem; 
    }
    .info-box { 
        background-color: #f0f2f6; 
        padding: 1rem; 
        border-radius: 0.5rem; 
        margin: 1rem 0;
    }
    .checklist-item { 
        margin-left: 1rem; 
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point"""
    
    # Header
    st.markdown('<p class="main-header">🫁 Chest X-Ray Systematic Analysis</p>', 
                unsafe_allow_html=True)
    
    # Medical disclaimer
    st.markdown("""
    <div class="warning-box">
        <strong>⚠️ Educational Tool Only</strong><br>
        This application is for educational purposes only. It is NOT intended for clinical 
        diagnosis or patient care. All clinical decisions must be made by qualified healthcare 
        professionals.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    **Educational tool based on:** 
    - Systematic Approach to Chest Radiographic Analysis (NIH/NCBI)
    - Radiographic Approach to Diffuse Lung Disease (UpToDate)
    - Fleischner Society Guidelines
    """)
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/lungs.png", width=80)
        st.header("Analysis Modules")
        
        module = st.radio(
            "Select Module:",
            [
                "📋 Technical Quality", 
                "🔍 Systematic Anatomy Review", 
                "🎯 Pattern Recognition", 
                "📚 Interactive Cases", 
                "📄 Report Generator", 
                "ℹ️ Knowledge Base"
            ],
            index=0
        )
        
        st.markdown("---")
        
        # Quick reference
        with st.expander("📖 Quick Reference"):
            st.info("""
            **Systematic Components:**
            1. Technical Quality
            2. Support/Monitoring Devices
            3. Chest Wall
            4. Mediastinum
            5. Hila
            6. Lungs
            7. Airways
            8. Pleura/Diaphragm
            """)
        
        # API status check
        st.markdown("---")
        check_api_status()
    
    # Module routing
    if "Technical Quality" in module:
        technical_quality_assessor()
    elif "Systematic Anatomy" in module:
        anatomy_systematic_review()
    elif "Pattern Recognition" in module:
        pattern_analysis()
    elif "Interactive Cases" in module:
        interactive_case_study()
    elif "Report Generator" in module:
        generate_structured_report()
    else:
        display_knowledge_base()

def check_api_status():
    """Check if Gemini API key is configured"""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", None)
        if api_key:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Key Missing")
            st.info("Add GEMINI_API_KEY to .streamlit/secrets.toml")
    except Exception:
        st.warning("⚠️ Configure API Key")

def display_knowledge_base():
    """Display reference knowledge base"""
    st.markdown('<p class="section-header">Reference Knowledge Base</p>', 
                unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Technical Factors", 
        "Anatomic Regions", 
        "Differential Diagnoses",
        "Quick Tips"
    ])
    
    with tab1:
        st.subheader("Technical Quality Assessment")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Positioning
            - ✓ Spinous processes midline between clavicular heads
            - ✓ Scapulae rotated laterally (elbows forward)
            - ✓ No rotation of thorax
            - ✓ Symmetric rib spacing
            
            #### Penetration
            - ✓ Vertebral bodies faintly visible through mediastinum
            - ✓ Lung fields appear gray (not black or white)
            - ✓ Vascular markings clearly visible
            - ✓ Can see through cardiac silhouette
            """)
        
        with col2:
            st.markdown("""
            #### Inspiration
            - ✓ Right hemidiaphragm at 6th anterior rib
            - ✓ Or 10th posterior rib at mid-clavicular line
            - ✓ Adequate lung expansion
            - ✓ Costophrenic angles visible
            
            #### Motion
            - ✓ Sharp rib cortices
            - ✓ Sharp vessel margins
            - ✓ Sharp diaphragm contours
            - ✓ No cardiac border blurring
            """)
    
    with tab2:
        st.subheader("Systematic Anatomic Review")
        
        regions = {
            "🦴 Chest Wall": {
                "desc": "Check symmetry, rib integrity, soft tissues, breast shadows",
                "details": [
                    "Evaluate rib fractures, lytic or blastic lesions",
                    "Assess soft tissue emphysema",
                    "Check breast shadows (bilateral, symmetric)",
                    "Look for surgical clips or previous surgery"
                ]
            },
            "❤️ Mediastinum": {
                "desc": "Heart size/shape, aortic arch, SVC, lines/stripes",
                "details": [
                    "Cardiothoracic ratio (normal <50% on PA view)",
                    "Aortic knob contour and calcification",
                    "Mediastinal widening or mass",
                    "Tracheal deviation"
                ]
            },
            "🔗 Hila": {
                "desc": "Right normally lower than left, assess size/density",
                "details": [
                    "Hilar point: right at 6th rib, left at 5th rib",
                    "Hilar overlay sign for masses",
                    "Lymphadenopathy evaluation",
                    "Vascular vs mass density"
                ]
            },
            "🫁 Lungs": {
                "desc": "Volumes, vascularity, opacities (air space vs interstitial)",
                "details": [
                    "Hyperinflation vs atelectasis",
                    "Air space vs interstitial patterns",
                    "Distribution: upper, lower, peripheral, central",
                    "Cavitation, nodules, masses"
                ]
            },
            "🌬️ Airways": {
                "desc": "Trachea position, bronchi, bronchiectasis signs",
                "details": [
                    "Tracheal deviation or narrowing",
                    "Bronchial wall thickening",
                    "Air bronchograms",
                    "Bronchiectasis (tramtrack sign)"
                ]
            },
            "💧 Pleura": {
                "desc": "Effusions (meniscus sign), pneumothorax (pleural line)",
                "details": [
                    "Blunted costophrenic angles",
                    "Meniscus sign for effusion",
                    "Pleural line for pneumothorax",
                    "Pleural thickening or calcification"
                ]
            }
        }
        
        for region, info in regions.items():
            with st.expander(f"{region}"):
                st.write(f"**Overview:** {info['desc']}")
                st.write("**Key Points:**")
                for detail in info['details']:
                    st.write(f"- {detail}")
    
    with tab3:
        st.subheader("Pattern-Based Differential Diagnosis")
        
        patterns = {
            "Reticular + Basal": {
                "dd": ["UIP/IPF", "NSIP", "Asbestosis", "Collagen vascular disease"],
                "desc": "Fine linear opacities, predominantly lower lobes"
            },
            "Nodular + Upper Zone": {
                "dd": ["Tuberculosis", "Sarcoidosis", "Silicosis", "Langerhans cell histiocytosis"],
                "desc": "Small nodules, upper lobe predominance"
            },
            "Perihilar": {
                "dd": ["Sarcoidosis", "Lymphoma", "Pulmonary edema", "Kaposi sarcoma"],
                "desc": "Central distribution around hila"
            },
            "Air Space (Consolidation)": {
                "dd": ["Pneumonia", "Pulmonary edema", "Hemorrhage", "Lipoid pneumonia"],
                "desc": "Fluffy opacities with air bronchograms"
            },
            "Miliary": {
                "dd": ["Tuberculosis", "Fungal infection", "Metastases", "Sarcoidosis"],
                "desc": "Diffuse tiny nodules (1-3mm)"
            },
            "Cavitary": {
                "dd": ["Tuberculosis", "Lung abscess", "Squamous cell cancer", "Wegener's"],
                "desc": "Thick or thin-walled cavities"
            }
        }
        
        for pattern, info in patterns.items():
            with st.expander(f"📊 {pattern}"):
                st.write(f"**Description:** {info['desc']}")
                st.write("**Differential Diagnosis:**")
                for dx in info['dd']:
                    st.write(f"- {dx}")
    
    with tab4:
        st.subheader("Quick Clinical Tips")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### Remember ABC
            - **A**irways
            - **B**reathing (lungs)
            - **C**irculation (heart, vessels)
            
            #### Silhouette Sign
            Loss of normal border = adjacent density
            - Right heart border → RML
            - Left heart border → Lingula
            - Diaphragm → Lower lobes
            
            #### Air Bronchogram
            Air-filled bronchi visible in consolidated lung
            = Air space disease, NOT interstitial
            """)
        
        with col2:
            st.markdown("""
            #### Golden S Sign
            RUL collapse with hilar mass
            (S-shaped configuration)
            
            #### Sail Sign
            LUL collapse in children
            (thymus displaced forward)
            
            #### Hampton's Hump
            Peripheral wedge-shaped opacity
            = Pulmonary infarction/PE
            
            #### Kerley Lines
            - **A lines**: Long, diagonal (upper)
            - **B lines**: Short, horizontal (lower)
            - **C lines**: Reticular (both)
            """)

if __name__ == "__main__":
    main()
