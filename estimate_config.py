# -----------------------------
# global estimate configuration
# -----------------------------

VAT_RATE = 0.18

EMPLOYER_LOAD_RATE = 0.25
LABOR_CONTINGENCY_RATE = 0.10

WARRANTY_RESERVE_RATE = 0.05
MANAGEMENT_BUFFER_RATE = 0.05
DESIGN_BUREAU_COMMISSION_RATE = 0.00

PRODUCTION_WORKERS = 12
WORKDAYS_PER_MONTH = 21
HOURS_PER_DAY = 8

SALE_PRICE_MARKUP_RATE = 0.30

DELIVERY_RATE = 0.03
INSTALLATION_RATE = 0.10


# -----------------------------
# labor rates, excl. VAT
# -----------------------------

ROLE_RATES = {
    "estimator / PM": 120,
    "CNC operator": 80,
    "carpenter": 80,
    "metal worker": 80,
    "worker": 60,
}


# -----------------------------
# monthly overhead, excl. VAT
# -----------------------------

MONTHLY_OVERHEAD_ROWS = [
    # Back-office payroll — no VAT
    {
        "group": "Back-office payroll",
        "item": "Accountant salary + 25%",
        "monthly_cost": 16250,
        "vat_applicable": False,
    },
    {
        "group": "Back-office payroll",
        "item": "Constructor salary + 25%",
        "monthly_cost": 16250,
        "vat_applicable": False,
    },
    {
        "group": "Back-office payroll",
        "item": "Project manager salary + 25%",
        "monthly_cost": 16250,
        "vat_applicable": False,
    },

    # Facility / rent / arnona
    {
        "group": "Facility / rent / arnona",
        "item": "Rent",
        "monthly_cost": 10000,
        "vat_applicable": True,
    },
    {
        "group": "Facility / rent / arnona",
        "item": "Arnona",
        "monthly_cost": 2500,
        "vat_applicable": False,
    },
    {
        "group": "Facility / rent / arnona",
        "item": "Maintenance fee",
        "monthly_cost": 1200,
        "vat_applicable": True,
    },

    # Utilities / safety
    {
        "group": "Utilities / safety",
        "item": "Electricity",
        "monthly_cost": 7500,
        "vat_applicable": True,
    },
    {
        "group": "Utilities / safety",
        "item": "Water",
        "monthly_cost": 350,
        "vat_applicable": True,
    },
    {
        "group": "Utilities / safety",
        "item": "Compressed air / gas",
        "monthly_cost": 650,
        "vat_applicable": True,
    },
    {
        "group": "Utilities / safety",
        "item": "Insurance / safety / fire",
        "monthly_cost": 1200,
        "vat_applicable": True,
    },

    # Machinery / equipment
    {
        "group": "Machinery / equipment",
        "item": "Equipment depreciation",
        "monthly_cost": 5000,
        "vat_applicable": True,
    },
    {
        "group": "Machinery / equipment",
        "item": "Machine consumables / wear",
        "monthly_cost": 4500,
        "vat_applicable": True,
    },

    # Software / shop supplies / waste
    {
        "group": "Software / shop supplies / waste",
        "item": "Software subscriptions",
        "monthly_cost": 1500,
        "vat_applicable": True,
    },
    {
        "group": "Software / shop supplies / waste",
        "item": "Shop supplies / cleaning",
        "monthly_cost": 1000,
        "vat_applicable": True,
    },
    {
        "group": "Software / shop supplies / waste",
        "item": "Waste removal",
        "monthly_cost": 700,
        "vat_applicable": True,
    },
]