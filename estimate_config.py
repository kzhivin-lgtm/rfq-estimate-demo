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

SALE_PRICE_MARKUP_RATE = 1.00

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
    {
        "group": "facility / rent",
        "item": "Rent",
        "monthly_cost": 10000,
        "vat_applicable": True,
    },
    {
        "group": "facility / rent",
        "item": "Arnona",
        "monthly_cost": 2500,
        "vat_applicable": True,
    },
    {
        "group": "facility / rent",
        "item": "Management / maintenance fee",
        "monthly_cost": 1200,
        "vat_applicable": True,
    },
    {
        "group": "utilities / production running",
        "item": "Electricity",
        "monthly_cost": 7500,
        "vat_applicable": True,
    },
    {
        "group": "utilities / production running",
        "item": "Water / sewage",
        "monthly_cost": 350,
        "vat_applicable": True,
    },
    {
        "group": "utilities / production running",
        "item": "Compressed air / gas",
        "monthly_cost": 650,
        "vat_applicable": True,
    },
    {
        "group": "equipment / machine overhead",
        "item": "Equipment depreciation",
        "monthly_cost": 5000,
        "vat_applicable": True,
    },
    {
        "group": "equipment / machine overhead",
        "item": "Machine consumables / wear",
        "monthly_cost": 4500,
        "vat_applicable": True,
    },
    {
        "group": "back office payroll",
        "item": "Accountant salary + 25%",
        "monthly_cost": 16250,
        "vat_applicable": False,
    },
    {
        "group": "back office payroll",
        "item": "Draftsman salary + 25%",
        "monthly_cost": 16250,
        "vat_applicable": False,
    },
    {
        "group": "back office payroll",
        "item": "Project manager salary + 25%",
        "monthly_cost": 16250,
        "vat_applicable": False,
    },
    {
        "group": "software / admin / shop operations",
        "item": "Software subscriptions",
        "monthly_cost": 1500,
        "vat_applicable": True,
    },
    {
        "group": "software / admin / shop operations",
        "item": "Shop supplies / cleaning",
        "monthly_cost": 1000,
        "vat_applicable": True,
    },
    {
        "group": "software / admin / shop operations",
        "item": "Waste removal",
        "monthly_cost": 700,
        "vat_applicable": True,
    },
    {
        "group": "software / admin / shop operations",
        "item": "Insurance / safety / fire",
        "monthly_cost": 1200,
        "vat_applicable": True,
    },
    {
        "group": "software / admin / shop operations",
        "item": "Internal handling / forklift allowance",
        "monthly_cost": 800,
        "vat_applicable": True,
    },
]