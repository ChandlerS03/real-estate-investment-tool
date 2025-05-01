
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy_financial import irr, npv

# Page Configuration
st.set_page_config(page_title="Real Estate Investment Tool", layout="wide")

# Sidebar Inputs
st.sidebar.header("Property Information")
purchase_price = st.sidebar.number_input("Purchase Price ($)", 0.0, 1e7, 250000.0, 1000.0)
down_payment = st.sidebar.number_input("Down Payment ($)", 0.0, purchase_price, 50000.0, 1000.0)
loan_term = st.sidebar.number_input("Loan Term (Years)", 1, 40, 30)
base_interest_rate = st.sidebar.number_input("Base Interest Rate (%)", 0.0, 25.0, 4.0, 0.1)

st.sidebar.header("Income and Expenses")
base_rent = st.sidebar.number_input("Base Monthly Rent ($)", 0.0, 1e5, 2000.0, 100.0)
monthly_expenses = st.sidebar.number_input("Monthly Expenses ($)", 0.0, 1e5, 500.0, 50.0)

st.sidebar.header("Investment Assumptions")
holding_period = st.sidebar.number_input("Holding Period (Years)", 1, loan_term, 10)
appreciation_rate = st.sidebar.number_input("Annual Appreciation Rate (%)", 0.0, 25.0, 3.0, 0.1)
discount_rate = st.sidebar.number_input("Discount Rate for NPV (%)", 0.0, 25.0, 8.0, 0.1)

st.sidebar.header("Sensitivity Analysis")
rent_change = st.sidebar.slider("Adjust Monthly Rent (%)", -50, 50, 0)
rate_change = st.sidebar.slider("Adjust Interest Rate (%)", -3, 3, 0)

# Adjusted values
monthly_rent = base_rent * (1 + rent_change / 100)
interest_rate = base_interest_rate + rate_change

# Main Display
st.title("🏘️ Real Estate Investment Analysis Tool")

# Calculations
loan_amount = purchase_price - down_payment
monthly_interest_rate = interest_rate / 100 / 12
num_payments = loan_term * 12

if interest_rate > 0:
    monthly_payment = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate)**num_payments) /                       ((1 + monthly_interest_rate)**num_payments - 1)
else:
    monthly_payment = loan_amount / num_payments

annual_rent = monthly_rent * 12
annual_expenses = monthly_expenses * 12
net_operating_income = annual_rent - annual_expenses
annual_debt_service = monthly_payment * 12
cash_flow = net_operating_income - annual_debt_service
cash_on_cash_return = (cash_flow / down_payment) * 100 if down_payment > 0 else 0

# Amortization Schedule
balance = loan_amount
amort_data = []
loan_balance_list = []
for month in range(1, num_payments + 1):
    interest_payment = balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    balance -= principal_payment
    amort_data.append({
        "Month": month,
        "Payment": monthly_payment,
        "Principal": principal_payment,
        "Interest": interest_payment,
        "Remaining Balance": max(balance, 0)
    })
    loan_balance_list.append(max(balance, 0))

amort_df = pd.DataFrame(amort_data)
remaining_balance = amort_df.loc[holding_period * 12 - 1, "Remaining Balance"]
sale_price = purchase_price * ((1 + appreciation_rate / 100) ** holding_period)
sale_proceeds = sale_price - remaining_balance

# NPV & IRR
cash_flows = [-down_payment] + [cash_flow] * holding_period
cash_flows[-1] += sale_proceeds
npv_result = npv(discount_rate / 100, cash_flows)
irr_result = irr(cash_flows) * 100

# Display Summary Metrics
st.subheader("📈 Financial Metrics")
metrics = {
    "Monthly Mortgage Payment": monthly_payment,
    "Net Operating Income (NOI)": net_operating_income,
    "Cap Rate (%)": (net_operating_income / purchase_price) * 100,
    "Annual Cash Flow": cash_flow,
    "Cash-on-Cash Return (%)": cash_on_cash_return,
    "Estimated Sale Price": sale_price,
    "Remaining Balance at Exit": remaining_balance,
    "Net Proceeds from Sale": sale_proceeds,
    "NPV": npv_result,
    "IRR (%)": irr_result
}

for k, v in metrics.items():
    if "IRR" in k or "Cap Rate" in k or "Return" in k:
        st.write(f"**{k}:** {v:.2f}%")
    else:
        st.write(f"**{k}:** ${v:,.2f}")

# Matplotlib Charts
st.subheader("📉 Loan Balance Over Time")
fig1, ax1 = plt.subplots()
ax1.plot(np.arange(1, num_payments + 1), loan_balance_list)
ax1.set_xlabel("Month")
ax1.set_ylabel("Balance ($)")
ax1.set_title("Amortization Schedule")
ax1.grid(True)
st.pyplot(fig1)

st.subheader("💵 Annual Cash Flow Projection")
fig2, ax2 = plt.subplots()
years = np.arange(1, holding_period + 1)
cash_flow_projection = [cash_flow] * holding_period
cash_flow_projection[-1] += sale_proceeds
ax2.bar(years, cash_flow_projection)
ax2.set_xlabel("Year")
ax2.set_ylabel("Cash Flow ($)")
ax2.set_title("Cash Flow Over Holding Period")
st.pyplot(fig2)

# CSV Export
st.subheader("📤 Export Data")
csv_amort = amort_df.to_csv(index=False)
st.download_button("Download Amortization Schedule", data=csv_amort, file_name="amortization_schedule.csv", mime="text/csv")

summary_df = pd.DataFrame([metrics])
csv_metrics = summary_df.to_csv(index=False)
st.download_button("Download Financial Metrics Summary", data=csv_metrics, file_name="financial_metrics_summary.csv", mime="text/csv")
