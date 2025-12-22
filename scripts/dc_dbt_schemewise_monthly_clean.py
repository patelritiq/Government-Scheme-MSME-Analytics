import pandas as pd

dbt_raw = pd.read_csv("DBT_Schemewise_Beneficiaries_Aadhaar_Banking.csv")

dbt = dbt_raw[[
    "Name of the Scheme",
    "Periodicity - ending Month & Year",
    "Total No. of beneficiaries"
]].copy()

dbt = dbt.rename(columns={
    "Name of the Scheme": "scheme_name",
    "Periodicity - ending Month & Year": "period",
    "Total No. of beneficiaries": "beneficiaries"
})

dbt["beneficiaries"] = (
    dbt["beneficiaries"]
    .astype(str)
    .str.replace(",", "")
)

dbt["beneficiaries"] = pd.to_numeric(
    dbt["beneficiaries"],
    errors="coerce"
)

dbt["period"] = pd.to_datetime(
    dbt["period"].astype(str).str.strip(),
    format="%b-%y",
    errors="coerce"
)

dbt = dbt.dropna(subset=["period", "beneficiaries"])


dbt["year"] = dbt["period"].dt.year
dbt["month"] = dbt["period"].dt.month


dbt_clean = (
    dbt
    .groupby(["scheme_name", "year", "month"], as_index=False)
    .agg({"beneficiaries": "sum"})
)


dbt_clean.to_csv("dbt_schemewise_monthly_clean.csv", index=False)

print("dbt_schemewise_monthly_clean.csv created")
print("Rows:", len(dbt_clean))
print(dbt_clean.head())