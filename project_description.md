# Snapdragon Sense
## AI-Powered Laptop Troubleshooting Assistant

### Project summary
Snapdragon Sense is a prototype concept for an AI assistant that helps laptop users understand common symptoms—such as unusual battery drain, slow performance, app crashes, freezes, and wireless problems—and decide what to check next. It converts user-provided observations into plain-language troubleshooting guidance.

### Problem
When a laptop behaves unexpectedly, users often encounter technical error messages and generic online advice. They may not know which evidence to collect, which checks are safe, or which actions could make the problem worse. The prototype focuses on making the first troubleshooting steps clearer and more structured.

### Proposed solution
A lightweight desktop-friendly interface collects the user's symptom and optional details. A guided analysis layer produces cautious, low-risk checks. An optional local AI mode uses an open-source model served by Ollama on the same computer to rewrite the assessment in clear language. The prototype does not silently monitor the PC or make changes to system settings.

### Intended Snapdragon fit
The solution is intended for future optimization on Snapdragon-powered HP PCs. A local inference architecture can support reduced dependence on cloud services and keep diagnostic prompts on the device. Actual Snapdragon model compatibility, runtime selection, latency, and power consumption must be tested before claiming performance or NPU acceleration.

### Current prototype
- Streamlit interface with guided paths for five common symptom categories.
- User-entered diagnostics and an explicitly labelled sample demo.
- Optional local model integration through Ollama.
- Fallback guidance when a local model is not configured.
- Clear limitations and no automatic system modifications.

### AI use
The local model is used to explain the user-provided symptom and generate structured troubleshooting guidance. The app includes safeguards instructing the model not to claim that it inspected the device, verified compatibility, or fixed an issue. The guided fallback is rule-based, so the AI-enabled mode should be demonstrated separately when available.

### User journey
1. User selects a symptom and describes what happened.
2. User adds optional details such as battery drop, time period, or recent changes.
3. The app generates a cautious initial assessment.
4. The app offers low-risk checks and explains uncertainty.
5. The user decides whether to follow a step or consult official support.

### Safety, privacy, and limitations
The prototype uses only user-provided text and selected values. It does not collect live system telemetry, access personal files, or change system settings. Local AI mode sends the prompt to the local Ollama service. Users should avoid entering sensitive information. Recommendations are hypotheses, not confirmed diagnoses.

### Validation plan
- Test with representative scenarios and check that recommendations are safe and understandable.
- Add consent-based access to supported Windows diagnostic data.
- Select and document a model from Qualcomm AI Hub or another open-source platform.
- Test on actual Snapdragon-powered HP hardware.
- Record model/runtime, latency, memory usage, answer quality, and power measurements using repeatable tests.
- Verify the challenge's hardware ownership eligibility and all submission requirements.

### Current status
Proof of concept. Built and packaged for local demonstration on Windows; Snapdragon hardware testing and deployment optimization are not yet completed.
