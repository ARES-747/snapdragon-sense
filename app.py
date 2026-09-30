import os
import json
import requests
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Snapdragon Sense", page_icon="🧭", layout="wide")

NAVY = "#0B1220"
CYAN = "#55D6FF"
GREEN = "#8CE99A"
st.markdown("""
<style>
.stApp {background: linear-gradient(135deg, #0b1220 0%, #111d32 100%); color: #eef5ff;}
h1, h2, h3 {color: #f4f8ff !important;}
div[data-testid="stMetric"] {background: #17243a; border: 1px solid #2c4262; padding: 14px; border-radius: 12px;}
div.stButton > button {background: #55D6FF; color: #08111f; border: 0; border-radius: 9px; font-weight: 700;}
.small-note {color: #b8c6dc; font-size: 0.88rem;}
</style>
""", unsafe_allow_html=True)

st.title("🧭 Snapdragon Sense")
st.subheader("AI-powered laptop troubleshooting assistant")
st.markdown("**Explain the symptoms. Understand likely causes. Choose safer next steps.**")
st.caption("Prototype status: uses user-entered or clearly labelled sample diagnostics. It does not silently monitor your PC or make system changes.")

with st.sidebar:
    st.header("Settings")
    model_mode = st.radio("Analysis mode", ["Local AI (Ollama)", "Guided prototype (no model required)"], index=1)
    ollama_model = st.text_input("Ollama model name", value=os.getenv("OLLAMA_MODEL", "qwen2.5:3b"))
    st.markdown("---")
    st.markdown("**Privacy by design**")
    st.write("No diagnostic text is sent to a remote service by this app. If Local AI is selected, requests go to your local Ollama service on this computer.")
    st.markdown('<p class="small-note">For a future Snapdragon deployment, validate model support and performance on actual Snapdragon-powered HP hardware.</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1.1, 0.9], gap="large")
with col1:
    st.markdown("### 1. Describe the issue")
    issue = st.selectbox("What are you experiencing?", [
        "Battery drains faster than usual",
        "Laptop feels slow",
        "An app crashes or will not open",
        "Laptop freezes or becomes unresponsive",
        "Wi-Fi or Bluetooth is unreliable",
        "Other / mixed symptoms"
    ])
    details = st.text_area("What have you noticed?", height=110, placeholder="Example: Battery fell from 80% to 35% in about 90 minutes while several browser tabs and a video call were open.")
    st.markdown("### 2. Add any diagnostic details you know")
    c1, c2, c3 = st.columns(3)
    with c1:
        battery_drop = st.number_input("Battery drop (%)", min_value=0, max_value=100, value=0, help="Optional. Enter the percentage lost during a known period.")
    with c2:
        duration = st.number_input("Time period (hours)", min_value=0.0, max_value=24.0, value=0.0, step=0.5)
    with c3:
        recent_change = st.selectbox("Recent change?", ["Not sure", "Windows update", "New app or driver", "Changed settings", "No known change"])
    sample = st.checkbox("Use sample diagnostic details for a quick demo")
    if sample:
        issue = "Battery drains faster than usual"
        details = "Battery dropped from 82% to 44% during a 2-hour video call with a browser, chat app, and cloud sync running. The laptop felt warmer than usual."
        battery_drop = 38
        duration = 2.0
        recent_change = "Windows update"

with col2:
    st.markdown("### What this prototype can do")
    st.markdown("""
- Turn symptoms into a clear troubleshooting summary
- Suggest low-risk checks before disruptive actions
- Explain what evidence is missing
- Use a local open-source model if Ollama is configured
""")
    st.info("This is decision support, not a hardware diagnostic tool. Recommendations are hypotheses until confirmed by system data or a qualified technician.")

def safe_guided_analysis(issue, details, battery_drop, duration, recent_change):
    tips = []
    cause = "The available details are not enough to identify one confirmed cause."
    if issue == "Battery drains faster than usual":
        cause = "Possible causes include high background activity, screen brightness, video calls, sync/download tasks, or a recent update. The data entered does not prove which cause is responsible."
        tips = [
            "Open Windows Settings → System → Power & battery and review battery usage by app.",
            "Check Task Manager for high CPU/GPU use and unexpected background processes.",
            "If this started after an update, check whether updates or cloud sync are still running; reassess after they finish.",
            "Compare battery use during a similar workload with brightness and connected devices held roughly constant."
        ]
        if duration > 0 and battery_drop > 0:
            rate = battery_drop / duration
            tips.insert(0, f"Your entered figures imply about {rate:.1f} percentage points of battery use per hour. This is a simple estimate, not a battery-health measurement.")
    elif issue == "Laptop feels slow":
        cause = "Possible causes include a busy background process, low free storage, memory pressure, thermal throttling, or a recent software change."
        tips = [
            "Open Task Manager and sort Processes by CPU, Memory, and Disk to find unusually busy processes.",
            "Check free storage and close apps you do not need.",
            "Restart once if the system has been running for a long time, then compare performance.",
            "Install app and driver updates only from trusted official sources."
        ]
    elif issue == "An app crashes or will not open":
        cause = "Possible causes include an app bug, damaged settings, missing dependencies, a driver issue, or processor-architecture compatibility. This prototype cannot confirm compatibility without a verified app record."
        tips = [
            "Record the app name, version, and exact error message.",
            "Check the app publisher's official system requirements and update history.",
            "Try the app's built-in repair/reset option if available, after saving your work.",
            "Avoid downloading unofficial replacement DLLs or drivers."
        ]
    elif issue == "Laptop freezes or becomes unresponsive":
        cause = "Possible causes include a misbehaving process, driver issue, overheating, memory pressure, or an operating-system fault."
        tips = [
            "Save work frequently and note whether the freeze happens with one specific app.",
            "Check Windows Reliability Monitor for errors around the time of the freeze.",
            "Check ventilation and whether the laptop is unusually hot.",
            "Install updates from Windows Update and official device support pages."
        ]
    elif issue == "Wi-Fi or Bluetooth is unreliable":
        cause = "Possible causes include signal interference, router issues, power-management settings, or a wireless driver problem."
        tips = [
            "Check whether the issue affects other devices on the same network.",
            "Restart the router only if you control it and can safely do so.",
            "Check Windows network diagnostics and official driver updates.",
            "Note whether the problem appears only after sleep or on a specific network."
        ]
    else:
        tips = [
            "Write down the exact symptom, when it began, and whether it happens repeatedly.",
            "Record any error message and the app or task involved.",
            "Change one setting at a time so you can tell what helped.",
            "Back up important files before attempting major troubleshooting."
        ]
    if recent_change == "Windows update":
        tips.append("Because you noted a recent Windows update, check Windows Update history and whether related app or driver updates are pending. Do not uninstall updates without a clear reason.")
    elif recent_change == "New app or driver":
        tips.append("If the issue began immediately after a new app or driver, check its official release notes and consider the vendor's supported rollback path.")
    return {"summary": cause, "recommendations": tips}

def ask_ollama(model, prompt):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2}
    }
    response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=90)
    response.raise_for_status()
    return response.json().get("response", "").strip()

if st.button("Analyse my issue", type="primary", use_container_width=True):
    if not details.strip():
        st.warning("Please add a short description of what happened, or select the sample demo details.")
    else:
        context = {
            "symptom": issue,
            "user_description": details,
            "battery_drop_percent": battery_drop if battery_drop else "not provided",
            "duration_hours": duration if duration else "not provided",
            "recent_change": recent_change,
            "time_created": datetime.now().isoformat(timespec="minutes")
        }
        guided = safe_guided_analysis(issue, details, battery_drop, duration, recent_change)
        st.markdown("---")
        st.markdown("## Troubleshooting report")
        st.markdown(f"**Symptom:** {issue}")
        st.markdown(f"**Initial assessment:** {guided['summary']}")
        if model_mode == "Local AI (Ollama)":
            prompt = f"""You are a cautious laptop troubleshooting assistant. Use only the user-provided information below.
Do not claim to have measured the computer, read telemetry, verified app compatibility, or fixed anything.
Clearly separate possibilities from confirmed facts. Give 3-5 low-risk next steps, explain uncertainty, and never recommend disabling security tools or downloading unofficial drivers.
User-provided information:
{json.dumps(context, indent=2)}
Prototype heuristic notes:
{json.dumps(guided, indent=2)}
Respond in simple language with headings: What might be happening; What to check next; What not to assume."""
            try:
                with st.spinner("Contacting the local Ollama model on this computer..."):
                    answer = ask_ollama(ollama_model, prompt)
                st.markdown("### Local AI explanation")
                st.write(answer)
                st.caption(f"Model requested: {ollama_model}. Confirm Ollama is running and the model is installed.")
            except Exception as e:
                st.error("Local AI could not be reached. Showing the guided prototype analysis instead.")
                st.caption("To enable local AI, install Ollama, pull a compatible model, and start the local service.")
                st.caption(f"Technical detail: {type(e).__name__}")
                st.markdown("### Recommended checks")
                for tip in guided["recommendations"]:
                    st.markdown(f"- {tip}")
        else:
            st.markdown("### Recommended checks")
            for tip in guided["recommendations"]:
                st.markdown(f"- {tip}")
        st.markdown("### Confidence and limitations")
        st.write("This is an initial triage, not a confirmed diagnosis. The assistant uses only the details you supplied. Check official support resources before making major changes.")
        st.success("No system settings were changed by this prototype.")

st.markdown("---")
st.markdown("**Prototype roadmap:** integrate supported Windows diagnostic sources, validate a small open-source model on Snapdragon-powered HP hardware, and measure response quality, latency, and power use.")
st.caption("Snapdragon Sense is an independent prototype concept for the challenge. It is not an official Qualcomm or HP product.")
