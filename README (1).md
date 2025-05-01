# 🏘️ Real Estate Investment Analysis Tool

This is a comprehensive **Streamlit app** designed to help real estate investors evaluate the financial performance of rental properties. It allows users to enter property-specific details and dynamically calculates key investment metrics, visualizes data, and enables CSV exports.

---

## 🚀 Features

- 📊 **Core Financial Metrics**:
  - Monthly mortgage payment
  - Net Operating Income (NOI)
  - Cap Rate
  - Cash-on-Cash Return
  - Annual cash flow

- 📈 **Advanced Investment Analysis**:
  - Internal Rate of Return (IRR)
  - Net Present Value (NPV)
  - Sale proceeds estimation based on property appreciation
  - Holding period analysis

- 📅 **Amortization Schedule**:
  - Monthly breakdown of principal and interest
  - Remaining loan balance over time

- 🎛️ **Sensitivity Analysis**:
  - Rent and interest rate adjustment sliders
  - Real-time impact on cash flow, IRR, and NPV

- 📉 **Matplotlib Visualizations**:
  - Loan balance over time (line chart)
  - Annual cash flow (bar chart)

- 📤 **Data Export**:
  - Download amortization schedule and summary metrics as CSV files

---

## 📦 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/ChandlerS03/real-estate-investment-tool.git
cd real-estate-investment-tool
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the app locally with:

```bash
streamlit run real_estate_tool_final.py
```

The app will open in your browser at `http://localhost:8501/`.

---

## 📂 Files in This Repo

| File | Description |
|------|-------------|
| `real_estate_tool_final.py` | Main Streamlit app |
| `requirements.txt` | List of required Python packages |
| `.gitignore` | Ignore cache, virtual envs, OS junk |
| `README.md` | This file |

---

## 📝 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
