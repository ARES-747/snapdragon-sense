# Snapdragon Sense — AI-Powered Laptop Troubleshooting

A prototype concept for the Snapdragon AI Lab Build & Present Challenge. Snapdragon Sense helps users translate a laptop symptom into cautious, plain-language troubleshooting steps. It is designed with a future on-device deployment on Snapdragon-powered HP PCs in mind.

## Current prototype capabilities

- Simple Streamlit user interface.
- Guided troubleshooting flows for battery drain, slow performance, application crashes, freezes, and wireless connectivity.
- User-entered diagnostics and a clearly labelled sample scenario.
- Optional local AI generation through Ollama (`localhost:11434`); no remote LLM API is used by the app.
- A guided fallback mode that works without a model installed.
- No silent monitoring and no automatic system changes.

## Important current limitations

- This prototype does **not** read live battery telemetry, inspect installed apps, detect ARM compatibility, or automatically fix issues.
- Sample data is illustrative and must not be presented as measured performance.
- Ollama model support and performance on Snapdragon hardware have not been validated in this prototype.
- The app is being developed on an AMD Windows laptop; actual Snapdragon-device testing is still required before claiming deployment or optimization.

## Run on Windows

1. Install Python 3.10 or newer.
2. Open PowerShell in this folder.
3. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install packages:

   ```powershell
   pip install -r requirements.txt
   ```

5. Launch the app:

   ```powershell
   streamlit run app.py
   ```

6. In the browser, choose **Guided prototype** and select **Use sample diagnostic details** to try the demo.

## Optional local AI mode

1. Install Ollama for Windows from the official Ollama website.
2. Download a model supported by your computer, for example a small Qwen model if compatible with your setup.
3. In a terminal, pull the model using Ollama's documented command (example: `ollama pull qwen2.5:3b`).
4. Keep Ollama running, select **Local AI (Ollama)** in the app, and enter the same model name.

Model availability and resource needs vary. Do not assume that a model runs on the NPU just because it runs locally; confirm the actual backend separately.

## Safety and privacy

- The app only uses details typed or selected by the user.
- In local AI mode, prompt text is sent to the local Ollama service on the same computer.
- Do not paste passwords, personal documents, serial numbers, or other sensitive information into the demo.
- The app provides suggestions, not professional repair advice. It does not make system changes.

## Suggested next steps

1. Add a consent-based Windows diagnostics module.
2. Use verified vendor documentation for application compatibility.
3. Select a model from Qualcomm AI Hub or another open-source platform and document the exact model and runtime.
4. Test on a Snapdragon-powered HP PC and record repeatable latency, answer quality, and power measurements.
5. Review privacy, safety, and usability with test users.

## Project status

**Prototype / proof of concept.** The implementation should be validated and expanded before being represented as a production-ready diagnostic tool.
