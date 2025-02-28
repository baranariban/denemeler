import streamlit as st
import pandas as pd
import altair as alt

st.title("CompApp - Composite Application")
st.markdown("### :red[by Ali Baran Arıban]")
st.title("Composite Grader Version 2.0")
st.write("Write the thermal and physical properties of the composite below. The table shows grades, while the chart shows weighted contributions to the total grade.")

if "grades_data" not in st.session_state:
    st.session_state.grades_data = pd.DataFrame()

if "contributions_data" not in st.session_state:
    st.session_state.contributions_data = pd.DataFrame()

composite = st.text_input("Type of the composite (UNFILLED, GF, CF, MINERAL, CONDUCTIVE): ")
ifss = st.number_input("Interfacial Properties with Carbon Fiber (IFSS, in MPa): ")
cte = st.number_input("Coefficient of Thermal Expansion (CTE, in microstrain/°C): ")
tg = st.number_input("Glass Transition Temperature (Tg, in °C): ")
cost = st.number_input("Cost (in USD/kg): ")
strength = st.number_input("Strength (Tensile Modulus or Flexural Modulus, in GPa): ")
tp = st.number_input("Processing Temperature (Tp, in °C): ")
shrinkage = st.number_input("Shrinkage (in %): ")
density = st.number_input("Density (in kg/m^3): ")

# Calculate Grades (Values between 0 and 3)
ifss_grade = 3.00 if ifss >= 100 else round(3.00 - 3.00 * ((100 - ifss) / 100), 2)
cte_grade = round(3.00 - 3.00 * ((7.5 - cte) / (144 - 7.5)), 2) if 0 < cte < 144 else 0
tg_grade = 3.00 if tg >= 180 else 0
cost_grade = round(3.00 - 3.00 * ((0 - cost) / (0 - 117.5)), 2) if cost < 117.5 else 0
strength_grade = round(3.00 - 3.00 * ((18 - strength) / 18), 2) if strength < 18 else 3.00
tp_grade = round(3.00 - 3.00 * ((119.5 - tp) / (119.5 - 400)), 2) if 119.5 < tp < 400 else (3.00 if tp <= 119.5 else 0)
shrinkage_grade = round(3.00 - 3.00 * ((0.5 - shrinkage) / (0.5 - 1.5)), 2) if 0.5 < shrinkage < 1.5 else (3.00 if shrinkage <= 0.5 else 0)
density_grade = round(3.00 - 3.00 * ((1400 - density) / (1400 - 2000)), 2) if 1000 < density < 2000 else 0

# Apply Weights for Contributions
ifss_contribution = ifss_grade * 20
cte_contribution = cte_grade * 20
tg_contribution = tg_grade * 15
cost_contribution = cost_grade * 12.5
strength_contribution = strength_grade * 12.5
tp_contribution = tp_grade * 10
shrinkage_contribution = shrinkage_grade * 5
density_contribution = density_grade * 5

# Compute Total Grade
total_grade = round((ifss_contribution + cte_contribution + tg_contribution + cost_contribution +
                     strength_contribution + tp_contribution + shrinkage_contribution + density_contribution) / 3.00, 2)

if st.button("Add Entry"):
    # Store raw grades in one table
    new_grades_entry = {
        "IFSS Grade": ifss_grade,
        "CTE Grade": cte_grade,
        "Tg Grade": tg_grade,
        "Cost Grade": cost_grade,
        "Strength Grade": strength_grade,
        "Tp Grade": tp_grade,
        "Shrinkage Grade": shrinkage_grade,
        "Density Grade": density_grade,
        "Total Grade": total_grade
    }
    st.session_state.grades_data[composite] = pd.Series(new_grades_entry)

    # Store weighted contributions separately for the chart
    new_contributions_entry = {
        "IFSS Contribution": ifss_contribution,
        "CTE Contribution": cte_contribution,
        "Tg Contribution": tg_contribution,
        "Cost Contribution": cost_contribution,
        "Strength Contribution": strength_contribution,
        "Tp Contribution": tp_contribution,
        "Shrinkage Contribution": shrinkage_contribution,
        "Density Contribution": density_contribution
    }
    st.session_state.contributions_data[composite] = pd.Series(new_contributions_entry)

# Display the Table of Grades
st.write("### Composite Property Grades (Values Between 0 and 3)")
st.write(st.session_state.grades_data)

# Display the Chart of Contributions
if not st.session_state.contributions_data.empty:
    chart_data = st.session_state.contributions_data.reset_index().melt(id_vars="index", var_name="Composite", value_name="Contribution")
    chart = alt.Chart(chart_data).mark_bar().encode(
        x="Composite:N",
        y="Contribution:Q",
        color="index:N",
        tooltip=["Composite", "index", "Contribution"]
    ).properties(
        width=800,
        height=500,
        title="Weighted Contributions to Total Grade"
    )
    st.altair_chart(chart, use_container_width=True)
