import streamlit as st
from PIL import Image
from predictor import DiseasePredictor

st.set_page_config(
    page_title="LeafAI — Plant Disease Detection",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css()

@st.cache_resource
def load_predictor():
    return DiseasePredictor()

try:
    predictor = load_predictor()
    models_loaded = True
except Exception as e:
    models_loaded = False

diseases_db = {
    "tomato bacterial spot": {"name":"Tomato Bacterial Spot","crop":"Tomato","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Bacterium: Xanthomonas vesicatoria","symptoms":"Small dark water-soaked spots on leaves turning brown with yellow halo.","treatment":["Apply copper-based bactericide every 7 days","Remove infected plant parts immediately","Avoid working with plants when wet","Use streptomycin spray in severe cases"],"prevention":["Use certified disease-free seeds","Avoid overhead irrigation","Rotate crops every season","Disinfect tools regularly"],"fertilizer":["Apply Calcium-rich fertilizer to strengthen cell walls","Use balanced NPK 20-20-20 fertilizer","Avoid excessive Nitrogen","Apply foliar spray of Potassium to boost immunity"]},
    "tomato early blight": {"name":"Tomato Early Blight","crop":"Tomato","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 3 days","cause":"Fungus: Alternaria solani","symptoms":"Brown spots with yellow rings on lower leaves. Leaves turn yellow and drop.","treatment":["Remove infected leaves immediately","Spray Chlorothalonil fungicide every 7 days","Apply copper-based fungicide as alternative","Water at base only"],"prevention":["Rotate crops every season","Plant resistant varieties","Proper spacing for air circulation","Remove plant debris after harvest"],"fertilizer":["Apply Potassium fertilizer to boost plant immunity","Use NPK 15-15-15 balanced fertilizer","Avoid excessive Nitrogen fertilizer","Apply Calcium and Magnesium foliar spray"]},
    "tomato late blight": {"name":"Tomato Late Blight","crop":"Tomato","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Water mold: Phytophthora infestans","symptoms":"Dark watery spots on leaves and stems. White mold visible underneath.","treatment":["Remove and destroy infected plants immediately","Spray Mancozeb or Metalaxyl every 5-7 days","Do not compost — burn infected plants","Increase spray frequency in wet weather"],"prevention":["Use drip irrigation only","Plant certified disease-free seeds","Ensure good drainage","Monitor during rainy season"],"fertilizer":["Apply Phosphorus fertilizer to strengthen roots","Use Potassium-rich fertilizer to boost immunity","Avoid high Nitrogen fertilizer","Apply Calcium nitrate to strengthen plant tissue"]},
    "tomato leaf mold": {"name":"Tomato Leaf Mold","crop":"Tomato","emoji":"🟡","severity":"Moderate","severity_emoji":"🟡","action":"Act within 5 days","cause":"Fungus: Passalora fulva","symptoms":"Yellow spots on upper leaf surface with olive-green mold on underside.","treatment":["Apply Chlorothalonil or Mancozeb","Improve air circulation","Remove infected leaves","Reduce humidity around plants"],"prevention":["Plant resistant varieties","Space plants properly","Avoid overhead watering","Maintain low humidity"],"fertilizer":["Apply balanced NPK fertilizer","Use Potassium fertilizer to boost resistance","Avoid excessive Nitrogen","Apply micronutrient foliar spray"]},
    "tomato mosaic virus": {"name":"Tomato Mosaic Virus","crop":"Tomato","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Virus: Tomato Mosaic Virus (ToMV)","symptoms":"Mosaic pattern of light and dark green on leaves, stunted growth.","treatment":["Remove and destroy infected plants","Control aphid vectors with insecticide","Disinfect tools with bleach solution","Wash hands before handling plants"],"prevention":["Use virus-free certified seeds","Control insect vectors","Remove infected plants immediately","Avoid tobacco near plants"],"fertilizer":["Apply balanced NPK to maintain plant strength","Use Zinc and Boron foliar spray","Avoid excessive Nitrogen","Apply Potassium to boost overall immunity"]},
    "tomato septoria leaf spot": {"name":"Tomato Septoria Leaf Spot","crop":"Tomato","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 3 days","cause":"Fungus: Septoria lycopersici","symptoms":"Small circular spots with dark borders and light grey centers on leaves.","treatment":["Apply Chlorothalonil or copper fungicide","Remove infected lower leaves","Spray every 7-10 days","Avoid wetting foliage when watering"],"prevention":["Rotate crops for 2 years","Use mulch to prevent soil splash","Space plants for good airflow","Remove crop debris"],"fertilizer":["Apply Potassium fertilizer to boost resistance","Use balanced NPK 15-15-15","Avoid high Nitrogen fertilizer","Apply Calcium foliar spray"]},
    "tomato spider mites": {"name":"Tomato Spider Mites","crop":"Tomato","emoji":"🟡","severity":"Moderate","severity_emoji":"🟡","action":"Act within 5 days","cause":"Pest: Tetranychus urticae","symptoms":"Yellow stippling on leaves, fine webbing on underside. Leaves turn bronze.","treatment":["Apply miticide or insecticidal soap","Spray neem oil every 5 days","Increase humidity around plants","Remove heavily infested leaves"],"prevention":["Monitor regularly","Avoid water stress","Remove infested leaves","Use reflective mulch"],"fertilizer":["Apply Silicon fertilizer to strengthen leaves","Use balanced NPK fertilizer","Apply Potassium to boost plant immunity","Avoid excessive Nitrogen"]},
    "tomato target spot": {"name":"Tomato Target Spot","crop":"Tomato","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 3 days","cause":"Fungus: Corynespora cassiicola","symptoms":"Brown spots with concentric rings resembling a target on leaves and fruits.","treatment":["Apply Chlorothalonil or Mancozeb fungicide","Remove infected plant material","Spray every 7-14 days","Improve air circulation"],"prevention":["Use disease-free transplants","Rotate crops regularly","Avoid overhead irrigation","Remove crop debris"],"fertilizer":["Apply Potassium-rich fertilizer","Use NPK 15-15-15 balanced fertilizer","Apply Calcium and Boron foliar spray","Avoid excessive Nitrogen"]},
    "tomato yellow leaf curl virus": {"name":"Tomato Yellow Leaf Curl Virus","crop":"Tomato","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Virus transmitted by whitefly Bemisia tabaci","symptoms":"Upward curling and yellowing of leaves, stunted growth, reduced fruit.","treatment":["Remove and destroy infected plants","Apply insecticide to control whiteflies","Use yellow sticky traps","No chemical cure for the virus"],"prevention":["Plant resistant varieties","Use insect-proof screens","Control whitefly with neem oil","Use reflective mulch"],"fertilizer":["Apply balanced NPK to maintain plant strength","Use Potassium fertilizer to boost immunity","Apply Zinc foliar spray","Avoid excessive Nitrogen fertilizer"]},
    "tomato healthy": {"name":"Tomato Healthy","crop":"Tomato","emoji":"🟢","severity":"Healthy","severity_emoji":"🟢","action":"No action needed","cause":"No disease","symptoms":"Plant appears completely healthy.","treatment":["No treatment needed","Continue regular care"],"prevention":["Maintain good soil nutrition","Monitor regularly"],"fertilizer":["Apply balanced NPK 15-15-15 every 2 weeks","Use Calcium and Magnesium foliar spray","Apply Potassium during fruiting stage","Use compost to improve soil health"]},
    "potato early blight": {"name":"Potato Early Blight","crop":"Potato","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 3 days","cause":"Fungus: Alternaria solani","symptoms":"Dark brown spots with concentric rings on older leaves.","treatment":["Apply Chlorothalonil or Mancozeb","Remove infected leaves","Spray every 7-10 days","Avoid overhead irrigation"],"prevention":["Use certified seed potatoes","Rotate crops every 2-3 years","Maintain proper nutrition","Remove crop debris"],"fertilizer":["Apply Potassium fertilizer to boost immunity","Use NPK 15-15-15","Avoid excessive Nitrogen","Apply Calcium foliar spray"]},
    "potato late blight": {"name":"Potato Late Blight","crop":"Potato","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Water mold: Phytophthora infestans","symptoms":"Water-soaked spots turning brown. White mold on undersides. Tubers rot.","treatment":["Apply Metalaxyl or Cymoxanil immediately","Remove all infected material","Harvest early if severe","Spray preventively in wet weather"],"prevention":["Plant resistant varieties","Avoid poorly drained fields","Use certified seed potatoes","Monitor weather forecasts"],"fertilizer":["Apply Phosphorus to strengthen roots","Use Potassium-rich fertilizer","Avoid high Nitrogen","Apply Calcium nitrate"]},
    "potato healthy": {"name":"Potato Healthy","crop":"Potato","emoji":"🟢","severity":"Healthy","severity_emoji":"🟢","action":"No action needed","cause":"No disease","symptoms":"Plant appears completely healthy.","treatment":["No treatment needed"],"prevention":["Maintain good soil health","Monitor regularly"],"fertilizer":["Apply NPK 15-15-15 fertilizer","Use Potassium during tuber formation","Apply Calcium and Magnesium","Use compost to improve soil"]},
    "corn common rust": {"name":"Corn Common Rust","crop":"Corn/Maize","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 5 days","cause":"Fungus: Puccinia sorghi","symptoms":"Small golden-brown pustules scattered on both leaf surfaces.","treatment":["Apply Propiconazole or Azoxystrobin","Spray at first sign of disease","Repeat application every 14 days","Remove heavily infected plants"],"prevention":["Plant rust-resistant corn varieties","Plant early to avoid peak rust season","Monitor fields regularly","Maintain good crop nutrition"],"fertilizer":["Apply Potassium fertilizer to boost resistance","Use NPK 15-15-15","Avoid excessive Nitrogen","Apply Silicon fertilizer to strengthen leaves"]},
    "corn northern leaf blight": {"name":"Corn Northern Leaf Blight","crop":"Corn/Maize","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 3 days","cause":"Fungus: Exserohilum turcicum","symptoms":"Long tan-grey cigar-shaped lesions on leaves.","treatment":["Apply Propiconazole or Tebuconazole","Spray at tasseling stage","Remove infected debris","Avoid dense planting"],"prevention":["Plant resistant hybrids","Rotate crops","Till soil to bury debris","Avoid excessive nitrogen"],"fertilizer":["Apply balanced NPK fertilizer","Use Potassium to boost immunity","Avoid excessive Nitrogen","Apply Zinc foliar spray"]},
    "corn cercospora leaf spot": {"name":"Corn Cercospora Leaf Spot","crop":"Corn/Maize","emoji":"🟡","severity":"Moderate","severity_emoji":"🟡","action":"Act within 5 days","cause":"Fungus: Cercospora zeae-maydis","symptoms":"Rectangular grey to tan lesions running between leaf veins.","treatment":["Apply Strobilurin or Triazole fungicide","Spray at early disease onset","Improve field drainage","Remove infected residue"],"prevention":["Plant resistant varieties","Rotate crops","Reduce plant density","Avoid minimum tillage"],"fertilizer":["Apply Potassium fertilizer","Use balanced NPK 15-15-15","Apply Zinc and Boron foliar spray","Avoid excessive Nitrogen"]},
    "corn healthy": {"name":"Corn Healthy","crop":"Corn/Maize","emoji":"🟢","severity":"Healthy","severity_emoji":"🟢","action":"No action needed","cause":"No disease","symptoms":"Plant appears completely healthy.","treatment":["No treatment needed"],"prevention":["Maintain good soil health","Monitor regularly"],"fertilizer":["Apply NPK 15-15-15 at planting","Use Urea for top dressing","Apply Zinc foliar spray","Use compost to improve soil"]},
    "rice blast": {"name":"Rice Blast Disease","crop":"Rice","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Fungus: Magnaporthe oryzae","symptoms":"Diamond-shaped lesions with grey centers and brown borders on leaves.","treatment":["Apply Tricyclazole or Isoprothiolane","Spray at booting stage and repeat after 10 days","Drain fields periodically","Remove infected plant debris"],"prevention":["Plant blast-resistant rice varieties","Avoid excessive nitrogen fertilization","Maintain proper water management","Use certified disease-free seeds"],"fertilizer":["Reduce Nitrogen fertilizer application","Apply Silicon fertilizer to strengthen stems","Use Potassium to boost immunity","Apply balanced NPK before blast season"]},
    "rice brown spot": {"name":"Rice Brown Spot","crop":"Rice","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 3 days","cause":"Fungus: Cochliobolus miyabeanus","symptoms":"Oval brown spots with yellow halo on leaves.","treatment":["Apply Mancozeb or Iprodione","Spray at tillering stage","Improve soil fertility","Remove infected debris"],"prevention":["Use certified seeds","Maintain proper nutrition","Avoid water stress","Rotate crops"],"fertilizer":["Apply balanced NPK fertilizer","Improve soil nutrition with compost","Use Zinc fertilizer to correct deficiency","Apply Potassium to boost resistance"]},
    "rice bacterial blight": {"name":"Rice Bacterial Blight","crop":"Rice","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Bacterium: Xanthomonas oryzae","symptoms":"Water-soaked lesions on leaf margins turning yellow then white.","treatment":["Apply copper-based bactericide","Drain fields and keep dry","Remove infected plants","Avoid excessive nitrogen"],"prevention":["Plant resistant varieties","Use certified seeds","Avoid flood irrigation","Maintain field hygiene"],"fertilizer":["Reduce Nitrogen fertilizer immediately","Apply Potassium to boost immunity","Use Silicon fertilizer","Apply balanced NPK after recovery"]},
    "rice sheath blight": {"name":"Rice Sheath Blight","crop":"Rice","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 3 days","cause":"Fungus: Rhizoctonia solani","symptoms":"Oval lesions on leaf sheaths near water line with brown borders.","treatment":["Apply Propiconazole or Hexaconazole","Spray at early tillering","Drain field to reduce humidity","Remove infected stubble"],"prevention":["Reduce plant density","Avoid excessive nitrogen","Use resistant varieties","Rotate crops"],"fertilizer":["Reduce Nitrogen application","Apply Silicon fertilizer","Use Potassium to strengthen stems","Apply balanced NPK at recommended rates"]},
    "rice tungro": {"name":"Rice Tungro Disease","crop":"Rice","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Virus transmitted by green leafhopper","symptoms":"Yellow-orange discoloration of leaves, stunted growth.","treatment":["Control leafhopper with insecticide","Remove infected plants","Use systemic insecticide"],"prevention":["Plant tungro-resistant varieties","Control leafhopper","Synchronize planting dates","Remove infected plants early"],"fertilizer":["Apply balanced NPK to maintain plant strength","Use Zinc foliar spray","Apply Potassium to boost immunity","Avoid excessive Nitrogen"]},
    "rice healthy": {"name":"Rice Healthy","crop":"Rice","emoji":"🟢","severity":"Healthy","severity_emoji":"🟢","action":"No action needed","cause":"No disease","symptoms":"Plant appears completely healthy.","treatment":["No treatment needed"],"prevention":["Maintain good soil health","Monitor regularly"],"fertilizer":["Apply Urea at tillering stage","Use NPK 15-15-15 at planting","Apply Zinc foliar spray","Use compost to improve soil health"]},
    "cassava mosaic": {"name":"Cassava Mosaic Disease","crop":"Cassava","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Virus transmitted by whitefly Bemisia tabaci","symptoms":"Mosaic pattern of yellow and green on leaves, distortion, stunted growth.","treatment":["Remove and destroy infected plants","Control whitefly with insecticide","Use mineral oil spray","No chemical cure"],"prevention":["Plant certified virus-free cuttings","Use mosaic-resistant varieties","Control whitefly with neem","Inspect planting material"],"fertilizer":["Apply balanced NPK to maintain plant strength","Use Potassium to boost immunity","Apply Zinc and Boron foliar spray","Avoid excessive Nitrogen"]},
    "cassava brown streak": {"name":"Cassava Brown Streak Disease","crop":"Cassava","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Virus: Cassava Brown Streak Virus","symptoms":"Yellow patches on leaves, brown streaks on stems, brown patches in tubers.","treatment":["Remove all infected plants","Control whitefly vectors","No chemical treatment","Replace with resistant varieties"],"prevention":["Use CBSD-resistant varieties","Plant certified cuttings","Control whitefly","Avoid moving material from infected areas"],"fertilizer":["Apply balanced NPK fertilizer","Use Potassium to boost plant immunity","Apply micronutrient foliar spray","Avoid excessive Nitrogen"]},
    "cassava bacterial blight": {"name":"Cassava Bacterial Blight","crop":"Cassava","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 3 days","cause":"Bacterium: Xanthomonas axonopodis","symptoms":"Angular water-soaked leaf spots, wilting, stem cankers.","treatment":["Apply copper-based bactericide","Remove infected parts","Disinfect cutting tools","Destroy severely infected plants"],"prevention":["Use disease-free planting material","Disinfect tools","Plant resistant varieties","Avoid infected soil"],"fertilizer":["Apply Calcium fertilizer to strengthen cell walls","Use balanced NPK fertilizer","Avoid excessive Nitrogen","Apply Potassium to boost immunity"]},
    "cassava healthy": {"name":"Cassava Healthy","crop":"Cassava","emoji":"🟢","severity":"Healthy","severity_emoji":"🟢","action":"No action needed","cause":"No disease","symptoms":"Plant appears completely healthy.","treatment":["No treatment needed"],"prevention":["Maintain good soil health","Monitor regularly"],"fertilizer":["Apply NPK 15-15-15 at planting","Use Potassium during tuber formation","Apply Zinc foliar spray","Use compost to improve soil"]},
    "groundnut early leaf spot": {"name":"Groundnut Early Leaf Spot","crop":"Groundnut","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 5 days","cause":"Fungus: Cercospora arachidicola","symptoms":"Dark brown circular spots on upper leaf surface with yellow halo.","treatment":["Spray Chlorothalonil or Mancozeb","Apply every 14 days","Remove infected leaves","Avoid overhead irrigation"],"prevention":["Use certified seeds","Rotate crops","Remove crop debris","Plant resistant varieties"],"fertilizer":["Apply Calcium fertilizer","Use balanced NPK fertilizer","Apply Potassium to boost resistance","Use Gypsum to provide Calcium and Sulfur"]},
    "groundnut late leaf spot": {"name":"Groundnut Late Leaf Spot","crop":"Groundnut","emoji":"🟠","severity":"Moderate-High","severity_emoji":"🟠","action":"Act within 3 days","cause":"Fungus: Cercosporidium personatum","symptoms":"Dark brown to black spots on lower leaf surface.","treatment":["Apply Tebuconazole or Propiconazole","Spray every 14 days","Remove infected material","Improve air circulation"],"prevention":["Rotate crops","Use resistant varieties","Remove crop debris","Avoid dense planting"],"fertilizer":["Apply Calcium and Gypsum","Use balanced NPK fertilizer","Apply Potassium to boost immunity","Avoid excessive Nitrogen"]},
    "groundnut rosette": {"name":"Groundnut Rosette Disease","crop":"Groundnut","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Virus transmitted by aphid Aphis craccivora","symptoms":"Stunted plants with small mottled leaves, chlorotic rosette pattern.","treatment":["Control aphid with insecticide","Remove infected plants","Apply mineral oil to reduce spread"],"prevention":["Plant early","Use resistant varieties","Control aphid with neem","Plant barrier crops"],"fertilizer":["Apply balanced NPK to maintain plant strength","Use Zinc and Boron foliar spray","Apply Potassium to boost immunity","Avoid excessive Nitrogen"]},
    "groundnut rust": {"name":"Groundnut Rust","crop":"Groundnut","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 5 days","cause":"Fungus: Puccinia arachidis","symptoms":"Orange-brown pustules on lower leaf surfaces, yellowing and defoliation.","treatment":["Apply Mancozeb or Propiconazole","Spray every 14 days","Remove infected leaves"],"prevention":["Plant resistant varieties","Rotate crops","Remove crop debris","Monitor fields regularly"],"fertilizer":["Apply Potassium fertilizer to boost resistance","Use balanced NPK","Apply Calcium and Gypsum","Avoid excessive Nitrogen"]},
    "pepper bacterial spot": {"name":"Pepper Bacterial Spot","crop":"Pepper","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 3 days","cause":"Bacterium: Xanthomonas campestris","symptoms":"Small water-soaked spots on leaves turning brown with yellow halo.","treatment":["Apply copper bactericide every 7 days","Remove infected parts","Avoid wet plants"],"prevention":["Use certified seeds","Avoid overhead irrigation","Rotate crops","Disinfect tools"],"fertilizer":["Apply Calcium fertilizer to strengthen cell walls","Use balanced NPK","Avoid excessive Nitrogen","Apply Potassium to boost immunity"]},
    "pepper healthy": {"name":"Pepper Healthy","crop":"Pepper","emoji":"🟢","severity":"Healthy","severity_emoji":"🟢","action":"No action needed","cause":"No disease","symptoms":"Plant appears completely healthy.","treatment":["No treatment needed"],"prevention":["Maintain good soil health","Monitor regularly"],"fertilizer":["Apply NPK 15-15-15 fertilizer","Use Calcium during fruiting","Apply Potassium to improve fruit quality","Use compost to improve soil"]},
    "onion purple blotch": {"name":"Onion Purple Blotch","crop":"Onion","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 3 days","cause":"Fungus: Alternaria porri","symptoms":"Small white lesions with purple centers on leaves enlarging to kill leaves.","treatment":["Apply Mancozeb or Iprodione","Spray every 7-10 days","Remove infected leaves","Improve air circulation"],"prevention":["Use certified disease-free sets","Avoid overhead irrigation","Rotate crops","Remove crop debris"],"fertilizer":["Apply Potassium fertilizer to boost resistance","Use balanced NPK","Apply Calcium foliar spray","Avoid excessive Nitrogen"]},
    "apple scab": {"name":"Apple Scab","crop":"Apple","emoji":"🟠","severity":"Moderate","severity_emoji":"🟡","action":"Act within 5 days","cause":"Fungus: Venturia inaequalis","symptoms":"Olive-green to brown scab-like lesions on leaves and fruits.","treatment":["Apply Myclobutanil or Captan fungicide","Spray from bud break","Remove infected leaves","Prune for air circulation"],"prevention":["Plant resistant varieties","Remove fallen leaves","Apply dormant sprays","Prune for good airflow"],"fertilizer":["Apply balanced NPK fertilizer","Use Calcium to strengthen fruit","Apply Boron foliar spray","Avoid excessive Nitrogen"]},
    "apple black rot": {"name":"Apple Black Rot","crop":"Apple","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Fungus: Botryosphaeria obtusa","symptoms":"Brown circular lesions on leaves, black rotting of fruits, cankers on branches.","treatment":["Apply Captan or Thiophanate-methyl","Remove infected fruits and branches","Spray every 7-10 days","Prune cankers from branches"],"prevention":["Remove mummified fruits","Prune infected branches","Maintain tree vigor","Apply dormant copper spray"],"fertilizer":["Apply Calcium fertilizer","Use balanced NPK fertilizer","Apply Potassium to boost immunity","Avoid excessive Nitrogen"]},
    "grape black rot": {"name":"Grape Black Rot","crop":"Grape","emoji":"🔴","severity":"Severe","severity_emoji":"🔴","action":"Act IMMEDIATELY!","cause":"Fungus: Guignardia bidwellii","symptoms":"Brown circular lesions on leaves, shriveled black mummified berries.","treatment":["Apply Myclobutanil or Mancozeb","Spray from bud break","Remove infected berries","Repeat every 7-14 days"],"prevention":["Remove mummified berries","Prune for good air circulation","Apply early season sprays","Remove infected plant material"],"fertilizer":["Apply Potassium fertilizer","Use balanced NPK","Apply Calcium and Boron foliar spray","Avoid excessive Nitrogen"]},
}

def show_disease_info(info, confidence=None):
    if confidence:
        st.markdown(f"""
        <div class="confidence-wrap">
            <div class="confidence-lbl">AI Confidence Score</div>
            <div class="confidence-val">{confidence:.1f}%</div>
            <div class="confidence-desc">Based on deep learning analysis</div>
        </div>
        """, unsafe_allow_html=True)

    if info['severity'] != 'Healthy':
        st.markdown(f"""
        <div class="severity-wrap">
            <div class="severity-icon">{info['severity_emoji']}</div>
            <div>
                <div class="severity-title">Severity Level</div>
                <div class="severity-level">{info['severity']}</div>
                <div class="severity-action">⏰ {info['action']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="info-box">
        <div class="info-box-header">
            <div class="info-box-title">🔬 Disease Information</div>
        </div>
        <div class="info-field">
            <div class="info-field-label">Disease Name</div>
            <div class="info-field-val">{info['name']}</div>
        </div>
        <div class="info-field">
            <div class="info-field-label">Affected Crop</div>
            <div class="info-field-val">{info['crop']}</div>
        </div>
        <div class="info-field">
            <div class="info-field-label">Cause</div>
            <div class="info-field-val">{info['cause']}</div>
        </div>
        <div class="info-field">
            <div class="info-field-label">Symptoms</div>
            <div class="info-field-val">{info['symptoms']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="info-box"><div class="info-box-header"><div class="info-box-title">💊 Treatment</div></div>', unsafe_allow_html=True)
    for t in info["treatment"]:
        st.markdown(f'<div class="list-item"><span class="dot-green">▸</span><span>{t}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="info-box"><div class="info-box-header"><div class="info-box-title">🛡️ Prevention</div></div>', unsafe_allow_html=True)
    for p in info["prevention"]:
        st.markdown(f'<div class="list-item"><span class="dot-blue">▸</span><span>{p}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="info-box"><div class="info-box-header"><div class="info-box-title">🌱 Fertilizer Recommendation</div></div>', unsafe_allow_html=True)
    for f in info["fertilizer"]:
        st.markdown(f'<div class="list-item"><span class="dot-purple">▸</span><span>{f}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🌿 AI-Powered Agriculture</div>
    <h1>Detect Plant <span>Disease Instantly</span></h1>
    <p>Federal University of Technology Babura &nbsp;·&nbsp;
    Computer Science &nbsp;·&nbsp; 2024/2025</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stat-grid">
    <div class="stat-card"><div class="stat-num">14+</div><div class="stat-label">Crops</div></div>
    <div class="stat-card"><div class="stat-num">47+</div><div class="stat-label">Diseases</div></div>
    <div class="stat-card"><div class="stat-num">95%</div><div class="stat-label">Accuracy</div></div>
    <div class="stat-card"><div class="stat-num">Free</div><div class="stat-label">Always</div></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs([
    "📸  Detect Disease",
    "🔍  Search",
    "🌾  Browse Crops"
])

# ════════════════════════════════════════════════
# TAB 1
# ════════════════════════════════════════════════
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="how-to-box">
        <div class="info-box-header">
            <div class="info-box-title">📖 How It Works</div>
        </div>
        <div class="step-item">
            <div class="step-num">1</div>
            <div class="step-text">Upload a clear close-up photo of a plant leaf</div>
        </div>
        <div class="step-item">
            <div class="step-num">2</div>
            <div class="step-text">Our AI validates the image then detects the disease</div>
        </div>
        <div class="step-item">
            <div class="step-num">3</div>
            <div class="step-text">Read diagnosis, severity, treatment and fertilizer advice</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### ✅ Crops Supported by AI Detection")
    st.markdown("""
    <div>
        <span class="crop-chip">🍎 Apple</span>
        <span class="crop-chip">🫐 Blueberry</span>
        <span class="crop-chip">🍒 Cherry</span>
        <span class="crop-chip">🌽 Corn/Maize</span>
        <span class="crop-chip">🍇 Grape</span>
        <span class="crop-chip">🍊 Orange</span>
        <span class="crop-chip">🍑 Peach</span>
        <span class="crop-chip">🌶️ Pepper</span>
        <span class="crop-chip">🥔 Potato</span>
        <span class="crop-chip">🍓 Raspberry</span>
        <span class="crop-chip">🫘 Soybean</span>
        <span class="crop-chip">🎃 Squash</span>
        <span class="crop-chip">🍓 Strawberry</span>
        <span class="crop-chip">🍅 Tomato</span>
    </div>
    <p style="color:#adb5bd;font-size:0.8rem;margin-top:10px;">
    ⚠️ For Rice, Cassava, Groundnut, Onion — use Search or Browse tab
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop your leaf image here or click to browse",
        type=["jpg","jpeg","png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        col1, col2, col3 = st.columns([1,4,1])
        with col2:
            st.image(image, caption="Uploaded Image", use_column_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        detect_btn = st.button(
            "⚡ ANALYZE DISEASE NOW",
            use_container_width=True,
            type="primary"
        )

        if detect_btn:
            if models_loaded:
                with st.spinner("Stage 1 — Validating image..."):
                    val_result, val_confidence = predictor.validate_leaf(image)

                if val_result == 'not_leaf' and val_confidence > 70:
                    st.markdown("""
                    <div class="result-box result-error">
                        <div class="result-tag tag-orange">❌ Invalid Image</div>
                        <div class="result-title">Not a Plant Leaf</div>
                        <div class="result-sub">
                        Our AI detected this image is not a plant leaf.
                        Please upload a clear leaf photo and try again.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("""
                    <div class="how-to-box">
                        <div class="info-box-header">
                            <div class="info-box-title">💡 Tips for a Good Photo</div>
                        </div>
                        <div class="step-item">
                            <div class="step-num">✓</div>
                            <div class="step-text">Take a close-up photo of the leaf only</div>
                        </div>
                        <div class="step-item">
                            <div class="step-num">✓</div>
                            <div class="step-text">Leaf should fill most of the photo frame</div>
                        </div>
                        <div class="step-item">
                            <div class="step-num">✓</div>
                            <div class="step-text">Use good natural daylight</div>
                        </div>
                        <div class="step-item">
                            <div class="step-num">✗</div>
                            <div class="step-text" style="color:#e53935;">
                            Do NOT upload photos of people, animals, cars or objects
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    with st.spinner("Stage 2 — Analyzing disease..."):
                        result, confidence = predictor.predict_disease(image)

                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("""
                    <div style="margin-bottom:16px;">
                        <span class="stage-badge">✅ Stage 1: Leaf Confirmed</span>
                        <span class="stage-badge">✅ Stage 2: Analysis Complete</span>
                    </div>
                    """, unsafe_allow_html=True)

                    if confidence < 60:
                        st.markdown(f"""
                        <div class="result-box result-warning">
                            <div class="result-tag tag-orange">⚠️ Low Confidence</div>
                            <div class="result-title">Photo Not Clear Enough</div>
                            <div class="result-sub">
                            Confidence score: {confidence:.1f}% —
                            The AI needs a clearer photo for an accurate result.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("""
                        <div class="how-to-box">
                            <div class="info-box-header">
                                <div class="info-box-title">💡 How to Take a Better Photo</div>
                            </div>
                            <div class="step-item">
                                <div class="step-num">✓</div>
                                <div class="step-text">
                                <b>Use natural light</b> — Take photo outside
                                or near a window in daylight</div>
                            </div>
                            <div class="step-item">
                                <div class="step-num">✓</div>
                                <div class="step-text">
                                <b>Get closer</b> — Leaf should fill most
                                of the photo frame</div>
                            </div>
                            <div class="step-item">
                                <div class="step-num">✓</div>
                                <div class="step-text">
                                <b>Hold still</b> — Avoid blurry photos
                                by keeping your hand steady</div>
                            </div>
                            <div class="step-item">
                                <div class="step-num">✓</div>
                                <div class="step-text">
                                <b>Clean lens</b> — Wipe your camera lens
                                before taking the photo</div>
                            </div>
                            <div class="step-item">
                                <div class="step-num">✓</div>
                                <div class="step-text">
                                <b>Show disease clearly</b> — Focus on
                                the sick part of the leaf</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    elif "Healthy" in result:
                        st.markdown(f"""
                        <div class="result-box result-healthy">
                            <div class="result-tag tag-green">✅ Healthy Plant</div>
                            <div class="result-title">{result}</div>
                            <div class="result-sub">
                            Your plant appears completely healthy.
                            Keep monitoring regularly.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        info = diseases_db.get(result.lower())
                        if info:
                            show_disease_info(info, confidence)

                    else:
                        st.markdown(f"""
                        <div class="result-box result-disease">
                            <div class="result-tag tag-red">⚠️ Disease Detected</div>
                            <div class="result-title">{result}</div>
                            <div class="result-sub">
                            Disease found! Follow recommendations below immediately.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        info = diseases_db.get(result.lower())
                        if info:
                            show_disease_info(info, confidence)

            else:
                st.error("❌ Models not loaded. Check your tflite files are in the models/ folder.")

# ════════════════════════════════════════════════
# TAB 2
# ════════════════════════════════════════════════
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Search Any Disease or Crop")
    st.markdown("""
    <p style="color:#6c757d;margin-bottom:20px;">
    Type any crop name, disease name, or symptom
    </p>
    """, unsafe_allow_html=True)

    query = st.text_input(
        "",
        placeholder="🔎  Try: tomato, rice blast, cassava, blight, rust...",
        label_visibility="collapsed"
    )

    if not query:
        st.markdown("""
        <div style="margin-top:12px;">
            <span class="crop-chip">🍅 Tomato</span>
            <span class="crop-chip">🌾 Rice</span>
            <span class="crop-chip">🌿 Cassava</span>
            <span class="crop-chip">🌽 Maize</span>
            <span class="crop-chip">🥜 Groundnut</span>
            <span class="crop-chip">🥔 Potato</span>
            <span class="crop-chip">🌶️ Pepper</span>
            <span class="crop-chip">🍎 Apple</span>
        </div>
        """, unsafe_allow_html=True)

    if query:
        q = query.lower().strip()
        found = [info for key, info in diseases_db.items()
                 if q in key or q in info["name"].lower()
                 or q in info["crop"].lower()
                 or q in info["symptoms"].lower()
                 or q in info["cause"].lower()]

        if found:
            st.markdown(f"""
            <p style="color:#adb5bd;font-size:0.85rem;margin:12px 0;">
            Found {len(found)} result(s) for "{query}"
            </p>
            """, unsafe_allow_html=True)
            for info in found:
                with st.expander(
                    f"{info['emoji']}  {info['name']}  ·  {info['crop']}  ·  {info['severity_emoji']} {info['severity']}"
                ):
                    show_disease_info(info)
        else:
            st.markdown(f"""
            <div class="search-empty">
                <div class="search-empty-title">No results for "{query}"</div>
                <div class="search-empty-sub">
                Try: tomato, potato, rice, cassava, maize,
                groundnut, pepper, onion, apple, grape
                </div>
            </div>
            """, unsafe_allow_html=True)

# ════════════════════════════════════════════════
# TAB 3
# ════════════════════════════════════════════════
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Browse by Crop")
    st.markdown("""
    <p style="color:#6c757d;margin-bottom:20px;">
    Select a crop to see all diseases, treatments and fertilizer advice
    </p>
    """, unsafe_allow_html=True)

    crops = sorted(set(info["crop"] for info in diseases_db.values()))
    crop_emojis = {
        "Apple":"🍎","Cassava":"🌿","Corn/Maize":"🌽",
        "Grape":"🍇","Groundnut":"🥜","Onion":"🧅",
        "Pepper":"🌶️","Potato":"🥔","Rice":"🌾","Tomato":"🍅"
    }

    selected = st.selectbox(
        "",
        ["— Select a crop —"] + crops,
        label_visibility="collapsed"
    )

    if selected != "— Select a crop —":
        matches = [info for info in diseases_db.values() if info["crop"] == selected]
        emoji = crop_emojis.get(selected, "🌿")
        disease_count = len([m for m in matches if "Healthy" not in m["name"]])

        st.markdown(f"""
        <div class="crop-header-box">
            <div class="crop-header-emoji">{emoji}</div>
            <div>
                <div class="crop-header-name">{selected}</div>
                <div class="crop-header-sub">
                {disease_count} diseases · 1 healthy state · Full treatment guide
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        diseases = [m for m in matches if "Healthy" not in m["name"]]
        healthy = [m for m in matches if "Healthy" in m["name"]]

        if diseases:
            st.markdown(f"#### ⚠️ {len(diseases)} Disease(s)")
            for info in diseases:
                with st.expander(
                    f"{info['emoji']}  {info['name']}  ·  {info['severity_emoji']} {info['severity']}"
                ):
                    show_disease_info(info)

        if healthy:
            st.markdown("#### ✅ Healthy State")
            for info in healthy:
                with st.expander(f"🟢  {info['name']}"):
                    show_disease_info(info)

# ── Footer ───────────────────────────────────────
st.markdown("""
<div class="footer-box">
    <div class="footer-logo">🌿 LeafAI</div>
    <div class="footer-text">
        Plant Disease Detection System<br>
        Developed by <b>Yusuf Gambo</b> · Matric: SIT/CSC/23/0005<br>
        B.Sc Computer Science · FUTB · 2024/2025<br>
        Supervised by <b>Dr. Khalid Haruna</b><br><br>
        <a class="footer-link"
        href="https://futb-plant-disease.streamlit.app">
        🌐 futb-plant-disease.streamlit.app</a>
    </div>
</div>
""", unsafe_allow_html=True)