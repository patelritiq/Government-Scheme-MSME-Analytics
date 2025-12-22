import pandas as pd
import numpy as np


dbt_clean = pd.read_csv("dbt_schemewise_monthly_clean.csv")


scheme_name = "Post-Matric Scholarship for SC Students"

base = dbt_clean[
    dbt_clean["scheme_name"] == scheme_name
].copy()


if base.empty:
    raise ValueError("Base scheme not found in clean dataset")


dates = pd.date_range(start="2019-01-01", end="2022-12-01", freq="MS")

synthetic = pd.DataFrame({
    "year": dates.year,
    "month": dates.month
})

synthetic["scheme_name"] = scheme_name

BASE_VALUE = base["beneficiaries"].mean()
np.random.seed(42)

def generate_value(year):
    if year == 2020:
        factor = 0.85 
    elif year == 2021:
        factor = 1.05
    elif year == 2022:
        factor = 1.2
    else:
        factor = 1.0
    noise = np.random.uniform(0.95, 1.05)
    return int(BASE_VALUE * factor * noise)

synthetic["beneficiaries"] = synthetic["year"].apply(generate_value)

extended = pd.concat([base, synthetic], ignore_index=True)
extended = extended.sort_values(["year", "month"])


extended.to_csv(
    "dbt_schemewise_monthly_extended.csv",
    index=False
)

print("dbt_schemewise_monthly_extended.csv created")
print("Rows:", len(extended))
print(extended.tail())
