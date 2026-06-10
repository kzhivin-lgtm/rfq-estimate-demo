import pandas as pd

from pricing import format_money
from estimate_config import (
    VAT_RATE,
    EMPLOYER_LOAD_RATE,
    LABOR_CONTINGENCY_RATE,
    WARRANTY_RESERVE_RATE,
    MANAGEMENT_BUFFER_RATE,
    DESIGN_BUREAU_COMMISSION_RATE,
    PRODUCTION_WORKERS,
    WORKDAYS_PER_MONTH,
    HOURS_PER_DAY,
    ROLE_RATES,
    MONTHLY_OVERHEAD_ROWS,
)

def format_unit_price(value):
    if value is None:
        return "—"

    if isinstance(value, float) and not value.is_integer():
        return f"₪{value:g}"

    return format_money(value)

# -----------------------------
# materials
# -----------------------------

def kitchen_island_materials_rows():
    return [
                {
            "category": "sheet materials",
            "item": "Birman 2650 Formica 16 mm",
            "unit": "2.44×1.22 m",
            "unit_price": 280,
            "qty": 3,
        },
        {
            "category": "sheet materials",
            "item": "Black back panel 5 mm",
            "unit": "2.44×1.22 m",
            "unit_price": 110,
            "qty": 1,
        },
        {
            "category": "sheet materials",
            "item": "Black MDF steel fronts 16 mm",
            "unit": "2.44×1.22 m",
            "unit_price": 1103,
            "qty": 2,
        },
        {
            "category": "sheet materials",
            "item": "Steel 304 0.8 mm wrapped fronts",
            "unit": "3.0×1.5 m",
            "unit_price": 520,
            "qty": 2,
        },
        {
            "category": "sheet materials",
            "item": "Stone Marble Laba Rosa 20 mm",
            "unit": "sqm",
            "unit_price": 2200,
            "qty": 6.3,
        },
        {
            "category": "hardware",
            "item": "Domicile 0583T handles",
            "unit": "pc",
            "unit_price": 36.5,
            "qty": 6,
        },
        {
            "category": "hardware",
            "item": "Blum hinges",
            "unit": "pc",
            "unit_price": 16.7,
            "qty": 8,
        },
        {
            "category": "hardware",
            "item": "Blum drawer runners",
            "unit": "set",
            "unit_price": 84.3,
            "qty": 3,
        },
        {
            "category": "hardware",
            "item": "Adjustable legs",
            "unit": "pc",
            "unit_price": 11.5,
            "qty": 10,
        },
        {
            "category": "consumables",
            "item": "Edge banding",
            "unit": "m",
            "unit_price": 8.5,
            "qty": 35,
        },
        {
            "category": "consumables",
            "item": "Screws / glue / sealant / fixings",
            "unit": "lot",
            "unit_price": 200,
            "qty": 1,
        },
        {
            "category": "consumables",
            "item": "Stone adhesive / sealant",
            "unit": "lot",
            "unit_price": 250,
            "qty": 1,
        },
        {
            "category": "packaging",
            "item": "Cardboard corner protectors",
            "unit": "pc 2 m",
            "unit_price": 5,
            "qty": 14,
        },
        {
            "category": "packaging",
            "item": "Stretch film",
            "unit": "roll",
            "unit_price": 45,
            "qty": 1,
        },
        {
            "category": "packaging",
            "item": "Foam wrap roll",
            "unit": "roll",
            "unit_price": 180,
            "qty": 1,
        },
        {
            "category": "packaging",
            "item": "Packing tape",
            "unit": "roll",
            "unit_price": 8.5,
            "qty": 2,
        },
    ]


def kitchen_island_materials_df():
    rows = []

    for row in kitchen_island_materials_rows():
        total = round(row["unit_price"] * row["qty"])

        rows.append(
            {
                "category": row["category"],
                "item": row["item"],
                "unit": row["unit"],
                "unit price": format_unit_price(row["unit_price"]),
                "qty": row["qty"],
                "total": format_money(total),
            }
        )

    return pd.DataFrame(rows)


def kitchen_island_materials_totals():
    subtotal = round(
        sum(row["unit_price"] * row["qty"] for row in kitchen_island_materials_rows())
    )
    vat = round(subtotal * VAT_RATE)
    total = subtotal + vat

    return subtotal, vat, total


# -----------------------------
# labor / works
# -----------------------------

def kitchen_island_labor_rows():
    return [
        {
            "group": "carpentry / production",
            "work": "CNC nesting / sheet optimization",
            "role": "CNC operator",
            "hours": 1.5,
            "rate": ROLE_RATES["CNC operator"],
        },
        {
            "group": "carpentry / production",
            "work": "CNC cutting / drilling / boring",
            "role": "CNC operator",
            "hours": 5,
            "rate": ROLE_RATES["CNC operator"],
        },
        {
            "group": "carpentry / production",
            "work": "Edge banding",
            "role": "carpenter",
            "hours": 3,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry / production",
            "work": "Island carcass / box assembly",
            "role": "carpenter",
            "hours": 8,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry / production",
            "work": "Drawer box assembly",
            "role": "carpenter",
            "hours": 3,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry / production",
            "work": "Hinges / runners / legs fitting",
            "role": "carpenter",
            "hours": 3,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry / production",
            "work": "Panel substrate prep",
            "role": "carpenter",
            "hours": 3,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry / production",
            "work": "SS panels bonding to substrate",
            "role": "carpenter",
            "hours": 4,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "assembly",
            "work": "Production pre-assembly / test fit",
            "role": "carpenter",
            "hours": 4,
            "rate": ROLE_RATES["carpenter"],
        },
                {
            "group": "stone work",
            "work": "Stone CNC cutting / sink and appliance cutouts",
            "role": "CNC operator",
            "hours": 6,
            "rate": ROLE_RATES["CNC operator"],
        },
        {
            "group": "stone work",
            "work": "Stone edge processing / polishing",
            "role": "carpenter",
            "hours": 6,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "assembly",
            "work": "Stone fitting / dry fit / final adjustment",
            "role": "carpenter",
            "hours": 3,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "metal work",
            "work": "Stainless drawings / laser files",
            "role": "metal worker",
            "hours": 2,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "metal work",
            "work": "Laser cutting, 0.8 mm sheets",
            "role": "metal worker",
            "hours": 3,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "metal work",
            "work": "Bending / folded edges",
            "role": "metal worker",
            "hours": 4,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "metal work",
            "work": "Metal QA / cleaning",
            "role": "metal worker",
            "hours": 1.5,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "packing / dispatch",
            "work": "Packing island panels",
            "role": "worker",
            "hours": 2,
            "rate": ROLE_RATES["worker"],
        },
        {
            "group": "packing / dispatch",
            "work": "Stone protection / padding",
            "role": "worker",
            "hours": 2,
            "rate": ROLE_RATES["worker"],
        },
        {
            "group": "packing / dispatch",
            "work": "Labeling / loading prep",
            "role": "worker",
            "hours": 1,
            "rate": ROLE_RATES["worker"],
        },
        {
            "group": "packing / dispatch",
            "work": "Truck loading",
            "role": "worker",
            "hours": 1,
            "rate": ROLE_RATES["worker"],
        },
    ]


def kitchen_island_direct_labor_hours():
    return sum(row["hours"] for row in kitchen_island_labor_rows())


def kitchen_island_direct_labor_cost():
    return sum(row["hours"] * row["rate"] for row in kitchen_island_labor_rows())


def kitchen_island_adjusted_labor_hours():
    return kitchen_island_direct_labor_hours() * (1 + LABOR_CONTINGENCY_RATE)


def kitchen_island_labor_totals():
    direct_cost = kitchen_island_direct_labor_cost()
    contingency_cost = round(direct_cost * LABOR_CONTINGENCY_RATE)
    base_with_contingency = round(direct_cost + contingency_cost)
    employer_load = round(base_with_contingency * EMPLOYER_LOAD_RATE)
    total = base_with_contingency + employer_load

    return base_with_contingency, employer_load, total


# -----------------------------
# overhead / reserves
# -----------------------------

def kitchen_island_monthly_capacity_hours():
    return PRODUCTION_WORKERS * WORKDAYS_PER_MONTH * HOURS_PER_DAY


def kitchen_island_monthly_overhead_group_rows():
    monthly_capacity_hours = kitchen_island_monthly_capacity_hours()
    object_hours = kitchen_island_adjusted_labor_hours()

    rows = []

    for row in MONTHLY_OVERHEAD_ROWS:
        object_cost = round(row["monthly_cost"] / monthly_capacity_hours * object_hours)

        rows.append(
            {
                "group": row["item"],
                "overhead_group": row["group"],
                "monthly_cost": row["monthly_cost"],
                "allocation": f"{round(object_hours, 1)}h / {monthly_capacity_hours}h",
                "vat_applicable": row["vat_applicable"],
                "object_cost": object_cost,
                "details": [row["item"]],
            }
        )

    return rows


def kitchen_island_base_cost_before_project_reserves():
    materials_subtotal, materials_vat, materials_total = kitchen_island_materials_totals()
    labor_base, employer_load, labor_total = kitchen_island_labor_totals()

    monthly_rows = kitchen_island_monthly_overhead_group_rows()

    monthly_overhead_cost = round(sum(row["object_cost"] for row in monthly_rows))
    monthly_overhead_taxable = round(
        sum(row["object_cost"] for row in monthly_rows if row["vat_applicable"])
    )
    monthly_overhead_vat = round(monthly_overhead_taxable * VAT_RATE)

    return materials_total + labor_total + monthly_overhead_cost + monthly_overhead_vat


def kitchen_island_project_reserve_rows():
    base_cost = kitchen_island_base_cost_before_project_reserves()

    return [
        {
            "group": "Warranty reserve",
            "overhead_group": "Project reserves",
            "monthly_cost": 0,
            "allocation": f"{int(WARRANTY_RESERVE_RATE * 100)}% of self-cost",
            "vat_applicable": True,
            "object_cost": round(base_cost * WARRANTY_RESERVE_RATE),
            "details": ["Warranty visits / corrections / small post-delivery fixes"],
        },
        {
            "group": "Management buffer",
            "overhead_group": "Project reserves",
            "monthly_cost": 0,
            "allocation": f"{int(MANAGEMENT_BUFFER_RATE * 100)}% of self-cost",
            "vat_applicable": True,
            "object_cost": round(base_cost * MANAGEMENT_BUFFER_RATE),
            "details": ["Project coordination / small mistakes / schedule friction"],
        },
        {
            "group": "Design bureau commission",
            "overhead_group": "Project reserves",
            "monthly_cost": 0,
            "allocation": f"{int(DESIGN_BUREAU_COMMISSION_RATE * 100)}% for this project",
            "vat_applicable": False,
            "object_cost": round(base_cost * DESIGN_BUREAU_COMMISSION_RATE),
            "details": ["Optional referral / architect commission"],
        },
    ]


def kitchen_island_overhead_rows():
    return kitchen_island_monthly_overhead_group_rows() + kitchen_island_project_reserve_rows()