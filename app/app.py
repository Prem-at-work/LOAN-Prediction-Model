import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.predict import predict_loan

st.set_page_config(
    page_title="Loan Approval Prediction App",
    page_icon="💰",
    layout="wide"
)

# ------------------ SESSION STATE DEFAULTS ------------------
def set_default_state():
    defaults = {
        "Gender": "Male",
        "Married": "Yes",
        "Dependents": "0",
        "Education": "Graduate",
        "Self_Employed": "No",
        "ApplicantIncome": "",
        "CoapplicantIncome": "",
        "LoanAmount": "",
        "Loan_Amount_Term": "",
        "Credit_History": 1.0,
        "Property_Area": "Semiurban"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

set_default_state()

# ------------------ SAMPLE DATA FUNCTIONS ------------------
def fill_sample_approved():
    st.session_state.Gender = "Male"
    st.session_state.Married = "Yes"
    st.session_state.Dependents = "1"
    st.session_state.Education = "Graduate"
    st.session_state.Self_Employed = "No"
    st.session_state.ApplicantIncome = "5000"
    st.session_state.CoapplicantIncome = "1500"
    st.session_state.LoanAmount = "120"
    st.session_state.Loan_Amount_Term = "360"
    st.session_state.Credit_History = 1.0
    st.session_state.Property_Area = "Semiurban"

def fill_sample_rejected():
    st.session_state.Gender = "Male"
    st.session_state.Married = "No"
    st.session_state.Dependents = "0"
    st.session_state.Education = "Not Graduate"
    st.session_state.Self_Employed = "Yes"
    st.session_state.ApplicantIncome = "1800"
    st.session_state.CoapplicantIncome = "0"
    st.session_state.LoanAmount = "220"
    st.session_state.Loan_Amount_Term = "120"
    st.session_state.Credit_History = 0.0
    st.session_state.Property_Area = "Rural"

def reset_form():
    st.session_state.Gender = "Male"
    st.session_state.Married = "Yes"
    st.session_state.Dependents = "0"
    st.session_state.Education = "Graduate"
    st.session_state.Self_Employed = "No"
    st.session_state.ApplicantIncome = ""
    st.session_state.CoapplicantIncome = ""
    st.session_state.LoanAmount = ""
    st.session_state.Loan_Amount_Term = ""
    st.session_state.Credit_History = 1.0
    st.session_state.Property_Area = "Semiurban"

# ------------------ DYNAMIC REASONS FUNCTION ------------------
def generate_reasons(
    status,
    credit_history,
    applicant_income,
    coapplicant_income,
    loan_amount,
    loan_term,
    education,
    property_area,
    married,
    dependents
):
    reasons = []

    total_income = applicant_income + coapplicant_income

    # Positive reasons
    if credit_history == 1.0:
        reasons.append("Good credit history increased the approval chance.")
    if total_income >= 5000:
        reasons.append("Stable total income supports repayment ability.")
    if loan_amount <= 150:
        reasons.append("Requested loan amount is moderate, which helps approval.")
    if loan_term >= 180:
        reasons.append("Longer repayment term can make repayment easier.")
    if education == "Graduate":
        reasons.append("Graduate education may be seen as a positive financial stability indicator.")
    if property_area == "Semiurban":
        reasons.append("Semiurban property area has historically shown good approval patterns in this dataset.")
    if married == "Yes":
        reasons.append("Marital status may indicate household stability for repayment.")
    if dependents in ["0", "1"]:
        reasons.append("Lower number of dependents can reduce financial burden.")

    # Negative reasons
    if credit_history == 0.0:
        reasons.append("Poor or missing credit history strongly reduces approval chance.")
    if total_income < 2500:
        reasons.append("Low combined income may make repayment difficult.")
    if loan_amount > 200:
        reasons.append("High loan amount may reduce approval probability.")
    if loan_term < 120:
        reasons.append("Very short repayment term can increase EMI burden.")
    if education == "Not Graduate":
        reasons.append("Non-graduate education may slightly reduce approval chances in this model pattern.")
    if property_area == "Rural":
        reasons.append("Rural property area may have slightly weaker approval patterns in this dataset.")

    # Select reasons based on result
    if status == "Approved":
        final_reasons = []
        for r in reasons:
            if any(word in r.lower() for word in [
                "increased", "supports", "helps", "easier", "positive", "good", "stability"
            ]):
                final_reasons.append(r)

        if not final_reasons:
            final_reasons = [
                "The overall applicant profile appears favorable for loan approval.",
                "Income, credit history, and loan details seem reasonably balanced."
            ]
    else:
        final_reasons = []
        for r in reasons:
            if any(word in r.lower() for word in [
                "reduces", "difficult", "high loan", "burden", "poor", "weaker"
            ]):
                final_reasons.append(r)

        if not final_reasons:
            final_reasons = [
                "The current applicant profile appears less favorable for loan approval.",
                "Some financial or credit-related factors may be reducing approval chances."
            ]

    return final_reasons[:4]   # show max 4 reasons


# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #050816 0%, #081224 40%, #06152d 100%);
    color: white;
}

/* Main container */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1250px;
}

/* Title */
.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.3rem;
}
.gradient-text {
    background: linear-gradient(90deg, #f59e0b, #ec4899, #8b5cf6, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.sub-text {
    text-align: center;
    font-size: 19px;
    color: #d1d5db;
    margin-bottom: 1.3rem;
}

/* Cards */
.card {
    background: rgba(15, 23, 42, 0.78);
    border: 1px solid rgba(139, 92, 246, 0.22);
    border-radius: 20px;
    padding: 20px 22px;
    box-shadow: 0 0 18px rgba(59, 130, 246, 0.12);
    margin-bottom: 18px;
}
.card h3, .card h4 {
    margin-top: 0;
    color: white;
}
.card p, .card li {
    color: #e5e7eb;
    font-size: 15px;
    line-height: 1.6;
}

/* Section title */
.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 10px;
    margin-bottom: 14px;
}

/* Result cards */
.result-approved {
    background: linear-gradient(135deg, rgba(16,185,129,0.18), rgba(5,150,105,0.12));
    border: 1px solid rgba(16,185,129,0.45);
    border-radius: 24px;
    padding: 26px;
    box-shadow: 0 0 28px rgba(16,185,129,0.20);
}
.result-rejected {
    background: linear-gradient(135deg, rgba(239,68,68,0.16), rgba(127,29,29,0.10));
    border: 1px solid rgba(239,68,68,0.45);
    border-radius: 24px;
    padding: 26px;
    box-shadow: 0 0 28px rgba(239,68,68,0.18);
}

/* Small info boxes */
.mini-box {
    background: rgba(255,255,255,0.05);
    padding: 14px 14px;
    border-radius: 14px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
}
.mini-label {
    color: #cbd5e1;
    font-size: 14px;
}
.mini-value {
    color: white;
    font-size: 20px;
    font-weight: 700;
}

/* Probability */
.prob-big {
    font-size: 56px;
    font-weight: 800;
    margin: 0;
}

/* Predict button */
div.stButton > button {
    width: 100%;
    border: none;
    border-radius: 14px;
    padding: 0.9rem 1rem;
    font-size: 20px;
    font-weight: 700;
    color: white;
    background: linear-gradient(90deg, #ec4899, #8b5cf6, #2563eb);
    box-shadow: 0 0 18px rgba(139,92,246,0.35);
}
div.stButton > button:hover {
    filter: brightness(1.08);
}

/* Inputs */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background-color: rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* Reason chips */
.reason-box {
    background: rgba(255,255,255,0.05);
    border-left: 4px solid #8b5cf6;
    padding: 12px 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: #f3f4f6;
    font-size: 15px;
}

/* Sidebar note */
.sidebar-note {
    font-size: 14px;
    color: #d1d5db;
    line-height: 1.6;
}

/* Spacing */
.spacer-20 { height: 20px; }
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.markdown("## 💡 Project Info")
    st.markdown("""
<div class="sidebar-note">
<b>Loan Approval Prediction System</b><br><br>
This app predicts whether a loan application is likely to be approved using a trained <b>Logistic Regression</b> model.<br><br>

<b>Input Features:</b>
- Gender
- Married
- Dependents
- Education
- Self Employed
- Applicant Income
- Coapplicant Income
- Loan Amount
- Loan Amount Term
- Credit History
- Property Area
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚡ Quick Actions")

    if st.button("✅ Fill Approved Sample"):
        fill_sample_approved()
        st.rerun()

    if st.button("❌ Fill Rejected Sample"):
        fill_sample_rejected()
        st.rerun()

    if st.button("🔄 Reset Form"):
        reset_form()
        st.rerun()

    st.markdown("---")
    st.markdown("### 🧠 Model")
    st.info("Final deployed model: Logistic Regression")

# ------------------ HEADER ------------------
st.markdown(
    """
    <div class="main-title">💰 Loan Approval <span class="gradient-text">Prediction App</span></div>
    <div class="sub-text">AI-powered model to predict whether a loan will be approved or rejected</div>
    """,
    unsafe_allow_html=True
)

# ------------------ TOP INFO CARDS ------------------
info_col1, info_col2 = st.columns([2.2, 1])

with info_col1:
    st.markdown("""
    <div class="card">
        <h3>ℹ️ How to enter the values</h3>
        <ul>
            <li><b>Applicant Income</b> and <b>Coapplicant Income</b> should be entered in the same numeric style used in the dataset/app examples.</li>
            <li><b>Loan Amount</b> is generally entered in <b>thousands</b>. Example: <b>128</b> means ₹1,28,000.</li>
            <li><b>Loan Amount Term</b> must be entered in <b>months</b>. Example: <b>60</b> = 5 years, <b>360</b> = 30 years.</li>
            <li>Use only numbers in numeric fields.</li>
        </ul>
        <p style="margin-top:10px;"><b>Examples:</b><br>
        ₹75,000 → enter <b>7500</b> for income fields<br>
        ₹1,20,000 → enter <b>120</b> for loan amount if your dataset follows amount-in-thousands format</p>
    </div>
    """, unsafe_allow_html=True)

with info_col2:
    st.markdown("""
    <div class="card">
        <h3>✨ Quick Examples</h3>
        <p><b>Applicant Income</b><br>₹75,000 → <b>7500</b></p>
        <p><b>Coapplicant Income</b><br>₹15,000 → <b>1500</b></p>
        <p><b>Loan Amount</b><br>₹1,28,000 → <b>128</b></p>
        <p><b>Loan Term</b><br>5 years → <b>60</b> months</p>
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-title">👤 Applicant Details</div>', unsafe_allow_html=True)

# ------------------ FORM ------------------
col1, col2 = st.columns(2)

with col1:
    Gender = st.selectbox(
        "Gender",
        ["Male", "Female"],
        key="Gender",
        help="Gender of the applicant."
    )

    Married = st.selectbox(
        "Married",
        ["Yes", "No"],
        key="Married",
        help="Whether the applicant is married."
    )

    Dependents = st.selectbox(
        "Dependents",
        ["0", "1", "2", "3+"],
        key="Dependents",
        help="Number of dependents of the applicant."
    )

    Education = st.selectbox(
        "Education",
        ["Graduate", "Not Graduate"],
        key="Education",
        help="Education status of the applicant."
    )

    Self_Employed = st.selectbox(
        "Self Employed",
        ["No", "Yes"],
        key="Self_Employed",
        help="Whether the applicant is self-employed."
    )

    ApplicantIncome = st.text_input(
        "Applicant Income",
        key="ApplicantIncome",
        placeholder="e.g. 4583",
        help="Monthly income of the applicant. Example from dataset: 4583"
    )

with col2:
    CoapplicantIncome = st.text_input(
        "Coapplicant Income",
        key="CoapplicantIncome",
        placeholder="e.g. 1508.0 or 0",
        help="Monthly income of the coapplicant. Enter 0 if there is no coapplicant."
    )

    LoanAmount = st.text_input(
        "Loan Amount",
        key="LoanAmount",
        placeholder="e.g. 128 for ₹1,28,000",
        help="Loan amount generally stored in thousands. Example: 128 means ₹1,28,000."
    )

    Loan_Amount_Term = st.text_input(
        "Loan Amount Term (months)",
        key="Loan_Amount_Term",
        placeholder="e.g. 360 for 30 years",
        help="Loan repayment term in months."
    )

    Credit_History = st.selectbox(
        "Credit History",
        [1.0, 0.0],
        key="Credit_History",
        format_func=lambda x: "1.0 (Good)" if x == 1.0 else "0.0 (Poor)",
        help="1.0 means good credit history, 0.0 means poor/no credit history."
    )

    Property_Area = st.selectbox(
        "Property Area",
        ["Rural", "Semiurban", "Urban"],
        key="Property_Area",
        help="Area where the property is located."
    )

st.markdown("<div class='spacer-20'></div>", unsafe_allow_html=True)

predict_btn = st.button("🚀 Predict Loan Status")

# ------------------ PREDICTION ------------------
if predict_btn:
    if not ApplicantIncome or not CoapplicantIncome or not LoanAmount or not Loan_Amount_Term:
        st.warning("⚠️ Please fill all numeric fields before predicting.")
    else:
        try:
            ApplicantIncome = float(ApplicantIncome)
            CoapplicantIncome = float(CoapplicantIncome)
            LoanAmount = float(LoanAmount)
            Loan_Amount_Term = float(Loan_Amount_Term)

            # -------- INPUT VALIDATION --------
            if ApplicantIncome < 0:
                st.error("Applicant Income cannot be negative.")
            elif CoapplicantIncome < 0:
                st.error("Coapplicant Income cannot be negative.")
            elif LoanAmount <= 0:
                st.error("Loan Amount must be greater than 0.")
            elif Loan_Amount_Term <= 0:
                st.error("Loan Amount Term must be greater than 0.")
            else:
                status, probability = predict_loan(
                    Gender,
                    Married,
                    Dependents,
                    Education,
                    Self_Employed,
                    ApplicantIncome,
                    CoapplicantIncome,
                    LoanAmount,
                    Loan_Amount_Term,
                    Credit_History,
                    Property_Area
                )

                probability_percent = round(probability * 100, 2)

                if probability_percent >= 80:
                    confidence = "High"
                elif probability_percent >= 60:
                    confidence = "Moderate"
                else:
                    confidence = "Low"

                reasons = generate_reasons(
                    status=status,
                    credit_history=Credit_History,
                    applicant_income=ApplicantIncome,
                    coapplicant_income=CoapplicantIncome,
                    loan_amount=LoanAmount,
                    loan_term=Loan_Amount_Term,
                    education=Education,
                    property_area=Property_Area,
                    married=Married,
                    dependents=Dependents
                )

                st.markdown("<div class='section-title'>✨ Prediction Result</div>", unsafe_allow_html=True)

                if status == "Approved":
                    result_class = "result-approved"
                    emoji = "✅"
                    result_text = "Loan Approved"
                    desc = "Based on the provided details, the applicant profile looks favorable for approval."
                else:
                    result_class = "result-rejected"
                    emoji = "❌"
                    result_text = "Loan Rejected"
                    desc = "Based on the provided details, the applicant profile looks less favorable for approval."

                st.markdown(f'<div class="{result_class}">', unsafe_allow_html=True)

                # Top result row
                top_col1, top_col2 = st.columns([1, 2])

                with top_col1:
                    st.markdown(
                        f"""
                        <div style="text-align:center; padding-top:18px;">
                            <p class="prob-big">{probability_percent}%</p>
                            <p style="font-size:18px; color:#d1d5db; margin-top:-10px;">Approval Probability</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.progress(min(probability, 1.0))

                with top_col2:
                    st.markdown(
                        f"""
                        <h1 style="margin-bottom:0;">{emoji} {result_text}</h1>
                        <p style="font-size:18px; color:#e5e7eb;">{desc}</p>
                        """,
                        unsafe_allow_html=True
                    )

                    b1, b2, b3 = st.columns(3)
                    with b1:
                        st.markdown(f"""
                        <div class="mini-box">
                            <div class="mini-label">Status</div>
                            <div class="mini-value">{status}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with b2:
                        st.markdown(f"""
                        <div class="mini-box">
                            <div class="mini-label">Confidence</div>
                            <div class="mini-value">{confidence}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    with b3:
                        st.markdown("""
                        <div class="mini-box">
                            <div class="mini-label">Model</div>
                            <div class="mini-value">Logistic Regression</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Reasons section
                st.markdown("### 📌 Key Factors Behind This Prediction")
                for reason in reasons:
                    st.markdown(f'<div class="reason-box">• {reason}</div>', unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                st.info("📌 This prediction is based on historical data and should be used as a reference, not as a final financial decision.")

        except ValueError:
            st.error("Please enter valid numeric values in income, loan amount, and loan term fields.")

# import os
# import sys
# import streamlit as st

# # Add project root to path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from src.predict import predict_loan

# st.set_page_config(
#     page_title="Loan Approval Prediction App",
#     page_icon="💰",
#     layout="wide"
# )

# # ------------------ CUSTOM CSS ------------------
# st.markdown("""
# <style>
# /* Main background */
# .stApp {
#     background: linear-gradient(135deg, #050816 0%, #081224 40%, #06152d 100%);
#     color: white;
# }

# /* Center container width */
# .block-container {
#     padding-top: 1.5rem;
#     padding-bottom: 2rem;
#     max-width: 1200px;
# }

# /* Title */
# .main-title {
#     text-align: center;
#     font-size: 52px;
#     font-weight: 800;
#     color: #ffffff;
#     margin-bottom: 0.3rem;
# }
# .gradient-text {
#     background: linear-gradient(90deg, #f59e0b, #8b5cf6, #3b82f6);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
# }
# .sub-text {
#     text-align: center;
#     font-size: 20px;
#     color: #d1d5db;
#     margin-bottom: 1.5rem;
# }

# /* Cards */
# .card {
#     background: rgba(15, 23, 42, 0.75);
#     border: 1px solid rgba(139, 92, 246, 0.25);
#     border-radius: 20px;
#     padding: 20px 22px;
#     box-shadow: 0 0 18px rgba(59, 130, 246, 0.12);
#     margin-bottom: 18px;
# }
# .card h3, .card h4 {
#     margin-top: 0;
#     color: white;
# }
# .card p, .card li {
#     color: #e5e7eb;
#     font-size: 15px;
#     line-height: 1.6;
# }

# /* Section title */
# .section-title {
#     font-size: 28px;
#     font-weight: 700;
#     color: #ffffff;
#     margin-top: 8px;
#     margin-bottom: 14px;
# }

# /* Result card */
# .result-approved {
#     background: linear-gradient(135deg, rgba(16,185,129,0.18), rgba(5,150,105,0.12));
#     border: 1px solid rgba(16,185,129,0.5);
#     border-radius: 22px;
#     padding: 24px;
#     box-shadow: 0 0 25px rgba(16,185,129,0.20);
# }
# .result-rejected {
#     background: linear-gradient(135deg, rgba(239,68,68,0.16), rgba(127,29,29,0.10));
#     border: 1px solid rgba(239,68,68,0.5);
#     border-radius: 22px;
#     padding: 24px;
#     box-shadow: 0 0 25px rgba(239,68,68,0.18);
# }

# /* Small info boxes inside result */
# .mini-box {
#     background: rgba(255,255,255,0.05);
#     padding: 12px 14px;
#     border-radius: 14px;
#     text-align: center;
#     border: 1px solid rgba(255,255,255,0.08);
# }
# .mini-label {
#     color: #cbd5e1;
#     font-size: 14px;
# }
# .mini-value {
#     color: white;
#     font-size: 20px;
#     font-weight: 700;
# }

# /* Probability big text */
# .prob-big {
#     font-size: 52px;
#     font-weight: 800;
#     margin: 0;
# }

# /* Button */
# div.stButton > button {
#     width: 100%;
#     border: none;
#     border-radius: 14px;
#     padding: 0.85rem 1rem;
#     font-size: 20px;
#     font-weight: 700;
#     color: white;
#     background: linear-gradient(90deg, #ec4899, #8b5cf6, #2563eb);
#     box-shadow: 0 0 18px rgba(139,92,246,0.35);
# }
# div.stButton > button:hover {
#     filter: brightness(1.08);
# }

# /* Streamlit inputs */
# div[data-baseweb="select"] > div,
# div[data-baseweb="input"] > div {
#     background-color: rgba(255,255,255,0.06) !important;
#     border-radius: 12px !important;
#     border: 1px solid rgba(255,255,255,0.08) !important;
# }

# /* Horizontal rule replacement spacing */
# .spacer-10 { height: 10px; }
# .spacer-20 { height: 20px; }
# </style>
# """, unsafe_allow_html=True)

# # ------------------ HEADER ------------------
# st.markdown(
#     """
#     <div class="main-title">💰 Loan Approval <span class="gradient-text">Prediction App</span></div>
#     <div class="sub-text">AI-powered model to predict whether your loan will be approved or rejected</div>
#     """,
#     unsafe_allow_html=True
# )

# # ------------------ TOP INFO CARDS ------------------
# info_col1, info_col2 = st.columns([2.2, 1])

# with info_col1:
#     st.markdown("""
#     <div class="card">
#         <h3>ℹ️ How to enter the values</h3>
#         <ul>
#             <li><b>Applicant Income</b> and <b>Coapplicant Income</b> should be entered in the same numeric style used in the dataset/app examples.</li>
#             <li><b>Loan Amount</b> is generally entered in <b>thousands</b>. Example: <b>128</b> means ₹1,28,000.</li>
#             <li><b>Loan Amount Term</b> must be entered in <b>months</b>. Example: <b>60</b> = 5 years, <b>360</b> = 30 years.</li>
#             <li>Use only numbers in numeric fields.</li>
#         </ul>
#         <p style="margin-top:10px;"><b>Examples:</b><br>
#         ₹75,000 → enter <b>7500</b> for income fields<br>
#         ₹1,20,000 → enter <b>120</b> for loan amount if your dataset follows amount-in-thousands format</p>
#     </div>
#     """, unsafe_allow_html=True)

# with info_col2:
#     st.markdown("""
#     <div class="card">
#         <h3>✨ Quick Examples</h3>
#         <p><b>Applicant Income</b><br>₹75,000 → <b>7500</b></p>
#         <p><b>Coapplicant Income</b><br>₹15,000 → <b>1500</b></p>
#         <p><b>Loan Amount</b><br>₹1,28,000 → <b>128</b></p>
#         <p><b>Loan Term</b><br>5 years → <b>60</b> months</p>
#     </div>
#     """, unsafe_allow_html=True)

# st.markdown('<div class="section-title">👤 Applicant Details</div>', unsafe_allow_html=True)

# # ------------------ FORM ------------------
# col1, col2 = st.columns(2)

# with col1:
#     Gender = st.selectbox(
#         "Gender",
#         ["Male", "Female"],
#         help="Gender of the applicant."
#     )

#     Married = st.selectbox(
#         "Married",
#         ["Yes", "No"],
#         help="Whether the applicant is married."
#     )

#     Dependents = st.selectbox(
#         "Dependents",
#         ["0", "1", "2", "3+"],
#         help="Number of dependents of the applicant."
#     )

#     Education = st.selectbox(
#         "Education",
#         ["Graduate", "Not Graduate"],
#         help="Education status of the applicant."
#     )

#     Self_Employed = st.selectbox(
#         "Self Employed",
#         ["No", "Yes"],
#         help="Whether the applicant is self-employed."
#     )

#     ApplicantIncome = st.text_input(
#         "Applicant Income",
#         placeholder="e.g. 7500",
#         help="Monthly income of the applicant. Example: ₹75,000 → enter 7500."
#     )

# with col2:
#     CoapplicantIncome = st.text_input(
#         "Coapplicant Income",
#         placeholder="e.g. 1500 or 0 if none",
#         help="Monthly income of the coapplicant. Enter 0 if there is no coapplicant."
#     )

#     LoanAmount = st.text_input(
#         "Loan Amount",
#         placeholder="e.g. 128 for ₹1,28,000",
#         help="Loan amount generally stored in thousands. Example: 128 means ₹1,28,000."
#     )

#     Loan_Amount_Term = st.text_input(
#         "Loan Amount Term (months)",
#         placeholder="e.g. 60 for 5 years / 360 for 30 years",
#         help="Loan repayment term in months."
#     )

#     Credit_History = st.selectbox(
#         "Credit History",
#         [1.0, 0.0],
#         format_func=lambda x: "1.0 (Good)" if x == 1.0 else "0.0 (Poor)",
#         help="1.0 means good credit history, 0.0 means poor/no credit history."
#     )

#     Property_Area = st.selectbox(
#         "Property Area",
#         ["Rural", "Semiurban", "Urban"],
#         help="Area where the property is located."
#     )

# st.markdown("<div class='spacer-20'></div>", unsafe_allow_html=True)

# predict_btn = st.button("🚀 Predict Loan Status")

# # ------------------ PREDICTION ------------------
# # ------------------ PREDICTION ------------------
# if predict_btn:
#     if not ApplicantIncome or not CoapplicantIncome or not LoanAmount or not Loan_Amount_Term:
#         st.warning("⚠️ Please fill all numeric fields before predicting.")
#     else:
#         try:
#             ApplicantIncome = float(ApplicantIncome)
#             CoapplicantIncome = float(CoapplicantIncome)
#             LoanAmount = float(LoanAmount)
#             Loan_Amount_Term = float(Loan_Amount_Term)

#             # -------- INPUT VALIDATION --------
#             if ApplicantIncome < 0:
#                 st.error("Applicant Income cannot be negative.")
#             elif CoapplicantIncome < 0:
#                 st.error("Coapplicant Income cannot be negative.")
#             elif LoanAmount <= 0:
#                 st.error("Loan Amount must be greater than 0.")
#             elif Loan_Amount_Term <= 0:
#                 st.error("Loan Amount Term must be greater than 0.")
#             else:
#                 status, probability = predict_loan(
#                     Gender,
#                     Married,
#                     Dependents,
#                     Education,
#                     Self_Employed,
#                     ApplicantIncome,
#                     CoapplicantIncome,
#                     LoanAmount,
#                     Loan_Amount_Term,
#                     Credit_History,
#                     Property_Area
#                 )

#                 probability_percent = round(probability * 100, 2)

#                 if probability_percent >= 80:
#                     confidence = "High"
#                 elif probability_percent >= 60:
#                     confidence = "Moderate"
#                 else:
#                     confidence = "Low"

#                 st.markdown("<div class='section-title'>✨ Prediction Result</div>", unsafe_allow_html=True)

#                 if status == "Approved":
#                     result_class = "result-approved"
#                     emoji = "✅"
#                     result_text = "Loan Approved"
#                     desc = "Based on the provided details, the applicant has a strong chance of loan approval."
#                 else:
#                     result_class = "result-rejected"
#                     emoji = "❌"
#                     result_text = "Loan Rejected"
#                     desc = "Based on the provided details, the applicant has a lower chance of loan approval."

#                 st.markdown(f'<div class="{result_class}">', unsafe_allow_html=True)

#                 rcol1, rcol2 = st.columns([1, 2])

#                 with rcol1:
#                     st.markdown(
#                         f"""
#                         <div style="text-align:center; padding-top:20px;">
#                             <p class="prob-big">{probability_percent}%</p>
#                             <p style="font-size:18px; color:#d1d5db; margin-top:-10px;">Approval Probability</p>
#                         </div>
#                         """,
#                         unsafe_allow_html=True
#                     )
#                     st.progress(min(probability, 1.0))

#                 with rcol2:
#                     st.markdown(
#                         f"""
#                         <h1 style="margin-bottom:0;">{emoji} {result_text}</h1>
#                         <p style="font-size:18px; color:#e5e7eb;">{desc}</p>
#                         """,
#                         unsafe_allow_html=True
#                     )

#                     b1, b2, b3 = st.columns(3)
#                     with b1:
#                         st.markdown(f"""
#                         <div class="mini-box">
#                             <div class="mini-label">Status</div>
#                             <div class="mini-value">{status}</div>
#                         </div>
#                         """, unsafe_allow_html=True)

#                     with b2:
#                         st.markdown(f"""
#                         <div class="mini-box">
#                             <div class="mini-label">Confidence</div>
#                             <div class="mini-value">{confidence}</div>
#                         </div>
#                         """, unsafe_allow_html=True)

#                     with b3:
#                         st.markdown("""
#                         <div class="mini-box">
#                             <div class="mini-label">Model</div>
#                             <div class="mini-value">Logistic Regression</div>
#                         </div>
#                         """, unsafe_allow_html=True)

#                 st.markdown("</div>", unsafe_allow_html=True)

#                 st.info("📌 This prediction is based on historical data and should be used as a reference, not as a final financial decision.")

#         except ValueError:
#             st.error("Please enter valid numeric values in income, loan amount, and loan term fields.")


# Very first basic style

# import streamlit as st
# import sys
# import os

# # Add project root to path so we can import from src
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from src.predict import predict_loan

# st.set_page_config(
#     page_title="Loan Approval Predictor",
#     page_icon="💰",
#     layout="centered"
# )

# # ---------------------------
# # Custom Styling
# # ---------------------------
# st.markdown("""
#     <style>
#     .main-title {
#         text-align: center;
#         font-size: 38px;
#         font-weight: 700;
#         color: #ffffff;
#         margin-bottom: 8px;
#     }
#     .sub-text {
#         text-align: center;
#         color: #cfcfcf;
#         font-size: 16px;
#         margin-bottom: 25px;
#     }
#     .note-box {
#         background-color: #1f2937;
#         padding: 12px 16px;
#         border-radius: 10px;
#         margin-bottom: 20px;
#         color: #e5e7eb;
#         font-size: 14px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # ---------------------------
# # Title Section
# # ---------------------------
# st.markdown('<div class="main-title">💰 Loan Approval Prediction App</div>', unsafe_allow_html=True)
# st.markdown(
#     '<div class="sub-text">Fill in the applicant details below to predict whether the loan will be approved or rejected.</div>',
#     unsafe_allow_html=True
# )

# st.markdown("""
# <div class="note-box">
# <b>Note:</b><br>
# • <b>Loan Amount</b> is usually entered in <b>thousands</b> (Example: 128 means ₹128,000)<br>
# • <b>Loan Amount Term</b> should be entered in <b>months</b> (Example: 360 means 30 years)
# </div>
# """, unsafe_allow_html=True)

# # ---------------------------
# # Input Form
# # ---------------------------
# col1, col2 = st.columns(2)

# with col1:
#     Gender = st.selectbox(
#         "Gender",
#         ["Male", "Female"],
#         help="Gender of the main applicant."
#     )

#     Married = st.selectbox(
#         "Married",
#         ["Yes", "No"],
#         help="Marital status of the applicant."
#     )

#     Dependents = st.selectbox(
#         "Dependents",
#         ["0", "1", "2", "3+"],
#         help="Number of dependents financially relying on the applicant."
#     )

#     Education = st.selectbox(
#         "Education",
#         ["Graduate", "Not Graduate"],
#         help="Education level of the applicant."
#     )

#     Self_Employed = st.selectbox(
#         "Self Employed",
#         ["No", "Yes"],
#         help="Whether the applicant is self-employed."
#     )

#     ApplicantIncome = st.text_input(
#         "Applicant Income",
#         placeholder="e.g. 4583",
#         help="Monthly income of the main applicant."
#     )

# with col2:
#     CoapplicantIncome = st.text_input(
#         "Coapplicant Income",
#         placeholder="e.g. 1508 or 0",
#         help="Monthly income of the co-applicant. Enter 0 if there is no co-applicant."
#     )

#     LoanAmount = st.text_input(
#         "Loan Amount",
#         placeholder="e.g. 128 (in thousands)",
#         help="Requested loan amount. Example: 128 means ₹128,000."
#     )

#     Loan_Amount_Term = st.text_input(
#         "Loan Amount Term",
#         placeholder="e.g. 360 (in months)",
#         help="Loan repayment term in months. Example: 360 means 30 years."
#     )

#     Credit_History = st.selectbox(
#         "Credit History",
#         [1.0, 0.0],
#         help="1 = good credit history, 0 = poor/no credit history."
#     )

#     Property_Area = st.selectbox(
#         "Property Area",
#         ["Rural", "Semiurban", "Urban"],
#         help="Area where the applicant's property is located."
#     )

# st.markdown("<br>", unsafe_allow_html=True)

# # ---------------------------
# # Prediction Button
# # ---------------------------
# if st.button("Predict Loan Status", use_container_width=True):
#     # Check empty fields
#     if not ApplicantIncome or not CoapplicantIncome or not LoanAmount or not Loan_Amount_Term:
#         st.warning("⚠️ Please fill all numeric fields before predicting.")
#     else:
#         try:
#             ApplicantIncome = float(ApplicantIncome)
#             CoapplicantIncome = float(CoapplicantIncome)
#             LoanAmount = float(LoanAmount)
#             Loan_Amount_Term = float(Loan_Amount_Term)

#             result = predict_loan(
#                 Gender,
#                 Married,
#                 Dependents,
#                 Education,
#                 Self_Employed,
#                 ApplicantIncome,
#                 CoapplicantIncome,
#                 LoanAmount,
#                 Loan_Amount_Term,
#                 Credit_History,
#                 Property_Area
#             )

#             st.markdown("<br>", unsafe_allow_html=True)

#             if result == "Approved":
#                 st.success("✅ Loan Approved")
#             else:
#                 st.error("❌ Loan Rejected")

#         except ValueError:
#             st.error("Please enter valid numeric values in income, loan amount, and loan term fields.")