import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Shopping Cart Analysis", layout="wide")

st.title("🛒 Online Shopping Cart Analysis Dashboard")

# Sidebar for file upload
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your dataset (CSV)", type="csv")

if uploaded_file:
    # Load dataset
    df = pd.read_csv(uploaded_file)

    # Sidebar filters
    st.sidebar.subheader("Filters")
    category_options = df['category'].unique()
    selected_category = st.sidebar.selectbox("Select Category", category_options)

    device_options = df['device'].unique()
    selected_device = st.sidebar.selectbox("Select Device", device_options)

    # Apply filters
    filtered_df = df[(df['category'] == selected_category) & (df['device'] == selected_device)]

    # Calculate metrics
    total_carts = len(filtered_df)
    abandoned_carts = len(filtered_df[filtered_df['status'] == 'abandoned'])
    completed_carts = len(filtered_df[filtered_df['status'] == 'completed'])
    abandonment_rate = (abandoned_carts / total_carts * 100) if total_carts > 0 else 0
    avg_cart_value = filtered_df['cart_value'].mean() if total_carts > 0 else 0

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Carts", total_carts)
    col2.metric("Abandoned Carts", abandoned_carts)
    col3.metric("Completed Carts", completed_carts)
    col4.metric("Abandonment Rate (%)", f"{abandonment_rate:.2f}")

    # Tabs
    tab1, tab2, tab3 = st.tabs(["📊 Dataset Overview", "📈 Visualizations", "🔍 Insights"])

    with tab1:
        st.subheader("Filtered Dataset Preview")
        st.write(filtered_df.head())
        st.write("Summary Statistics")
        st.write(filtered_df.describe())

    with tab2:
        st.subheader("Abandonment by Category")
        fig1 = px.histogram(filtered_df, x="category", color="status", barmode="group")
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("Cart Value Comparison")
        fig2 = px.box(filtered_df, x="status", y="cart_value", color="status")
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Device-wise Abandonment")
        fig3 = px.histogram(filtered_df, x="device", color="status", barmode="group")
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        st.subheader("Key Insights")
        st.write(f"- Abandonment Rate: **{abandonment_rate:.2f}%**")
        st.write(f"- Average Cart Value: **₹{avg_cart_value:.2f}**")
        if abandonment_rate > 50:
            st.write("- 🚨 High abandonment detected — consider improving checkout flow.")
        else:
            st.write("- ✅ Healthy completion rate observed.")
        st.write("- Device and category trends visible in charts above.")

else:
    st.info("Please upload a dataset to begin analysis.")
