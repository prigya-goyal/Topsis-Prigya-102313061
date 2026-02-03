from flask import Flask, request, render_template_string
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# -------- TOPSIS FUNCTION --------
def topsis_process(file, weights, impacts):
    data = pd.read_csv(file)
    criteria = data.iloc[:, 1:]

    weights = list(map(float, weights.split(',')))
    impacts = impacts.split(',')

    norm = criteria / np.sqrt((criteria**2).sum())
    weighted = norm * weights

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

    dist_best = np.sqrt(((weighted - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted - ideal_worst) ** 2).sum(axis=1))

    score = dist_worst / (dist_best + dist_worst)

    data['Topsis Score'] = score
    data['Rank'] = score.rank(ascending=False).astype(int)

    output = "result.csv"
    data.to_csv(output, index=False)
    return output


# -------- EMAIL FUNCTION --------
def send_email(receiver, file_path):
        sender = "goyalprigya@gmail.com"
        app_password = "csoixpcwufjelekx"

        msg = EmailMessage()
        msg['Subject'] = 'TOPSIS Result'
        msg['From'] = sender
        msg['To'] = receiver
        msg.set_content('Attached is your TOPSIS result.')

        with open(file_path, 'rb') as f:
            msg.add_attachment(f.read(),
                               maintype='application',
                               subtype='octet-stream',
                               filename='result.csv')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, app_password)
            smtp.send_message(msg)

       


# -------- HTML PAGE --------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>TOPSIS Web Service</title>

<style>
body {
    font-family: Arial, sans-serif;
    background: #f2f2f2;
}

.container {
    width: 400px;
    margin: 80px auto;
    padding: 25px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 0 10px gray;
}

h2 {
    text-align: center;
    color: #333;
}

input[type="text"],
input[type="email"],
input[type="file"] {
    width: 100%;
    padding: 8px;
    margin: 8px 0 15px 0;
}

input[type="submit"] {
    width: 100%;
    padding: 10px;
    background: #4CAF50;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
}

input[type="submit"]:hover {
    background: #45a049;
}
</style>
</head>

<body>

<div class="container">
<h2>TOPSIS Web Service</h2>

<form method="POST" enctype="multipart/form-data">
CSV File:
<input type="file" name="file">

Weights:
<input type="text" name="weights" placeholder="e.g. 1,1,1,1">

Impacts:
<input type="text" name="impacts" placeholder="e.g. +,+,-,-">

Email:
<input type="email" name="email" placeholder="Enter your email">

<input type="submit" value="Submit">
</form>

</div>

</body>
</html>
"""



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        weights = request.form['weights']
        impacts = request.form['impacts']
        email = request.form['email']

        file.save("input.csv")
        result = topsis_process("input.csv", weights, impacts)
        send_email(email, result)

        return "Result sent to your email!"

    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(debug=True)
