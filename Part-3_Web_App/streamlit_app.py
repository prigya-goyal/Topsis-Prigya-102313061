import streamlit as st
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage

st.set_page_config(page_title="TOPSIS Web Service", layout="centered")

st.title("📊 TOPSIS Web Service")

st.write("Upload your CSV file, enter weights & impacts, and receive the result via email.")

# ---------- Inputs ----------
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
weights_input = st.text_input("Enter Weights (e.g. 1,1,1,1)")
impacts_input = st.text_input("Enter Impacts (e.g. +,+,-,-)")
email = st.text_input("Enter your Email")

# ---------- TOPSIS Function ----------
def topsis_process(data, weights, impacts):
    criteria = data.iloc[:, 1:]

    # Clean inputs
    weights = [float(w.strip()) for w in weights.split(',') if w.strip()]
    impacts = [i.strip() for i in impacts.split(',') if i.strip()]

    if len(weights) != criteria.shape[1] or len(impacts) != criteria.shape[1]:
        st.error("❌ Number of weights/impacts must match number of criteria columns!")
        return None

    # Step 1: Normalization
    norm = criteria / np.sqrt((criteria**2).sum())

    # Step 2: Weighted normalized matrix
    weighted = norm.mul(weights)

    # Step 3: Ideal Best and Worst
    ideal_best, ideal_worst = [], []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted.iloc[:, i].max())
            ideal_worst.append(weighted.iloc[:, i].min())
        else:
            ideal_best.append(weighted.iloc[:, i].min())
            ideal_worst.append(weighted.iloc[:, i].max())

    ideal_best = np.array(ideal_best)
    ideal_worst = np.array(ideal_worst)

    # Step 4: Distance calculation
    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    # Step 5: Score
    score = dist_worst / (dist_best + dist_worst)

    data['Topsis Score'] = score
    data['Rank'] = score.rank(ascending=False).astype(int)

    data.to_csv("result.csv", index=False)
    return data

# ---------- Email Function ----------
def send_email(receiver):
    sender = "goyalprigya@gmail.com"           
    app_password = "uhvnhrmsshjouhuv"        

    msg = EmailMessage()
    msg['Subject'] = 'TOPSIS Result'
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content('Attached is your TOPSIS result.')

    with open("result.csv", 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='octet-stream',
            filename='result.csv'
        )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, app_password)
        smtp.send_message(msg)

# ---------- Submit Button ----------
if st.button("Submit"):
    if not uploaded_file:
        st.warning("Please upload a CSV file.")
    elif not weights_input or not impacts_input or not email:
        st.warning("Please fill all fields.")
    else:
        df = pd.read_csv(uploaded_file)
        result = topsis_process(df, weights_input, impacts_input)

        if result is not None:
            send_email(email)
            st.success("✅ Result sent to your email!")
            st.dataframe(result)
