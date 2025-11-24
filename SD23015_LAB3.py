import streamlit as st
import json
import operator

st.title("🎓 Scholarship Advisory Rule-Based System")

# =========================================
# JSON RULES
# =========================================
rules_json = """
[
  {
    "name": "Top merit candidate",
    "priority": 100,
    "conditions": [
      ["cgpa", ">=", 3.7],
      ["co_curricular_score", ">=", 80],
      ["family_income", "<=", 8000],
      ["disciplinary_actions", "==", 0]
    ],
    "action": {
      "decision": "AWARD_FULL",
      "reason": "Excellent academic & co-curricular performance, with acceptable need"
    }
  },
  {
    "name": "Good candidate - partial scholarship",
    "priority": 80,
    "conditions": [
      ["cgpa", ">=", 3.3],
      ["co_curricular_score", ">=", 60],
      ["family_income", "<=", 12000],
      ["disciplinary_actions", "<=", 1]
    ],
    "action": {
      "decision": "AWARD_PARTIAL",
      "reason": "Good academic & involvement record with moderate need"
    }
  },
  {
    "name": "Need-based review",
    "priority": 70,
    "conditions": [
      ["cgpa", ">=", 2.5],
      ["family_income", "<=", 4000]
    ],
    "action": {
      "decision": "REVIEW",
      "reason": "High need but borderline academic score"
    }
  },
  {
    "name": "Low CGPA – not eligible",
    "priority": 95,
    "conditions": [
      ["cgpa", "<", 2.5]
    ],
    "action": {
      "decision": "REJECT",
      "reason": "CGPA below minimum scholarship requirement"
    }
  },
  {
    "name": "Serious disciplinary record",
    "priority": 90,
    "conditions": [
      ["disciplinary_actions", ">=", 2]
    ],
    "action": {
      "decision": "REJECT",
      "reason": "Too many disciplinary records"
    }
  }
]
"""

rules = json.loads(rules_json)

# =========================================
# Rule engine functions
# =========================================
op_map = {
    "==": operator.eq,
    "!=": operator.ne,
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt
}

def evaluate_rule(rule, applicant):
    for field, op, value in rule["conditions"]:
        if not op_map[op](applicant.get(field), value):
            return False
    return True

def run_rule_engine(rules, applicant):
    sorted_rules = sorted(rules, key=lambda r: r["priority"], reverse=True)
    for rule in sorted_rules:
        if evaluate_rule(rule, applicant):
            return rule
    return None


# =========================================
# Streamlit user input form
# =========================================
st.subheader("📌 Applicant Information")

cgpa = st.number_input("CGPA", min_value=0.0, max_value=4.0, step=0.01)
co_curricular = st.number_input("Co-curricular Score", min_value=0, max_value=100)
income = st.number_input("Family Income (RM)", min_value=0)
disciplinary = st.number_input("Number of Disciplinary Actions", min_value=0, max_value=10)

if st.button("Evaluate Scholarship"):
    applicant = {
        "cgpa": cgpa,
        "co_curricular_score": co_curricular,
        "family_income": income,
        "disciplinary_actions": disciplinary
    }

    result = run_rule_engine(rules, applicant)

    if result:
        st.success(f"🎉 Decision: **{result['action']['decision']}**")
        st.info(f"Reason: {result['action']['reason']}")
        st.write(f"Matched Rule: **{result['name']}**")
    else:
        st.warning("No matching scholarship rule found.")
