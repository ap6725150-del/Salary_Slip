import numpy as np
import pandas as pd
import streamlit as st


st.title("SALARY & TAX CALCULATOR (India)")
st.subheader("CTC to In-Hand Salary & Tax Estimator")

# ================= CANDIDATE DETAILS =================
st.subheader("Candidate Details:-")

ctc = st.number_input("CTC:",min_value=0.0)
name = st.text_input("Candidate Name:")

# ============ SALARY STRUCTURE (Earnings) ============
st.subheader("Salary Structure Input:-")

st.write("Basic Salary:")
col1, col2, col3 = st.columns(3)
with col1:
    basic_type = st.radio("Type", ["₹", "%"], key="basic_type", horizontal=True)
with col2:
    basic_input = st.number_input("Value", min_value=0.0, key="basic_input")
with col3:
    if basic_type == "%" and ctc > 0:
        basic = (basic_input / 100) * ctc
        st.write("=", round(basic,2))
    else:
        basic = basic_input

st.write("HRA:")
col1, col2, col3 = st.columns(3)
with col1:
    hra_type = st.radio("Type", ["₹", "%"], key="hra_type", horizontal=True)
with col2:
    hra_input = st.number_input("Value", min_value=0.0, key="hra_input")
with col3:
    if hra_type == "%" and ctc > 0:
        hra = (hra_input / 100) * basic
        st.write("=", round(hra,2))
    else:
        hra = hra_input

st.write("Bonus:")
col1, col2, col3 = st.columns(3)
with col1:
    bonus_type = st.radio("Type", ["₹", "%"], key="bonus_type", horizontal=True)
with col2:
    bonus_input = st.number_input("Value", min_value=0.0, key="bonus_input")
with col3:
    if bonus_type == "%" and ctc > 0:
        bonus = (bonus_input / 100) * basic
        st.write("=", round(bonus,2))
    else:
        bonus = bonus_input

st.write("Other Allowance:")
col1, col2, col3 = st.columns(3)
with col1:
    other_type = st.radio("Type", ["₹", "%"], key="other_type", horizontal=True)
with col2:
    other_input = st.number_input("Value", min_value=0.0, key="other_input")
with col3:
    if other_type == "%" and ctc > 0:
        other = (other_input / 100) * basic
        st.write("=", round(other, 2))
    else:
        other = other_input

st.write("Business Allowance:")
col1, col2, col3 = st.columns(3)
with col1:
    business_type = st.radio("Type", ["₹", "%"], key="business_type", horizontal=True)
with col2:
    business_input = st.number_input("Value", min_value=0.0, key="business_input")
with col3:
    if business_type == "%" and ctc > 0:
        business = (business_input / 100) * basic
        st.write("=", round(business,2))
    else:
        business = business_input
        

# ========== SALARY STRUCTURE (Employer Costs) =========
st.subheader("Employer Cost:-")

admin_pf = st.number_input("Admin PF:", min_value=0.0)
edli = st.number_input("EDLI:", min_value=0.0)
employer_pf = st.number_input("Employer PF", min_value=0.0)

# ============ SALARY STRUCTURE (Deductions) ============
st.subheader("Deductions:-")

p_tax = st.number_input("Professional Tax:", min_value=0.0)
employee_pf = st.number_input("Employee PF", min_value=0.0)


## ===== CALCULATIONS =====
if st.button("Calculate", use_container_width=True):
    gross = basic + hra + bonus + other + business
    ctc = gross + admin_pf + edli + employer_pf
    net = gross-(p_tax + employee_pf)

    df = pd.DataFrame({"Components":["Basic", "HRA", "Bonus", "Other Allowance", "Business Allowance", "Gross Salary",
                                     "Admin P.F.", "E.D.L.I.", "Employer P.F.", "CTC",
                                     "Professional Tax", "Employee P.F.", "Net Salary"],
                       
                       "Type":["Earning", "Earning", "Earning", "Earning", "Earning", "Total of Earnings",
                               "Employer Cost", "Employer Cost", "Employer Cost", "Earnings+Employer Costs",
                               "Deduction", "Deduction", "Earnings-Deductions"],
                       
                       "Yearly (₹)":[basic, hra, bonus, other, business, gross, admin_pf, edli, employer_pf, ctc,
                                     p_tax, employee_pf, net],
                       
                       "Monthly (₹)":[basic/12, hra/12, bonus/12, other/12, business/12, gross/12,
                                      admin_pf/12, edli/12, employer_pf/12, ctc/12, p_tax/12, employee_pf/12, net/12]})

# ================== SALARY BREAKDOWN ====================
    st.subheader("-Salary Breakdown:-")
        
    def highlight_rows(row):
        if row["Components"] in ["CTC", "Gross Salary", "Net Salary"]:
            return ["background-color: #d3d3d3; font-weight: bold"] * len(row)
        return [""] * len(row)

    styled_df = df.round(2).style.apply(highlight_rows, axis=1)
    st.dataframe(styled_df)

    st.write("Monthly Net Salary:", round(net/12,2))
