import streamlit as st
import pickle

st.set_page_config(
    page_title="MediScan Mumbai",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# FORCE DARK THEME — override every Streamlit white element
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Sora:wght@400;600;700;800&display=swap');

/* ══ NUCLEAR DARK OVERRIDE — hits every Streamlit container ══ */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="block-container"],
[data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"],
.main, .block-container,
section.main > div,
div[class*="css"] {
    background-color: #080c18 !important;
    background: #080c18 !important;
    color: #e2e8f5 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ══ ROOT VARS ══ */
:root {
  --bg:      #080c18;
  --bg1:     #0e1528;
  --bg2:     #141c35;
  --border:  rgba(99,130,255,0.18);
  --border2: rgba(99,130,255,0.35);
  --blue:    #4f8cff;
  --teal:    #00d4aa;
  --purple:  #a78bfa;
  --red:     #ff5c5c;
  --amber:   #ffab40;
  --green:   #36d399;
  --text1:   #f0f4ff;
  --text2:   #8b9cc8;
  --text3:   #4a5a84;
}

/* ══ STREAMLIT WIDGET BACKGROUNDS ══ */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: #0e1528 !important;
    border: 1.5px solid rgba(79,140,255,0.25) !important;
    border-radius: 10px !important;
    color: #f0f4ff !important;
}
[data-testid="stSelectbox"] svg { color: #4f8cff !important; fill: #4f8cff !important; }

/* Dropdown list */
[data-baseweb="popover"] * {
    background: #0e1528 !important;
    color: #e2e8f5 !important;
}
[data-baseweb="menu"] [role="option"]:hover {
    background: rgba(79,140,255,0.15) !important;
}

/* Slider track */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: #4f8cff !important;
    border: 2px solid #80b0ff !important;
    box-shadow: 0 0 12px rgba(79,140,255,0.6) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div:first-child > div:first-child {
    background: rgba(79,140,255,0.2) !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div:first-child > div:nth-child(2) {
    background: #4f8cff !important;
}

/* Slider value label */
[data-testid="stSlider"] p {
    color: #4f8cff !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}

/* Widget labels */
label[data-testid="stWidgetLabel"] p,
label[data-testid="stWidgetLabel"] {
    color: #8b9cc8 !important;
    font-size: 0.74rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
}

/* ══ BUTTON ══ */
.stButton > button {
    width: 100% !important;
    margin-top: 1.5rem !important;
    padding: 1rem 2rem !important;
    background: linear-gradient(135deg, #4f8cff 0%, #00d4aa 100%) !important;
    color: #fff !important;
    font-family: 'Sora', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 12px !important;
    cursor: pointer !important;
    box-shadow: 0 4px 28px rgba(79,140,255,0.45), 0 2px 8px rgba(0,212,170,0.2) !important;
    transition: all 0.25s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 40px rgba(79,140,255,0.55), 0 4px 16px rgba(0,212,170,0.35) !important;
}

/* ══ HIDE STREAMLIT CHROME ══ */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { visibility: hidden !important; height: 0 !important; }

/* ══ MAIN CONTAINER ══ */
.block-container {
    padding: 0 2.5rem 4rem !important;
    max-width: 1300px !important;
    margin: auto !important;
}

/* ══ SCROLLBAR ══ */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #080c18; }
::-webkit-scrollbar-thumb { background: #4f8cff88; border-radius: 3px; }

/* ══ HR ══ */
hr { border-color: rgba(79,140,255,0.15) !important; }

/* ══ ALL TEXT FORCED ══ */
p, span, div, label, li {
    color: inherit;
}
</style>
""", unsafe_allow_html=True)

# ── Helper to render full-bleed colored HTML safely ──────────────────────────
def html(content): st.markdown(content, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════════════
AREAS = {
    "Dharavi":   {"lat": 19.0400, "lon": 72.8500, "pop": "700K+",  "zone": "Central"},
    "Kurla":     {"lat": 19.0728, "lon": 72.8826, "pop": "500K+",  "zone": "Central-East"},
    "Andheri":   {"lat": 19.1136, "lon": 72.8697, "pop": "1.4M+",  "zone": "Western"},
    "Bandra":    {"lat": 19.0596, "lon": 72.8295, "pop": "300K+",  "zone": "Western"},
    "Dadar":     {"lat": 19.0178, "lon": 72.8478, "pop": "400K+",  "zone": "Central"},
    "Malad":     {"lat": 19.1871, "lon": 72.8483, "pop": "600K+",  "zone": "Western"},
    "Chembur":   {"lat": 19.0527, "lon": 72.8985, "pop": "350K+",  "zone": "Eastern"},
    "Borivali":  {"lat": 19.2317, "lon": 72.8561, "pop": "750K+",  "zone": "Western"},
    "Worli":     {"lat": 19.0136, "lon": 72.8155, "pop": "250K+",  "zone": "Southern"},
    "Govandi":   {"lat": 19.0654, "lon": 72.9247, "pop": "400K+",  "zone": "Eastern"},
}
MONTHS = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
          7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
D_ICON = {"Dengue":"🦟","Malaria":"🦠","Typhoid":"🤒","Cholera":"💧","Leptospirosis":"🌧️","Unknown":"❓"}

def yn(x): return 1 if x=="Yes" else 0

def get_risk(rain, hum, sc):
    if rain>100 and hum>70 and sc>=3: return "HIGH",   "#ff5c5c", "rgba(255,92,92,0.12)",  "rgba(255,92,92,0.4)"
    if sc>=2:                          return "MEDIUM", "#ffab40", "rgba(255,171,64,0.12)", "rgba(255,171,64,0.4)"
    return                                    "LOW",    "#36d399", "rgba(54,211,153,0.12)", "rgba(54,211,153,0.4)"

# ══════════════════════════════════════════════════════════════════════════════
# SATELLITE MAP
# ══════════════════════════════════════════════════════════════════════════════
def sat_map(lat, lon, area, rc, info):
    return f"""<!DOCTYPE html><html><head>
<meta charset="utf-8"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{height:100%;overflow:hidden;background:#080c18}}
  #map{{height:100vh;width:100%}}
  .leaflet-control-zoom{{border:none!important;border-radius:12px!important;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.5)!important}}
  .leaflet-control-zoom a{{
    background:rgba(8,12,24,0.9)!important;backdrop-filter:blur(10px);
    color:#4f8cff!important;border:none!important;
    border-bottom:1px solid rgba(79,140,255,0.15)!important;
    width:36px!important;height:36px!important;line-height:36px!important;font-size:18px!important
  }}
  .leaflet-control-zoom a:hover{{background:rgba(79,140,255,0.25)!important}}
  .leaflet-popup-content-wrapper{{
    background:rgba(8,12,24,0.96)!important;
    border:1px solid rgba(255,255,255,0.1)!important;
    border-top:3px solid {rc}!important;
    border-radius:16px!important;
    box-shadow:0 24px 64px rgba(0,0,0,0.7)!important;
    backdrop-filter:blur(20px);padding:0!important
  }}
  .leaflet-popup-tip-container{{display:none}}
  .leaflet-popup-content{{margin:0!important;padding:0!important;min-width:220px}}
  .pop{{padding:18px 20px;font-family:'Plus Jakarta Sans',system-ui,sans-serif}}
  .pop-title{{font-size:15px;font-weight:800;color:#f0f4ff;margin-bottom:12px;display:flex;align-items:center;gap:8px}}
  .pop-badge{{background:{rc}22;border:1px solid {rc}55;border-radius:6px;padding:2px 9px;font-size:10px;font-weight:700;color:{rc};letter-spacing:0.07em}}
  .pop-grid{{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:10px}}
  .pop-cell{{background:rgba(255,255,255,0.04);border-radius:10px;padding:9px 11px}}
  .pop-k{{font-size:9px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:rgba(255,255,255,0.3);margin-bottom:3px}}
  .pop-v{{font-size:13px;font-weight:700;color:rgba(255,255,255,0.85)}}
  .pop-coord{{font-size:10.5px;font-family:'Courier New',monospace;color:rgba(255,255,255,0.35);
    background:rgba(255,255,255,0.03);border-radius:8px;padding:8px 11px;letter-spacing:0.05em}}
  .cbar{{position:absolute;bottom:14px;left:50%;transform:translateX(-50%);z-index:800;
    background:rgba(8,12,24,0.88);backdrop-filter:blur(16px);
    border:1px solid rgba(255,255,255,0.1);border-radius:20px;
    padding:7px 18px;font-size:11px;font-family:'Courier New',monospace;
    color:rgba(255,255,255,0.45);white-space:nowrap;letter-spacing:0.05em;
    box-shadow:0 4px 24px rgba(0,0,0,0.35)}}
  .cbar span{{color:{rc};font-weight:700}}
</style>
</head><body>
<div class="cbar" id="cb"><span>●</span> {lat:.5f}°N &nbsp; {lon:.5f}°E &nbsp; <span>{area}</span></div>
<div id="map"></div>
<script>
var map=L.map('map',{{center:[{lat},{lon}],zoom:14,zoomControl:true,attributionControl:false}});
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}',{{maxZoom:19}}).addTo(map);
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{{z}}/{{y}}/{{x}}',{{maxZoom:19,opacity:0.9}}).addTo(map);
L.circle([{lat},{lon}],{{radius:1100,color:'{rc}',fillColor:'{rc}',fillOpacity:0.04,weight:1.5,dashArray:'10 6'}}).addTo(map);
L.circle([{lat},{lon}],{{radius:500,color:'{rc}',fillColor:'{rc}',fillOpacity:0.12,weight:0}}).addTo(map);
L.circle([{lat},{lon}],{{radius:200,color:'{rc}',fillColor:'{rc}',fillOpacity:0.28,weight:0}}).addTo(map);
[0,1.1,2.2].forEach(function(d){{
  var ic=L.divIcon({{className:'',iconSize:[0,0],iconAnchor:[0,0],
    html:'<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="overflow:visible;position:absolute;">'
      +'<circle cx="0" cy="0" r="0" fill="none" stroke="{rc}" stroke-width="2" opacity="0">'
      +'<animate attributeName="r" values="40;420" dur="3.2s" begin="'+d+'s" repeatCount="indefinite"/>'
      +'<animate attributeName="opacity" values="0.8;0" dur="3.2s" begin="'+d+'s" repeatCount="indefinite"/>'
      +'</circle></svg>'
  }});
  L.marker([{lat},{lon}],{{icon:ic,interactive:false,zIndexOffset:-200}}).addTo(map);
}});
var mk=L.divIcon({{className:'',iconSize:[40,40],iconAnchor:[20,20],
  html:`<div style="width:40px;height:40px;position:relative;transform:translate(-50%,-50%)">
    <div style="position:absolute;inset:0;border-radius:50%;border:2.5px solid {rc};
      box-shadow:0 0 0 4px rgba(8,12,24,0.9),0 0 24px {rc}99;
      animation:rot 5s linear infinite;
      background:conic-gradient(transparent 0deg, {rc}33 180deg, transparent 360deg)"></div>
    <div style="position:absolute;inset:8px;border-radius:50%;background:rgba(8,12,24,0.95)"></div>
    <div style="position:absolute;inset:14px;border-radius:50%;background:{rc};box-shadow:0 0 14px {rc}"></div>
  </div><style>@keyframes rot{{to{{transform:translate(-50%,-50%) rotate(360deg)}}}}</style>`
}});
L.marker([{lat},{lon}],{{icon:mk}}).addTo(map)
  .bindPopup(`<div class="pop">
    <div class="pop-title">📍 {area} <span class="pop-badge">{info['zone']}</span></div>
    <div class="pop-grid">
      <div class="pop-cell"><div class="pop-k">Population</div><div class="pop-v">{info['pop']}</div></div>
      <div class="pop-cell"><div class="pop-k">Risk Zone</div><div class="pop-v" style="color:{rc}">■ Active</div></div>
    </div>
    <div class="pop-coord">{lat:.6f}°N &nbsp;&nbsp; {lon:.6f}°E</div>
  </div>`).openPopup();
map.on('mousemove',function(e){{
  document.getElementById('cb').innerHTML='<span>●</span> '+e.latlng.lat.toFixed(5)+'°N &nbsp; '+e.latlng.lng.toFixed(5)+'°E &nbsp; <span>{area}</span>';
}});
</script></body></html>"""

# ── Model ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        with open("model.pkl","rb") as f: return pickle.load(f)
    except: return None
model = load_model()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE — HERO
# ══════════════════════════════════════════════════════════════════════════════
html("""
<div style="
  padding: 3rem 0 2rem;
  margin-bottom: 1.5rem;
  position: relative;
  background: linear-gradient(180deg, rgba(79,140,255,0.07) 0%, transparent 100%);
  border-bottom: 1px solid rgba(79,140,255,0.15);
">
  <!-- animated bg orbs -->
  <div style="position:absolute;top:-60px;left:-80px;width:400px;height:400px;
    border-radius:50%;
    background:radial-gradient(circle, rgba(79,140,255,0.12) 0%, transparent 70%);
    pointer-events:none;animation:orb1 10s ease-in-out infinite alternate;"></div>
  <div style="position:absolute;top:0;right:-60px;width:300px;height:300px;
    border-radius:50%;
    background:radial-gradient(circle, rgba(0,212,170,0.09) 0%, transparent 70%);
    pointer-events:none;animation:orb2 12s ease-in-out infinite alternate;"></div>

  <style>
    @keyframes orb1 { from{transform:translate(0,0)} to{transform:translate(30px,-20px)} }
    @keyframes orb2 { from{transform:translate(0,0)} to{transform:translate(-20px,25px)} }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }
  </style>

  <!-- eyebrow pill -->
  <div style="display:inline-flex;align-items:center;gap:8px;
    background:rgba(79,140,255,0.12);
    border:1px solid rgba(79,140,255,0.35);
    border-radius:999px;padding:5px 14px;margin-bottom:18px;">
    <div style="width:7px;height:7px;border-radius:50%;background:#4f8cff;
      box-shadow:0 0 10px #4f8cff;animation:blink 1.5s infinite;"></div>
    <span style="font-size:0.72rem;font-weight:700;color:#4f8cff;
      letter-spacing:0.1em;text-transform:uppercase;">
      Live Risk Assessment · Mumbai
    </span>
  </div>

  <!-- main title -->
  <div style="font-family:'Sora',sans-serif;font-size:clamp(2.2rem,4vw,3.6rem);
    font-weight:800;line-height:1.06;letter-spacing:-0.03em;color:#f0f4ff;
    margin-bottom:14px;">
    AI Disease
    <span style="background:linear-gradient(120deg,#4f8cff,#00d4aa,#a78bfa);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
      Outbreak
    </span>
    Predictor
  </div>

  <!-- subtitle -->
  <div style="font-size:1rem;font-weight:400;color:#8b9cc8;
    max-width:520px;line-height:1.65;margin-bottom:22px;">
    Real-time outbreak intelligence powered by machine learning —
    satellite mapping, environmental analysis & instant risk scoring for Mumbai.
  </div>

  <!-- badges row -->
  <div style="display:flex;gap:10px;flex-wrap:wrap;">
    <div style="display:flex;align-items:center;gap:6px;
      background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
      border-radius:8px;padding:6px 14px;font-size:0.78rem;font-weight:600;color:#8b9cc8;">
      🛰 Satellite Imagery
    </div>
    <div style="display:flex;align-items:center;gap:6px;
      background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
      border-radius:8px;padding:6px 14px;font-size:0.78rem;font-weight:600;color:#8b9cc8;">
      🤖 ML-Powered
    </div>
    <div style="display:flex;align-items:center;gap:6px;
      background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
      border-radius:8px;padding:6px 14px;font-size:0.78rem;font-weight:600;color:#8b9cc8;">
      🗺 10 Areas Covered
    </div>
    <div style="display:flex;align-items:center;gap:6px;
      background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
      border-radius:8px;padding:6px 14px;font-size:0.78rem;font-weight:600;color:#8b9cc8;">
      ⚡ Instant Results
    </div>
  </div>
</div>
""")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
left, right = st.columns([1, 1.2], gap="large")

def sh(label):
    """Render a section heading."""
    html(f"""<div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;
      text-transform:uppercase;color:#4a5a84;margin:1.6rem 0 0.85rem;
      display:flex;align-items:center;gap:10px;">
      {label}
      <div style="flex:1;height:1px;background:linear-gradient(90deg,rgba(79,140,255,0.2),transparent);"></div>
    </div>""")

# ── LEFT PANEL ────────────────────────────────────────────────────────────────
with left:
    sh("📍 Location")
    area = st.selectbox("Select Area", list(AREAS.keys()), label_visibility="collapsed")
    info = AREAS[area]

    html(f"""<div style="display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 16px;">
      <span style="background:rgba(79,140,255,0.12);border:1px solid rgba(79,140,255,0.3);
        border-radius:8px;padding:4px 12px;font-size:0.73rem;font-weight:600;color:#4f8cff;">
        🏙 {info['zone']}</span>
      <span style="background:rgba(79,140,255,0.12);border:1px solid rgba(79,140,255,0.3);
        border-radius:8px;padding:4px 12px;font-size:0.73rem;font-weight:600;color:#4f8cff;">
        👥 {info['pop']}</span>
      <span style="background:rgba(79,140,255,0.12);border:1px solid rgba(79,140,255,0.3);
        border-radius:8px;padding:4px 12px;font-size:0.73rem;font-weight:600;color:#4f8cff;">
        📌 {info['lat']:.4f}°N, {info['lon']:.4f}°E</span>
    </div>""")

    sh("🌦 Environment")
    c1, c2 = st.columns(2)
    with c1:
        temp = st.slider("🌡 Temperature °C", 20, 42, 31)
        rain = st.slider("🌧 Rainfall mm",     0, 250, 60)
    with c2:
        hum   = st.slider("💧 Humidity %",  30, 100, 72)
        month = st.slider("📅 Month",         1,  12,  6)

    sh("🩺 Symptoms")
    sc1, sc2 = st.columns(2)
    with sc1:
        fever     = st.selectbox("Fever",      ["No","Yes"])
        headache  = st.selectbox("Headache",   ["No","Yes"])
        body_pain = st.selectbox("Body Pain",  ["No","Yes"])
    with sc2:
        cough   = st.selectbox("Cough",        ["No","Yes"])
        stomach = st.selectbox("Stomach Pain", ["No","Yes"])

    syms = {"Fever":fever,"Headache":headache,"Body Pain":body_pain,"Cough":cough,"Stomach":stomach}
    chips = "".join([
        f"""<span style="padding:5px 13px;border-radius:20px;font-size:0.73rem;font-weight:600;
          {'background:rgba(255,92,92,0.18);border:1px solid rgba(255,92,92,0.5);color:#ff7070;box-shadow:0 0 10px rgba(255,92,92,0.15)'
           if v=='Yes' else
           'background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);color:#4a5a84'}">
          {k}</span>"""
        for k,v in syms.items()
    ])
    html(f'<div style="display:flex;gap:7px;flex-wrap:wrap;margin-top:12px;">{chips}</div>')

    btn = st.button("🔍  Analyse Outbreak Risk")

# ── RIGHT PANEL ───────────────────────────────────────────────────────────────
with right:
    if btn:
        inp   = [[temp, hum, rain, yn(fever), yn(headache), yn(body_pain), yn(cough), yn(stomach), month]]
        score = sum(inp[0][3:8])
        rl, rc, rcbg, rcborder = get_risk(rain, hum, score)

        if model:
            pred = model.predict(inp)[0]
        else:
            pred = {5:"Dengue",4:"Malaria",3:"Typhoid",2:"Leptospirosis"}.get(
                score, "Cholera" if stomach=="Yes" else "Unknown")

        dicon = D_ICON.get(pred,"🦠")

        # ── Result cards
        sh("📊 Results")
        html(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:14px;">
          <!-- Disease card -->
          <div style="border-radius:14px;padding:18px 20px;
            background:linear-gradient(135deg,rgba(79,140,255,0.14),rgba(79,140,255,0.04));
            border:1px solid rgba(79,140,255,0.3);
            box-shadow:0 4px 24px rgba(79,140,255,0.1);
            position:relative;overflow:hidden;">
            <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,transparent,#4f8cff,transparent);"></div>
            <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.14em;
              text-transform:uppercase;color:#4a5a84;margin-bottom:8px;">
              Predicted Disease
            </div>
            <div style="font-family:'Sora',sans-serif;font-size:1.5rem;font-weight:700;
              color:#4f8cff;line-height:1.1;">
              {dicon} {pred}
            </div>
          </div>
          <!-- Risk card -->
          <div style="border-radius:14px;padding:18px 20px;
            background:{rcbg};border:1px solid {rcborder};
            box-shadow:0 4px 24px {rcbg};
            position:relative;overflow:hidden;
            {'animation:riskpulse 2.5s ease-in-out infinite;' if rl=='HIGH' else ''}">
            <style>@keyframes riskpulse{{0%,100%{{box-shadow:0 4px 24px {rcbg}}}50%{{box-shadow:0 4px 40px {rcborder}}}}}</style>
            <div style="position:absolute;top:0;left:0;right:0;height:2px;
              background:linear-gradient(90deg,transparent,{rc},transparent);"></div>
            <div style="font-size:0.65rem;font-weight:700;letter-spacing:0.14em;
              text-transform:uppercase;color:#4a5a84;margin-bottom:8px;">
              Risk Level
            </div>
            <div style="font-family:'Sora',sans-serif;font-size:1.5rem;font-weight:700;
              color:{rc};line-height:1.1;">
              {rl}
            </div>
          </div>
        </div>
        """)

        # ── Metric pills
        html(f"""<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;">
          {"".join([
            f'<span style="background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:5px 12px;font-size:0.76rem;font-weight:600;color:#8b9cc8;">{x}</span>'
            for x in [f"🌡 {temp}°C", f"💧 {hum}%", f"🌧 {rain}mm", f"📅 {MONTHS[month]}", f"🩺 {score}/5 Sx"]
          ])}
        </div>""")

        # ── Satellite map
        sh("🛰 Satellite Map")
        html(f"""
        <div style="border-radius:16px;overflow:hidden;
          border:1px solid rgba(255,255,255,0.12);
          box-shadow:0 20px 60px rgba(0,0,0,0.5),0 0 0 1px rgba(255,255,255,0.04);">
          <div style="display:flex;align-items:center;justify-content:space-between;
            background:rgba(8,12,24,0.95);backdrop-filter:blur(12px);
            padding:10px 16px;border-bottom:1px solid rgba(255,255,255,0.08);">
            <div style="display:flex;align-items:center;gap:8px;
              font-size:0.76rem;font-weight:600;color:#8b9cc8;">
              <div style="width:8px;height:8px;border-radius:50%;background:{rc};
                box-shadow:0 0 8px {rc};animation:blink 1.5s infinite;"></div>
              Esri World Imagery · Satellite View · {area}
            </div>
            <span style="font-size:0.72rem;font-weight:700;color:{rc};
              background:{rcbg};border:1px solid {rcborder};
              border-radius:6px;padding:3px 10px;letter-spacing:0.06em;">
              {rl} RISK
            </span>
          </div>
        """)
        st.components.v1.html(sat_map(info["lat"], info["lon"], area, rc, info), height=420, scrolling=False)
        html("</div>")

        # ── Advisory
        adv_map = {
            "HIGH":   f"⛔ <strong style='color:{rc}'>Critical Outbreak Alert — {area}</strong><br>"
                      "High probability of disease outbreak. Seek immediate medical attention. Avoid stagnant water, "
                      "use only purified drinking water, and maintain strict hygiene. "
                      f"Call MCGM Health Helpline <strong style='color:#f0f4ff'>1916</strong>.",
            "MEDIUM": f"⚠️ <strong style='color:{rc}'>Elevated Risk Detected — {area}</strong><br>"
                      "Moderate risk identified. Monitor all symptoms closely and maintain personal hygiene. "
                      "Visit your nearest PHC or clinic if condition worsens.",
            "LOW":    f"✅ <strong style='color:{rc}'>Low Risk — {area}</strong><br>"
                      "Environmental and symptom parameters are within normal range. Continue standard hygiene practices "
                      "and stay alert especially during the monsoon season.",
        }[rl]

        html(f"""
        <div style="border-radius:12px;padding:14px 18px;margin-top:12px;
          font-size:0.88rem;font-weight:500;line-height:1.72;color:#8b9cc8;
          background:{rcbg};
          border:1px solid {rcborder};border-left:3px solid {rc};">
          {adv_map}
        </div>""")

    else:
        html("""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;
          min-height:540px;text-align:center;
          background:rgba(255,255,255,0.025);
          border:1px dashed rgba(79,140,255,0.2);
          border-radius:20px;margin-top:1.6rem;padding:3rem 2rem;">
          <div style="width:84px;height:84px;border-radius:50%;
            background:linear-gradient(135deg,rgba(79,140,255,0.15),rgba(0,212,170,0.1));
            border:1px solid rgba(79,140,255,0.25);
            display:flex;align-items:center;justify-content:center;
            font-size:2.2rem;margin-bottom:18px;
            box-shadow:0 0 40px rgba(79,140,255,0.1);">
            🏥
          </div>
          <div style="font-family:'Sora',sans-serif;font-size:1.15rem;font-weight:700;
            color:rgba(240,244,255,0.5);margin-bottom:8px;">
            Ready to Analyse
          </div>
          <div style="font-size:0.85rem;color:#4a5a84;max-width:250px;line-height:1.75;">
            Configure location, environment &amp; symptoms on the left — then click Analyse.
          </div>
        </div>""")

# ── Footer ────────────────────────────────────────────────────────────────────
html("""<br>
<div style="height:1px;background:linear-gradient(90deg,transparent,rgba(79,140,255,0.2),transparent);margin-bottom:14px;"></div>
<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;
  font-size:0.73rem;font-weight:500;color:#4a5a84;padding-bottom:1.5rem;">
  <span>MediScan Mumbai &nbsp;·&nbsp; ML-Powered Disease Intelligence &nbsp;·&nbsp; v3.0</span>
  <span>⚕ Informational use only — consult a qualified medical professional</span>
</div>""")