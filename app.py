import streamlit as st
import pandas as pd
import joblib

# Load model and encoders
model = joblib.load("models/intrusion_detection_model.pkl")
protocol_encoder = joblib.load("models/protocol_encoder.pkl")
service_encoder = joblib.load("models/service_encoder.pkl")
flag_encoder = joblib.load("models/flag_encoder.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

st.set_page_config(page_title="Network Intrusion Detection", page_icon="🚨")

st.title("Network Intrusion Detection System")

st.write(
    "Predict whether a network connection is normal traffic or an intrusion attack."
)

# Inputs

protocol = st.selectbox(
    "Protocol Type",
    protocol_encoder.classes_
)

service = st.selectbox(
    "Service",
    service_encoder.classes_
)

flag = st.selectbox(
    "Flag",
    flag_encoder.classes_
)

src_bytes = st.number_input(
    "Source Bytes",
    min_value=0,
    value=491
)

dst_bytes = st.number_input(
    "Destination Bytes",
    min_value=0,
    value=0
)

count = st.number_input(
    "Count",
    min_value=0,
    value=2
)

srv_count = st.number_input(
    "Server Count",
    min_value=0,
    value=2
)

serror_rate = st.number_input(
    "Serror Rate",
    min_value=0.0,
    max_value=1.0,
    value=0.0
)

same_srv_rate = st.number_input(
    "Same Service Rate",
    min_value=0.0,
    max_value=1.0,
    value=1.0
)

dst_host_count = st.number_input(
    "Destination Host Count",
    min_value=0,
    value=150
)

if st.button("Predict"):

    protocol_encoded = protocol_encoder.transform([protocol])[0]
    service_encoded = service_encoder.transform([service])[0]
    flag_encoded = flag_encoder.transform([flag])[0]

    input_data = pd.DataFrame(
        [[
            protocol_encoded,
            service_encoded,
            flag_encoded,
            src_bytes,
            dst_bytes,
            count,
            srv_count,
            serror_rate,
            same_srv_rate,
            dst_host_count
        ]],
        columns=[
            'protocol_type',
            'service',
            'flag',
            'src_bytes',
            'dst_bytes',
            'count',
            'srv_count',
            'serror_rate',
            'same_srv_rate',
            'dst_host_count'
        ]
    )

    prediction = model.predict(input_data)

    attack_name = label_encoder.inverse_transform(prediction)[0]

    if attack_name == "normal":
        st.success(f"Normal Traffic")
    else:
        st.error(f"Attack Detected: {attack_name}")

    st.subheader("Input Data")
    st.dataframe(input_data)