import xgboost as xgb
import pandas as pd

# --- Load your trained return risk model ---
model = xgb.XGBClassifier()
model.load_model("return_risk_model.json")  # Ensure this file is in your project root

# --- Define the expected features for the model ---
model_features = ['order_amount', 'past_returns', 'complaint_count', 'days_since_last_order']

# --- Predict return risk based on input order data ---
def predict_return_risk(order_data: dict) -> float:
    """
    Predicts return risk probability for a given order.
    
    Args:
        order_data (dict): Dictionary with keys matching model_features.
    
    Returns:
        float: Risk score between 0 and 1 (rounded to 2 decimal places).
    """
    try:
        df = pd.DataFrame([order_data])[model_features]
        risk_score = model.predict_proba(df)[0][1]
        return round(risk_score, 2)
    except Exception as e:
        print("❌ Error in predicting risk:", str(e))
        return 0.0


if __name__ == "__main__":
    test_samples = [
        # ✅ Low Risk Samples
        {
            "label": "Low Risk 1",
            "data": {
                'order_amount': 6500,
                'past_returns': 0,
                'complaint_count': 0,
                'days_since_last_order': 40
            }
        },
        {
            "label": "Low Risk 2",
            "data": {
                'order_amount': 200,
                'past_returns': 1,
                'complaint_count': 0,
                'days_since_last_order': 60
            }
        },
        {
            "label": "Low Risk 3",
            "data": {
                'order_amount': 3200,
                'past_returns': 0,
                'complaint_count': 1,
                'days_since_last_order': 35
            }
        },

        # 🔴 High Risk Samples
        {
            "label": "High Risk 1",
            "data": {
                'order_amount': 499,
                'past_returns': 6,
                'complaint_count': 4,
                'days_since_last_order': 1
            }
        },
        {
            "label": "High Risk 2",
            "data": {
                'order_amount': 700,
                'past_returns': 5,
                'complaint_count': 3,
                'days_since_last_order': 2
            }
        },
        {
            "label": "High Risk 3",
            "data": {
                'order_amount': 899,
                'past_returns': 7,
                'complaint_count': 5,
                'days_since_last_order': 3
            }
        }
    ]

    for sample in test_samples:
        score = predict_return_risk(sample["data"])
        print(f"📦 {sample['label']} – Risk Score: {score}")
        print("Probabilities:", model.predict_proba(df))

