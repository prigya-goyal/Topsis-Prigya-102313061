# TOPSIS 

This project implements the **TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)** method in three forms:

1. Command Line Tool
2. Python Package (PyPI)
3. Web Application using Streamlit

TOPSIS is a multi-criteria decision making technique used to rank alternatives based on their distance from an ideal best and ideal worst solution.

---

## Part-1: Python Package
The TOPSIS algorithm is packaged and published on PyPI.

## Installation

```bash
pip install Topsis-Prigya-102313061
```

---

## Part-2: Command Line Usage
## Input File Format

The input must be a CSV file with:

- First column: Names of alternatives
- Remaining columns: Numeric criteria values

### Example Input CSV

| Laptop Model | Performance | Battery Life | Weight (kg) | Price ($) |
| ------------ | ----------- | ------------ | ----------- | --------- |
| Model A      | 90          | 8            | 1.8         | 1200      |
| Model B      | 85          | 10           | 1.5         | 1500      |
| Model C      | 88          | 7            | 2.0         | 1000      |
| Model D      | 92          | 9            | 1.6         | 1800      |


### Meaning of Criteria

- Performance : Higher is better (+)
- Battery Life : Higher is better (+)
- Weight : Lower is better (-)
- Price : Lower is better (-)

---

### Parameters Used

- Weights vector = `[1, 1, 1, 1]`
- Impacts vector = `[+, +, -, -]`

---

## Command Line Usage

```bash
topsis data.csv "1,1,1,1" "+,+,-,-" output.csv
```

---

## Output

The output CSV file will contain two additional columns:

- **Topsis Score**
- **Rank**


| Laptop Model | Topsis Score | Rank |
| ------------ | ------------ | ---- |
| Model A      | 0.534277     | 3    |
| Model B      | 0.308368     | 4    |
| Model C      | 0.691632     | 1    |
| Model D      | 0.534737     | 2    |


---

## Part-3: Web Application (Streamlit)
A web interface is created using Streamlit where users can:

- Upload CSV file
- Enter weights and impacts
- Receive TOPSIS result on screen and via email


## Run Locally 

```bash
streamlit run streamlit_app.py
```

## Open in browser: 

```bash
http://localhost:8501
```

## Live Web App
The web application is deployed and accessible online via Streamlit Cloud.

---

## Project Structure

- Part-1_Python_Package/
- Part-2_Command_Line/
- Part-3_Web_App/
- streamlit_app.py
- requirements.txt
- README.md
- LICENSE
- User_Manual.pdf
  
---

### Notes

- The first column must contain the names of alternatives.
- All remaining columns must contain numeric values only.
- Number of weights and impacts must match the number of criteria columns.

---

## Requirements

- Python 3.6+
- pandas
- numpy

---

## Author

Prigya Goyal

---

## License

This project is released under the **MIT License** for educational purposes.
See the LICENSE file for details.

