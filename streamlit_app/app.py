import streamlit as st
import requests
import json

API_URL = "https://billy-ai-agent.onrender.com/full-pipeline"

st.set_page_config(page_title="Billy AI – Medical Invoice Analyzer", layout="wide")

st.title("🩺 Billy AI – Medical Invoice & Claims Analyzer")
st.write("Upload a medical invoice or claim PDF and Billy will extract, validate and check compliance.")

uploaded_file = st.file_uploader("Upload Medical Invoice PDF", type=["pdf"])

if uploaded_file:
    st.info("Processing... Please wait ~10 seconds.")

    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}

    try:
        response = requests.post(API_URL, files=files)
        
        if response.status_code == 200:
            result = response.json()

            st.success("Analysis complete!")

            # Pretty JSON viewer
            st.subheader("🧾 Parsed Document")
            st.json(result.get("parsed", {}))

            st.subheader("🧠 Coding Validation")
            st.json(result.get("coding", {}))

            st.subheader("🩺 Medical Necessity")
            st.json(result.get("necessity", {}))

            st.subheader("⚖️ Compliance Report")
            st.json(result.get("compliance", {}))

            st.subheader("📉 Denial Prediction")
            st.json(result.get("denial_prediction", {}))

            st.subheader("🛠 Corrections & Fixes")
            st.json(result.get("corrections", {}))

            # Download JSON
            st.download_button(
                label="⬇️ Download Full JSON",
                data=json.dumps(result, indent=4),
                file_name="billy_output.json",
                mime="application/json"
            )
        else:
            st.error(f"Error: {response.status_code}")
            st.text(response.text)

    except Exception as e:
        st.error("Failed to connect to API")
        st.text(str(e))
