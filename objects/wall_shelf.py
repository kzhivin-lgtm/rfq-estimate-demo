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


# -----------------------------
# materials
# -----------------------------

def wall_shelf_materials_rows():
    return [
                {
            "category": "sheet materials",
            "item": "Oak veneer board 16 mm",
            "unit": "2.44×1.22 m",
            "unit_price": 950,
            "qty": 6,
        },
        {
            "category": "consumables",
            "item": "Oak veneer edging / front lipping",
            "unit": "m",
            "unit_price": 24,
            "qty": 32,
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
            "item": "Corten 1 mm sheet",
            "unit": "3.0×1.5 m",
            "unit_price": 800,
            "qty": 2,
        },
        {
            "category": "hardware",
            "item": "Hidden wall mounting rail",
            "unit": "lot",
            "unit_price": 550,
            "qty": 1,
        },
        {
            "category": "hardware",
            "item": "Heavy-duty wall anchors",
            "unit": "lot",
            "unit_price": 260,
            "qty": 1,
        },
        {
            "category": "hardware",
            "item": "LED strip + aluminum profile",
            "unit": "lot",
            "unit_price": 750,
            "qty": 1,
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
            "item": "Sanding / finishing consumables",
            "unit": "lot",
            "unit_price": 260,
            "qty": 1,
        },
                {
            "category": "packaging",
            "item": "Cardboard corner protectors",
            "unit": "pc 2 m",
            "unit_price": 5,
            "qty": 12,
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
            "qty": 4,
        },
    ]


def wall_shelf_materials_totals():
    subtotal = round(
        sum(row["unit_price"] * row["qty"] for row in wall_shelf_materials_rows())
    )
    vat = round(subtotal * VAT_RATE)
    total = subtotal + vat

    return subtotal, vat, total


# -----------------------------
# labor / works
# -----------------------------

def wall_shelf_labor_rows():
    return [
        {
            "group": "technical prep",
            "work": "Production drawings / CNC file prep",
            "role": "CNC operator",
            "hours": 2,
            "rate": ROLE_RATES["CNC operator"],
        },
        {
            "group": "cnc",
            "work": "CNC nesting / sheet optimization",
            "role": "CNC operator",
            "hours": 1,
            "rate": ROLE_RATES["CNC operator"],
        },
        {
            "group": "cnc",
            "work": "CNC cutting / drilling / boring",
            "role": "CNC operator",
            "hours": 3.5,
            "rate": ROLE_RATES["CNC operator"],
        },
        {
            "group": "carpentry",
            "work": "Edge banding / veneer lipping",
            "role": "carpenter",
            "hours": 4,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry",
            "work": "Oak veneer shelf carcass fabrication",
            "role": "carpenter",
            "hours": 8,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "carpentry",
            "work": "Vertical partitions layout / fitting",
            "role": "carpenter",
            "hours": 6,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "assembly",
            "work": "End panels / alignment / test fit",
            "role": "carpenter",
            "hours": 4,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "assembly",
            "work": "LED routing / profile pre-fit",
            "role": "carpenter",
            "hours": 2,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "metal work",
            "work": "Corten laser files / production prep",
            "role": "metal worker",
            "hours": 1.5,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "metal work",
            "work": "Corten laser cutting / shearing",
            "role": "metal worker",
            "hours": 3,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "metal work",
            "work": "Corten bending / folded edges",
            "role": "metal worker",
            "hours": 3,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "metal work",
            "work": "Metal cleaning / finish prep for corten partitions",
            "role": "metal worker",
            "hours": 1,
            "rate": ROLE_RATES["metal worker"],
        },
        {
            "group": "assembly",
            "work": "Corten partitions fitting / installation",
            "role": "carpenter",
            "hours": 3,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "assembly",
            "work": "Final QA / disassembly for delivery",
            "role": "carpenter",
            "hours": 2,
            "rate": ROLE_RATES["carpenter"],
        },
        {
            "group": "packing / dispatch",
            "work": "Packing shelf parts",
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


def wall_shelf_direct_labor_hours():
    return sum(row["hours"] for row in wall_shelf_labor_rows())


def wall_shelf_direct_labor_cost():
    return sum(row["hours"] * row["rate"] for row in wall_shelf_labor_rows())


def wall_shelf_adjusted_labor_hours():
    return wall_shelf_direct_labor_hours() * (1 + LABOR_CONTINGENCY_RATE)


def wall_shelf_labor_totals():
    direct_cost = wall_shelf_direct_labor_cost()
    contingency_cost = round(direct_cost * LABOR_CONTINGENCY_RATE)
    base_with_contingency = round(direct_cost + contingency_cost)
    employer_load = round(base_with_contingency * EMPLOYER_LOAD_RATE)
    total = base_with_contingency + employer_load

    return base_with_contingency, employer_load, total


# -----------------------------
# overhead / reserves
# -----------------------------

def wall_shelf_monthly_capacity_hours():
    return PRODUCTION_WORKERS * WORKDAYS_PER_MONTH * HOURS_PER_DAY


def wall_shelf_monthly_overhead_group_rows():
    monthly_capacity_hours = wall_shelf_monthly_capacity_hours()
    object_hours = wall_shelf_adjusted_labor_hours()

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


def wall_shelf_base_cost_before_project_reserves():
    materials_subtotal, materials_vat, materials_total = wall_shelf_materials_totals()
    labor_base, employer_load, labor_total = wall_shelf_labor_totals()

    monthly_rows = wall_shelf_monthly_overhead_group_rows()

    monthly_overhead_cost = round(sum(row["object_cost"] for row in monthly_rows))
    monthly_overhead_taxable = round(
        sum(row["object_cost"] for row in monthly_rows if row["vat_applicable"])
    )
    monthly_overhead_vat = round(monthly_overhead_taxable * VAT_RATE)

    return materials_total + labor_total + monthly_overhead_cost + monthly_overhead_vat


def wall_shelf_project_reserve_rows():
    base_cost = wall_shelf_base_cost_before_project_reserves()

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


def wall_shelf_overhead_rows():
    return wall_shelf_monthly_overhead_group_rows() + wall_shelf_project_reserve_rows()