# Brazilian E-Commerce Data Analysis - Olist Store

## About Project
This project is a final assignment from the **"Belajar Analisis Data dengan Python"** course by Dicoding X DBS. The main goal of this project is to perform a complete data analysis workflow, starting from Data Wrangling, Exploratory Data Analysis (EDA), to Explanatory Analysis, which is presented through an interactive dashboard.

## About Dataset
Dataset yang digunakan adalah **Brazilian E-Commerce Public Dataset by Olist**.
Dataset ini berisi informasi riil dari 100.000 pesanan yang terjadi di **Olist Store** (marketplace terbesar di Brasil) antara tahun 2016 hingga 2018.

## Business Questions
This analysis focuses on answering the following key business questions:

1. How has the company's total order and revenue performed in recent months (2017-2018)?
2. How does performance compare across product categories in terms of order volume and total revenue generated between 2016 and 2018?
3. What is the geographic distribution of customers and their contribution to total spending across various Brazilian states between 2016 and 2018?

## Setup Environment - Shell/Terminal
To run the dashboard locally, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/akmalhen/brazilian-ecommerce-analysis.git
cd brazilian-ecommerce-analysis
```
### 2. Create a Virtual Environment
It is recommended to use an isolated environment to avoid dependency conflicts:
```bash
# For Mac/Linux
python3 -m venv dicoding
source dicoding/bin/activate

# For Windows
python -m venv dicoding
dicoding\Scripts\activate
```

### 3. Install Dependencies
Install all required libraries using pip:
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard
```bash
streamlit run dashboard/dashboard.py
```

## Directory Structure
```text
.
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── olist_customers_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── ...
├── notebook.ipynb
├── README.md
├── requirements.txt
├── url.txt
└── .gitignore
```

## Technologies Used
- **Python** (Pandas, Numpy, Matplotlib, Seaborn)
- **GeoPandas** (Advanced Geospatial Analysis)
- **Streamlit** (Interactive Dashboard)
- **Babel** (Currency Formatting)

## Author
- **Nama:** Akmal Hendrian Malik
- **ID Dicoding:** akmalhendrian
