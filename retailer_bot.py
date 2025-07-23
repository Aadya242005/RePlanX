from flask import Flask, render_template, request, jsonify
from predict_risk import predict_return_risk
from retailer_bot_logic import get_retailer_response  # Now safe
from send_whatsapp import send_whatsapp_message  # Add this import


app = Flask(__name__)
# Track state — simple simulation for a single session
user_state = {"expecting_number": False}


def get_bot_response(user_input):
    user_input = user_input.strip().lower()
    # Step 1: WhatsApp trigger
        # Handle WhatsApp trigger
    if "whatsapp" in user_input:
        user_state["expecting_number"] = True
        return "📲 Sure! Please enter your WhatsApp number starting with +91..."

    # Handle number entry
    if user_state.get("expecting_number", False):
        if user_input.startswith("+91") and len(user_input) == 13:
            user_state["expecting_number"] = False
            try:
                send_whatsapp_message(user_input, "✅ Your order is being processed! You'll receive updates here.")
                return "✅ WhatsApp update has been sent to your number!"
            except Exception as e:
                return f"❌ Could not send WhatsApp message. Error: {str(e)}"
        else:
            return "⚠️ Please enter a valid WhatsApp number starting with +91."



    if any(greet in user_input for greet in ["hello", "hi", "hey", "hii", "hola"]):
        return (
            "👋 Hello! I'm your order assistant bot.\n\n"
            "You can ask me about:\n"
            "• 📦 Order status\n"
            "• 🚚 Delivery time\n"
            "• 🔄 Returns, exchanges or refunds\n"
            "• 📬 COD, shipping fees, out-of-stock alerts\n"
            "Just type your question!"
        )
    elif "where is my parcel" in user_input:
        return "📦 Your parcel is currently in transit and is at the Delhi distribution center. Estimated delivery: 14th July."
    elif "when will" in user_input and "deliver" in user_input:
        return "🚚 Your order will be delivered within 2–3 business days."
    elif "cancel" in user_input:
        return "🛑 You can cancel your order from 'My Orders' before it gets shipped. Need help cancelling?"
    elif "returnable" in user_input or "return" in user_input:
        return "✅ Yes, this item is returnable within 7 days of delivery if unused and in original condition."
    elif "exchange" in user_input:
        return "🔄 Yes! You can exchange your item within 7 days. Just initiate it from the 'My Orders' section."
    elif "cash on delivery" in user_input or "cod" in user_input:
        return "💵 Yes, Cash on Delivery is available for orders under ₹5,000."
    elif "delivery charge" in user_input or "shipping cost" in user_input:
        return "🚚 Shipping is free for orders above ₹999. For others, ₹49 applies."
    elif "refund" in user_input:
        return "💰 Refunds are processed in 5–7 business days after item pickup and quality check."
    elif "change address" in user_input or "edit order" in user_input:
        return "🏠 You can change your delivery address within 30 minutes of placing the order."
    elif "out of stock" in user_input or "restock" in user_input:
        return "🔁 This item is expected to be restocked by 18th July. You can click ‘Notify Me’ to get an alert."
    elif "under review" in user_input or "return risk" in user_input:
        return (
            "📊 Based on past returns and complaints, this product shows higher return probability. "
            "We’re doing a quality recheck before dispatch to avoid issues. Thank you for your patience!"
        )
    elif "talk to human" in user_input or "real person" in user_input:
        return "🙋 Sure! I’ve raised a ticket. Our support team will reach out to you within 24 hours."
    elif "how do you know" in user_input or "predict return" in user_input:
        return (
            "🤖 Our AI analyzes your past returns, product type, delivery location, and more "
            "to predict if you might face issues. This helps us act early to ensure a smooth experience."
        )
    else:
        return (
            "❓ I'm not sure how to help with that. Try asking about:\n"
            "• Order delivery\n"
            "• Returns / exchanges\n"
            "• COD / charges\n"
            "Or type 'hi' to see more options!"
        )


# Your existing get_bot_response() function here

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def get_bot_reply():
    data = request.get_json()
    user_msg = data.get("message", "")
    response = get_bot_response(user_msg)
    return jsonify({"reply": response})

@app.route("/chat-retailer", methods=["POST"])
def retailer_chat():
    data = request.json
    sku = data.get("sku", "UNKNOWN")
    location = data.get("location", "UNKNOWN")
    order_data = data.get("order_data")

    risk_score = predict_return_risk(order_data)
    reply = get_retailer_response(sku, risk_score, location)

    return jsonify({"risk_score": risk_score, "reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
    result = send_whatsapp_message("whatsapp:+918755093039", "Hi! Your order is being processed.")
    print(result)

