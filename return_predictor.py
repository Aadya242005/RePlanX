import streamlit as st
import random
import datetime

# Configure Streamlit page
st.set_page_config(page_title="RePlanAI", page_icon="📦", layout="centered")

st.title("📦 RePlanAI – Return Risk & Contingency Executor")
st.caption("Built for Market – Theme: Transforming Retail Supply Chain")

# --- INPUT SECTION ---
st.header("📝 Enter Order Details")

with st.form("order_form"):
    sku = st.selectbox("Select Product SKU", ["TS-RED-M", "IP15-BLK-128GB", "KC-250G-CHOC"])
    region = st.selectbox("Delivery Region", ["Chennai", "Delhi", "Mumbai", "Bangalore"])
    vendor = st.text_input("Vendor Name", "Mohan Textiles")
    delivery_eta = st.slider("Delivery ETA (in days)", 1, 10, 4)
    complaints = st.multiselect(
        "Customer Complaints (if any)",
        ["wrong size", "bad stitching", "delayed delivery", "packaging issue", "damaged item"]
    )
    submitted = st.form_submit_button("🔍 Predict Return Risk")

# --- RETURN RISK SECTION ---
if submitted:
    st.divider()
    st.subheader("📦 Order Summary")

    order_data = {
        "SKU": sku,
        "Region": region,
        "Vendor": vendor,
        "ETA": f"{delivery_eta} days",
        "Complaints": complaints
    }

    st.json(order_data)

    # Simulate ML prediction
    risk_score = round(random.uniform(0.6, 0.95), 2)
    st.metric("Predicted Return Risk", f"{risk_score}")

    # --- AUTOMATED ACTION EXECUTION ---
    if risk_score >= 0.80:
        st.error("⚠️ High return risk detected! Initiating Preventive Actions...")

        with st.spinner("RePlanAI is taking intelligent actions..."):
            st.subheader("✅ Actions Executed Automatically")

            st.markdown("🛑 **Inventory Controls:**")
            st.markdown(f"- 📦 Held 100 units of `{sku}` at `{region}` warehouse for urgent QC.")
            st.markdown(f"- 🏷️ Tagged product batch for manual inspection before dispatch.")

            st.markdown("📩 **Vendor Coordination:**")
            st.markdown(f"- ✉️ Emailed vendor **{vendor}** requesting QC report within 24 hours.")
            st.markdown(f"- ⚠️ Flagged vendor on portal dashboard for compliance watch.")

            st.markdown("📢 **Customer Engagement:**")
            st.markdown(f"- 📬 Sent sizing guide + return reduction tips to all buyers in `{region}`.")
            st.markdown(f"- 🎁 Offered ₹100 cashback for opting for exchange instead of return.")

            st.markdown("🚚 **Logistics & Flow Adjustments:**")
            st.markdown(f"- ⛔ Paused auto-reorder of SKU `{sku}` for 3 days.")
            st.markdown(f"- 🔄 Rerouted future deliveries via verified partners only.")

            st.markdown("📊 **AI Summary of Action:**")
            summary = f"""
🔎 On detecting a {int(risk_score*100)}% return probability for `{sku}` in `{region}`, RePlanAI automatically initiated a 360° mitigation protocol across inventory, vendor, customer, and logistics layers.
            """
            st.info(summary)

            # Optional timestamp
            st.caption(f"🕓 Actions triggered at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            st.success("🟢 All actions executed. Ops & CRM teams notified.")

    else:
        st.success("✅ Low return risk. No action needed.")

# --- FOOTER ---
st.divider()
st.caption("🔬 Powered by ML + LLM Simulation | Team Neuronauts")
