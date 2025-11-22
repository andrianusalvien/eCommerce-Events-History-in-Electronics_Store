# 📊 **E‑Commerce Event History Dashboard** 

Welcome to the **E‑Commerce Event History Dashboard**! This interactive dashboard is designed to help you analyze and visualize e-commerce event data (such as views, cart additions, and purchases). Built with **Streamlit** and **Plotly**, it offers a user-friendly interface to explore various e-commerce KPIs, customer behaviors, and trends.

🔍 **Explore your e-commerce data interactively with filters, charts, and more!**

## 🌟 Features
- **Interactive Filters**: Filter the data by year, month, day, and event type (view, cart, purchase).
- **Customer Activity Over Time**: Visualize the number of unique customers over time.
- **Event Distribution**: Explore the distribution of events (views, cart additions, purchases) across brands, categories, and time.
- **Top Brands**: Get insights into the top 10 brands by event count and purchase actions.
- **Time-based Visualizations**: Analyze customer behavior based on hour of the day, day of the week, and monthly trends.

## 🚀 Live Demo

You can view and interact with the live dashboard here:  
[**E-Commerce Event History Dashboard**](https://ecommerce-event-history.streamlit.app/)

## 🔧 Installation

### Requirements
- **Python 3.x**
- **Streamlit**
- **Plotly**
- **Pandas**
- **Kagglehub** (for loading the dataset)

### To run the app locally:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ecommerce-event-history-dashboard.git
    cd ecommerce-event-history-dashboard
    ```

2. **Set up a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - **Windows**:
      ```bash
      .\venv\Scripts\activate
      ```
    - **MacOS/Linux**:
      ```bash
      source venv/bin/activate
      ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the Streamlit app**:
    ```bash
    streamlit run streamlit_app.py
    ```

This will launch the app in your default web browser.

## 📊 Visualizations

### **1. Event Distribution by Brand**
Explore how events are distributed across different brands, including the **Top 10 Brands** with the most interactions (views, cart additions, purchases).

### **2. Brand Purchase Analysis**
Understand the **Top 10 Brands** based on the number of **purchases**. This gives insights into which brands are performing best in terms of conversions.

### **3. Time-based Trends**
- **Event per Hour**: Visualize how events are distributed throughout the day (from **00:00** to **23:00**).
- **Event per Day of the Week**: Check the weekly trend of events.
- **Event per Month**: Understand monthly trends of events, with year and month displayed for better clarity.

### **4. Customer Activity Over Time**
See how the number of **unique customers** evolves over time by month. This helps track customer engagement across different periods.

## 📂 Project Structure

