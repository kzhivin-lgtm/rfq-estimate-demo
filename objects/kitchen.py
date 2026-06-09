import pandas as pd

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
from pricing import format_money


def format_unit_price(value):
    if value is None:
        return "—"

    if isinstance(value, float) and not value.is_integer():
        return f"₪{value:g}"

    return format_money(value)


# -----------------------------
# materials / hardware / packaging
# -----------------------------

def kitchen_materials_rows():
    return [
        {
            "category": "sheet materials",
            "item": "Birman 2650 Formica laminate",
            "unit": "sheet",
            "unit_price": 146,
            "qty": 5,
        },
        {
            "category": "sheet materials",
            "item": "17 mm chipboard / melamine substrate",
            "unit": "sheet 2.44×1.22 m",
            "unit_price": 246,
            "qty": 5,
        },
        {
            "category": "sheet materials",
            "item": "5 mm back panels",
            "unit": "sheet 2.44×1.22 m",
            "unit_price": 93,
            "qty": 2,
        },
        {
            "category": "sheet materials",
            "item": "Oak veneer board",
            "unit": "sheet 2.44×1.22 m",
            "unit_price": 950,
            "qty": 2,
        },
        {
            "category": "sheet materials",
            "item": "Black MDF substrate for SS fronts",
            "unit": "sheet 2.44×1.22 m",
            "unit_price": 1103,
            "qty": 3,
        },
        {
            "category": "sheet materials",
            "item": "SS sheet 304, 0.8 mm, wrapped fronts",
            "unit": "sheet 3.0×1.5 m",
            "unit_price": 260,
            "qty": 3,
        },
        {
            "category": "sheet materials",
            "item": "SS sheet 304, 2 mm, countertop / backsplash / toe kick",
            "unit": "sheet 3.0×1.5 m",
            "unit_price": 640,
            "qty": 2,
        },
        {
            "category": "hardware",
            "item": "Domicile 0583T handles",
            "unit": "pc",
            "unit_price": 36.5,
            "qty": 12,
        },
        {
            "category": "hardware",
            "item": "Blum hinges",
            "unit": "pc",
            "unit_price": 16.7,
            "qty": 16,
        },
        {
            "category": "hardware",
            "item": "Blum drawer runners",
            "unit": "set",
            "unit_price": 84.3,
            "qty": 4,
        },
        {
            "category": "hardware",
            "item": "Adjustable legs",
            "unit": "pc",
            "unit_price": 11.5,
            "qty": 14,
        },
        {
            "category": "consumables",
            "item": "Edge banding",
            "unit": "m",
            "unit_price": 8.5,
            "qty": 60,
        },
        {
            "category": "consumables",
            "item": "Screws / glue / sealant / fixings",
            "unit": "lot",
            "unit_price": 450,
            "qty": 1,
        },
        {
            "category": "packaging",
            "item": "Cardboard corner protectors",
            "unit": "pc 2 m",
            "unit_price": 5,
            "qty": 20,
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
            "qty": 3,
        },
    ]


def kitchen_materials_df():
    rows = []

    for row in kitchen_materials_rows():
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


def kitchen_materials_totals():
    subtotal = round(
        sum(row["unit_price"] * row["qty"] for row in kitchen_materials_rows())
    )
    vat = round(subtotal * VAT_RATE)
    total = subtotal + vat

    return subtotal, vat, total


# -----------------------------
# labor / works
# -----------------------------

def kitchen_labor_rows():
    return [
        {
            "group": "carpentry / production",
            "work": "CNC nesting / sheet optimization",
            "role": "CNC operator",
            "hours": 2,
            "rate": ROLE_RATES["CNC operator"],
        },
        {
            "group": "carpentry / production",
            "work": "CNC cutting / drilling / boring",
            "role": "CNC operator",
            "hours": 8,
            "rate": ROLE_RATES["CNC operator"],
        },
        {
            "group": "carpentry / production",
            "work": "Edge banding",
            "role": "carpenter",
            "hours": 5,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry / production",
            "work": "Carcass / box assembly",
            "role": "carpenter",
            "hours": 12,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry / production",
            "work": "Drawer box assembly",
            "role": "carpenter",
            "hours": 4,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry / production",
            "work": "Hinges / runners / legs fitting",
            "role": "carpenter",
            "hours": 5,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry / production",
            "work": "Front substrate prep",
            "role": "carpenter",
            "hours": 4,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry / production",
            "work": "SS fronts bonding to substrate",
            "role": "carpenter",
            "hours": 6,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry / production",
            "work": "Production pre-assembly / test fit",
            "role": "carpenter",
            "hours": 5,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry / production",
            "work": "Partial disassembly / dispatch prep",
            "role": "carpenter",
            "hours": 2,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "metal work",
            "work": "Stainless drawings / laser files",
            "role": "metal worker",
            "hours": 3,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "metal work",
            "work": "Laser cutting, 0.8 mm sheets",
            "role": "metal worker",
            "hours": 4,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "metal work",
            "work": "Laser cutting, 2 mm sheets",
            "role": "metal worker",
            "hours": 3,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "metal work",
            "work": "Bending / folded edges",
            "role": "metal worker",
            "hours": 6,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "metal work",
            "work": "Countertop / backsplash dry fit prep",
            "role": "metal worker",
            "hours": 3,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "metal work",
            "work": "Toe kick metal prep",
            "role": "metal worker",
            "hours": 2,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "metal work",
            "work": "Metal QA / cleaning",
            "role": "metal worker",
            "hours": 2,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "packing / dispatch",
            "work": "Packing fronts and panels",
            "role": "worker",
            "hours": 3,
            "rate": ROLE_RATES["worker"],
        },
        {
            "group": "packing / dispatch",
            "work": "Packing carcass boxes",
            "role": "worker",
            "hours": 3,
            "rate": ROLE_RATES["worker"],
        },
        {
            "group": "packing / dispatch",
            "work": "Labeling / loading prep",
            "role": "worker",
            "hours": 2,
            "rate": ROLE_RATES["worker"],
        },
    ]


def kitchen_direct_labor_hours():
    return sum(row["hours"] for row in kitchen_labor_rows())


def kitchen_direct_labor_cost():
    return sum(row["hours"] * row["rate"] for row in kitchen_labor_rows())


def kitchen_adjusted_labor_hours():
    return kitchen_direct_labor_hours() * (1 + LABOR_CONTINGENCY_RATE)


def kitchen_labor_df():
    rows = []

    for row in kitchen_labor_rows():
        base_cost = round(row["hours"] * row["rate"])

        rows.append(
            {
                "group": row["group"],
                "work": row["work"],
                "role": row["role"],
                "hours": row["hours"],
                "rate": format_money(row["rate"]),
                "base cost": format_money(base_cost),
            }
        )

    contingency_hours = round(kitchen_direct_labor_hours() * LABOR_CONTINGENCY_RATE, 1)
    contingency_cost = round(kitchen_direct_labor_cost() * LABOR_CONTINGENCY_RATE)

    rows.append(
        {
            "group": "contingency",
            "work": "Production contingency 10%",
            "role": "all roles",
            "hours": contingency_hours,
            "rate": f"{int(LABOR_CONTINGENCY_RATE * 100)}%",
            "base cost": format_money(contingency_cost),
        }
    )

    return pd.DataFrame(rows)


def kitchen_labor_totals():
    direct_cost = kitchen_direct_labor_cost()
    contingency_cost = round(direct_cost * LABOR_CONTINGENCY_RATE)
    base_with_contingency = round(direct_cost + contingency_cost)
    employer_load = round(base_with_contingency * EMPLOYER_LOAD_RATE)
    total = base_with_contingency + employer_load

    return base_with_contingency, employer_load, total


# -----------------------------
# overhead / reserves
# -----------------------------

def kitchen_monthly_capacity_hours():
    return PRODUCTION_WORKERS * WORKDAYS_PER_MONTH * HOURS_PER_DAY


def kitchen_monthly_overhead_group_rows():
    monthly_capacity_hours = kitchen_monthly_capacity_hours()
    object_hours = kitchen_adjusted_labor_hours()

    grouped = {}

    for row in MONTHLY_OVERHEAD_ROWS:
        group = row["group"]
        object_cost = round(row["monthly_cost"] / monthly_capacity_hours * object_hours)

        if group not in grouped:
            grouped[group] = {
                "group": group,
                "monthly_cost": 0,
                "allocation": f"{round(object_hours, 1)}h / {monthly_capacity_hours}h",
                "vat_applicable": False,
                "object_cost": 0,
                "details": [],
            }

        grouped[group]["monthly_cost"] += row["monthly_cost"]
        grouped[group]["object_cost"] += object_cost
        grouped[group]["details"].append(row["item"])

        if row["vat_applicable"]:
            grouped[group]["vat_applicable"] = True

    return list(grouped.values())


def kitchen_base_cost_before_project_reserves():
    materials_subtotal, materials_vat, materials_total = kitchen_materials_totals()
    labor_base, employer_load, labor_total = kitchen_labor_totals()

    monthly_rows = kitchen_monthly_overhead_group_rows()

    monthly_overhead_cost = round(sum(row["object_cost"] for row in monthly_rows))
    monthly_overhead_taxable = round(
        sum(row["object_cost"] for row in monthly_rows if row["vat_applicable"])
    )
    monthly_overhead_vat = round(monthly_overhead_taxable * VAT_RATE)

    return materials_total + labor_total + monthly_overhead_cost + monthly_overhead_vat


def kitchen_project_reserve_rows():
    base_cost = kitchen_base_cost_before_project_reserves()

    return [
        {
            "group": "warranty reserve",
            "monthly_cost": 0,
            "allocation": f"{int(WARRANTY_RESERVE_RATE * 100)}% of self-cost",
            "vat_applicable": False,
            "object_cost": round(base_cost * WARRANTY_RESERVE_RATE),
            "details": ["Warranty visits / corrections / small post-delivery fixes"],
        },
        {
            "group": "management buffer",
            "monthly_cost": 0,
            "allocation": f"{int(MANAGEMENT_BUFFER_RATE * 100)}% of self-cost",
            "vat_applicable": False,
            "object_cost": round(base_cost * MANAGEMENT_BUFFER_RATE),
            "details": ["Project coordination / small mistakes / schedule friction"],
        },
        {
            "group": "design bureau commission",
            "monthly_cost": 0,
            "allocation": f"{int(DESIGN_BUREAU_COMMISSION_RATE * 100)}% for this project",
            "vat_applicable": False,
            "object_cost": round(base_cost * DESIGN_BUREAU_COMMISSION_RATE),
            "details": ["Optional referral / architect commission"],
        },
    ]


def kitchen_overhead_rows():
    return kitchen_monthly_overhead_group_rows() + kitchen_project_reserve_rows()


def kitchen_overhead_df():
    rows = []

    for row in kitchen_overhead_rows():
        rows.append(
            {
                "group": row["group"],
                "monthly cost": format_money(row["monthly_cost"]) if row["monthly_cost"] else "—",
                "allocation": row["allocation"],
                "VAT": "yes" if row["vat_applicable"] else "no",
                "kitchen cost": format_money(row["object_cost"]),
            }
        )

    return pd.DataFrame(rows)


def kitchen_overhead_totals():
    rows = kitchen_overhead_rows()

    subtotal = round(sum(row["object_cost"] for row in rows))
    taxable_subtotal = round(
        sum(row["object_cost"] for row in rows if row["vat_applicable"])
    )
    vat = round(taxable_subtotal * VAT_RATE)
    total = subtotal + vat

    return subtotal, vat, total


# -----------------------------
# self cost
# -----------------------------

def kitchen_self_cost_totals():
    materials_subtotal, materials_vat, materials_total = kitchen_materials_totals()
    labor_base, employer_load, labor_total = kitchen_labor_totals()
    overhead_subtotal, overhead_vat, overhead_total = kitchen_overhead_totals()

    subtotal_excl_vat = materials_subtotal + labor_total + overhead_subtotal
    vat_total = materials_vat + overhead_vat
    total = materials_total + labor_total + overhead_total

    return subtotal_excl_vat, vat_total, total