# RFQ-to-Estimate Copilot Demo

Interactive Streamlit demo for RFQ-to-estimate workflow.

Update contents:

- app.py: Generate proposal now builds the PDF from current session_state totals instead of serving a stale static PDF first.
- styles.py: included unchanged from the design-system update for convenience.
- assets/RA-N01_commercial_proposal.pdf: redesigned static fallback proposal, recalculated to Price Total ₪144 195.
- requirements_addition.txt: add reportlab to requirements.txt if it is not already present.

Calculation used in the fallback PDF:
Kitchen 38 902
Kitchen island 43 372
Wall shelf 25 875
Delivery 3 244
Installation 10 806
Price 122 199
VAT 18% 21 996
Price Total 144 195
