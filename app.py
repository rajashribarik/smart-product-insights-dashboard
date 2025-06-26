from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os
from db_config import SessionLocal, init_db
from models import ProductReview
from sentiment import analyze_sentiment

app = Flask(__name__)
CORS(app)

init_db()

@app.route('/process', methods=['GET'])
def process_reviews():
    session = SessionLocal()

    # ✅ Use your actual dataset path
    df = pd.read_csv("C:/Users/Gayatri/Downloads/sales_reviews.csv")

    # Perform sentiment analysis
    df['sentiment'], df['polarity'] = zip(*df['review'].map(analyze_sentiment))

    # Store each row in the database
    for _, row in df.iterrows():
        entry = ProductReview(
            product_id=row['product_id'],
            product_name=row['product_name'],
            review=row['review'],
            sentiment=row['sentiment'],
            polarity=row['polarity'],
            sales=row['sales'],
            region=row['region']
        )
        session.add(entry)

    session.commit()
    session.close()

    # Save the processed DataFrame to a CSV file
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/processed_reviews.csv", index=False)

    return jsonify({"status": "success", "message": "Data saved to data/processed_reviews.csv"})

@app.route('/reviews', methods=['GET'])
def get_reviews():
    session = SessionLocal()
    results = session.query(ProductReview).all()
    data = [{
        "product_name": r.product_name,
        "review": r.review,
        "sentiment": r.sentiment,
        "sales": r.sales,
        "region": r.region
    } for r in results]
    session.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
