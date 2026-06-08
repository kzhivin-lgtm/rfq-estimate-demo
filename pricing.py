import streamlit as st


VAT_RATE = 0.18


def format_money(value):
    if value is None:
        return "—"

    formatted = f"{int(value):,}".replace(",", "\u00A0")
    return f"₪{formatted}"


def parse_money_input(value, fallback=0):
    if value is None:
        return fallback

    digits = "".join(ch for ch in str(value) if ch.isdigit())

    if not digits:
        return fallback

    return int(digits)


def normalize_money_state(key, fallback=0):
    value = parse_money_input(st.session_state.get(key), fallback=fallback)
    st.session_state[key] = format_money(value)


def vat_summary(subtotal, vat_rate=VAT_RATE):
    subtotal = round(subtotal)
    vat = round(subtotal * vat_rate)
    total = subtotal + vat

    return subtotal, vat, total