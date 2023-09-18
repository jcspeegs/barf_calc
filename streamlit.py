import streamlit as st
import yaml
from importlib.resources import files
import pandas as pd
import altair as alt
import barf_calc as bc


def presets_parse(fl) -> dict:
    with open(fl, "r") as f:
        presets = yaml.safe_load(f)
    return bc.Presets(presets)


def add_to_meal(meal, food_type, food_weight):
    food = bc.Food(presets, food_type, food_weight)
    meal.add_food(food)


PRESETS = files("barf_calc").joinpath("presets.yaml")
presets = presets_parse(PRESETS)

if st.session_state.get("meal") is None:
    st.session_state.meal = bc.Meal()

st.title("B.A.R.F. Meal Calculator")

meal = st.session_state.meal
# st.write(meal)

st.metric("Total Weight", meal.weight)

chart = pd.DataFrame(
    {"category": meal.components.keys(), "value": meal.components.values()}
)
chart = alt.Chart(chart).mark_arc().encode(theta="value", color="category")
st.altair_chart(chart, use_container_width=True)

c0, c1 = st.columns((3, 1))
food_type = c0.selectbox(
    "Add an ingreident to your meal",
    presets.ids,
    format_func=lambda id: presets.presets.get(id).description,
)
food_weight = c1.number_input("Weight (lbs)", format="%.2f")
c0.button(
    "Add to meal",
    on_click=add_to_meal,
    args=(st.session_state.meal, food_type, food_weight),
)
