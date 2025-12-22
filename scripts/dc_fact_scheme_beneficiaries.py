import pandas as pd
import numpy as np


dbt = pd.read_csv("dbt_schemewise_monthly_extended.csv")
dim_scheme = pd.read_csv("dim_scheme.csv")
dim_district = pd.read_csv("dim_district.csv")

SCHEME_NAME = "Post-Matric Scholarship for SC Students"

scheme_row = dim_scheme[
    dim_scheme["scheme_name"] == SCHEME_NAME
]

if scheme_row.empty:
    raise ValueError("Scheme not found in dim_scheme.csv")

scheme_id = scheme_row.iloc[0]["scheme_id"]

scheme_data = dbt[
    dbt["scheme_name"] == SCHEME_NAME
].copy()


districts = dim_district["district_id"].tolist()
n = len(districts)

np.random.seed(42)

weights = np.random.uniform(0.8, 1.2, size=n)
weights = weights / weights.sum()

district_weights = pd.DataFrame({
    "district_id": districts,
    "weight": weights
})


rows = []

for _, row in scheme_data.iterrows():
    total_beneficiaries = row["beneficiaries"]

    for _, d in district_weights.iterrows():
        rows.append({
            "scheme_id": scheme_id,
            "district_id": d["district_id"],
            "year": int(row["year"]),
            "month": int(row["month"]),
            "beneficiaries": int(total_beneficiaries * d["weight"])
        })

fact_scheme_beneficiaries = pd.DataFrame(rows)

original_totals = (
    scheme_data
    .groupby(["year", "month"])["beneficiaries"]
    .sum()
    .reset_index()
)

generated_totals = (
    fact_scheme_beneficiaries
    .groupby(["year", "month"])["beneficiaries"]
    .sum()
    .reset_index()
)

check = original_totals.merge(
    generated_totals,
    on=["year", "month"],
    suffixes=("_original", "_generated")
)

check["difference"] = (
    check["beneficiaries_generated"] -
    check["beneficiaries_original"]
)

print("Validation check:")
print(check.head())

fact_scheme_beneficiaries.to_csv(
    "fact_scheme_beneficiaries.csv",
    index=False
)

print("fact_scheme_beneficiaries.csv created")
print("Rows:", len(fact_scheme_beneficiaries))
print(fact_scheme_beneficiaries.head())
