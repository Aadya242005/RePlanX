# retailer_bot_logic.py

def get_retailer_response(sku: str, risk_score: float, location: str = "unspecified") -> str:
    msg = f"📦 SKU: {sku}\n📍 Location: {location}\n📊 Predicted Return Risk: {risk_score*100:.1f}%\n\n"

    if risk_score > 0.9:
        msg += (
            "🔴 Very High Risk Detected\n"
            "• 🚫 Hold further dispatch\n"
            "• 🧪 Alert supplier for full QA\n"
            "• 📲 Send customer sizing/usage help\n"
            "• 👁️‍🗨️ Reduce app visibility in region\n"
            "• 📤 Push Notification sent via WhatsApp\n"
        )
    elif risk_score > 0.7:
        msg += (
            "🟠 High Risk Detected\n"
            "• 🔍 Inspect 50% warehouse stock\n"
            "• 📞 Inform supplier for batch recheck\n"
            "• 📩 Customer: proactive message dispatched\n"
        )
    elif risk_score > 0.5:
        msg += (
            "🟡 Medium Risk\n"
            "• 📊 Monitor returns trend\n"
            "• 🔎 Optional quality inspection suggested\n"
        )
    else:
        msg += "🟢 Low Risk. Safe to dispatch ✅"

    return msg
