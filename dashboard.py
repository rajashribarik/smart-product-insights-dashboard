import streamlit as st
import pandas as pd
import plotly.express as px

# Absolute path to your CSV file
CSV_PATH = r"C:\Users\Gayatri\OneDrive\Desktop\smart-product-insights\backend\data\processed_reviews.csv"

# Load data with caching
@st.cache_data
def load_data():
    try:
        return pd.read_csv(CSV_PATH)
    except FileNotFoundError:
        st.error(f"❌ File not found: {CSV_PATH}")
        return pd.DataFrame()  # Return empty DataFrame on failure

# Main Streamlit App
def main():
    st.set_page_config(page_title="Smart Product Insights Dashboard", layout="wide")
    st.title("📊 Smart Product Insights Dashboard")

    df = load_data()

    if df.empty:
        st.warning("⚠️ No data loaded. Please check your file path or file content.")
        return

    # Display data
    st.subheader("🧾 Dataset Preview")
    st.dataframe(df.head())

    # Show product ratings distribution
    if 'rating' in df.columns:
        st.subheader("⭐ Rating Distribution")
        fig_rating = px.histogram(df, x="rating", nbins=10, title="Rating Distribution")
        st.plotly_chart(fig_rating, use_container_width=True)

    # Show sentiment analysis result (if column exists)
    if 'sentiment' in df.columns:
        st.subheader("🗣️ Sentiment Overview")
        fig_sentiment = px.histogram(df, x="sentiment", title="Sentiment Distribution")
        st.plotly_chart(fig_sentiment, use_container_width=True)

    # Filter by product
    if 'product_name' in df.columns:
        product_names = df['product_name'].dropna().unique().tolist()
        selected_product = st.selectbox("📦 Select Product", product_names)

        filtered_df = df[df['product_name'] == selected_product]
        st.write(f"Showing data for **{selected_product}**")
        st.dataframe(filtered_df)

        if 'rating' in filtered_df.columns:
            avg_rating = filtered_df['rating'].mean()
            st.metric("📈 Average Rating", f"{avg_rating:.2f}")

        if 'sentiment' in filtered_df.columns:
            st.bar_chart(filtered_df['sentiment'].value_counts())

if __name__ == "__main__":
    main()
