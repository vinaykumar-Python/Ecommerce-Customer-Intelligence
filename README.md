\# E-Commerce Customer \& Sales Intelligence Platform



An end-to-end data analytics project that transforms Brazilian e-commerce transaction data into actionable business insights using Python, SQL, SQLite, Excel and Power BI.



The project explores sales performance, customer purchasing behaviour, customer segmentation, cohort retention, product performance, delivery efficiency and customer satisfaction.



\## Project Overview



This project demonstrates a complete data analytics workflow, from raw data processing and exploratory analysis to advanced SQL reporting and interactive Power BI dashboards.



\### Key Business Areas



\- Executive Sales Overview

\- Customer Intelligence \& Retention

\- Operations \& Customer Experience



\## Technology Stack



| Technology | Purpose |

|---|---|

| Python | Data cleaning, transformation and analysis |

| Pandas \& NumPy | Data manipulation |

| Matplotlib | Exploratory data visualization |

| SQL | Business analysis and advanced queries |

| SQLite | Relational database |

| Power BI | Interactive dashboards |

| Excel | Data inspection and reporting |

| Git \& GitHub | Version control |



\## Project Structure



```text

Ecommerce-Customer-Intelligence/

â”‚

â”œâ”€â”€ data/

â”‚   â”œâ”€â”€ raw/

â”‚   â””â”€â”€ processed/

â”‚

â”œâ”€â”€ database/

â”‚   â””â”€â”€ ecommerce.db

â”‚

â”œâ”€â”€ notebooks/

â”‚

â”œâ”€â”€ powerbi/

â”‚   â””â”€â”€ dashboards/

â”‚       â”œâ”€â”€ Ecommerce\_Executive\_Sales\_Overview.pbix

â”‚       â”œâ”€â”€ Customer\_Intelligence.pbix

â”‚       â””â”€â”€ Operations \& Customer Experience.pbix

â”‚

â”œâ”€â”€ reports/

â”‚   â”œâ”€â”€ customer\_rfm.csv

â”‚   â”œâ”€â”€ customer\_rfm\_segmented.csv

â”‚   â”œâ”€â”€ cohort\_retention\_matrix.csv

â”‚   â”œâ”€â”€ monthly\_sales\_performance.csv

â”‚   â”œâ”€â”€ product\_category\_performance.csv

â”‚   â”œâ”€â”€ delivery\_performance.csv

â”‚   â””â”€â”€ seller\_performance.csv

â”‚

â”œâ”€â”€ screenshots/

â”‚   â”œâ”€â”€ executive\_sales\_overview.png

â”‚   â”œâ”€â”€ customer\_intelligence.png

â”‚   â””â”€â”€ operations\_customer\_experience.png

â”‚

â”œâ”€â”€ sql/

â”œâ”€â”€ src/

â”œâ”€â”€ requirements.txt

â”œâ”€â”€ .gitignore

â””â”€â”€ README.md

```



\## Power BI Dashboard Previews



\### 1. Executive Sales Overview



Provides an overview of sales performance, revenue trends, product categories, payment methods and geographical performance.



!\[Executive Sales Overview](screenshots/executive\_sales\_overview.png)



Dashboard file: `Ecommerce\_Executive\_Sales\_Overview.pbix`



\### 2. Customer Intelligence \& Retention



Analyses customer purchasing behaviour, RFM segmentation, repeat purchases, customer value and cohort retention.



!\[Customer Intelligence](screenshots/customer\_intelligence.png)



Dashboard file: `Customer\_Intelligence.pbix`



\### 3. Operations \& Customer Experience



Evaluates delivery performance, late deliveries, customer review scores and unsuccessful orders across geographical regions.



!\[Operations \& Customer Experience](screenshots/operations\_customer\_experience.png)



Dashboard file: `Operations \& Customer Experience.pbix`



\## Analytical Work



\### Python Analysis



\- Data cleaning and preprocessing

\- Missing-value analysis

\- Exploratory data analysis

\- Customer purchase behaviour

\- RFM customer segmentation

\- Cohort retention analysis

\- Product-level performance

\- Seller performance

\- Delivery and customer review analysis



\### SQL Analysis



\- Sales performance analysis

\- Monthly revenue trends

\- Customer purchase behaviour

\- Product and category performance

\- Customer ranking and segmentation

\- Window functions

\- Running totals and ranking

\- Business performance comparisons



\### Business Intelligence



Three Power BI dashboards provide interactive views of sales, customers and operational performance.



\## Key Business Insights



The analysis focuses on identifying:



1\. Best-performing products and product categories.

2\. Revenue contribution across geographical regions.

3\. Customer segments with different purchasing behaviours.

4\. Repeat customer patterns and retention challenges.

5\. Delivery delays and their relationship with customer satisfaction.

6\. States with higher unsuccessful order rates.

7\. Opportunities to improve customer experience and business performance.



\## Dataset



\*\*Source:\*\* Brazilian E-Commerce Public Dataset by Olist.



The dataset contains historical Brazilian marketplace transactions and related information, including orders, customers, products, sellers, payments, reviews and deliveries.



The analysis covers historical data from 2016â€“2018.



\## Installation \& Execution



Clone the repository:



```bash

git clone https://github.com/YOUR\_USERNAME/Ecommerce-Customer-Intelligence.git

cd Ecommerce-Customer-Intelligence

```



Create a virtual environment:



```bash

python -m venv .venv

```



Activate it on Windows:



```powershell

.venv\\Scripts\\Activate.ps1

```



Install dependencies:



```bash

pip install -r requirements.txt

```



Run the analysis scripts from the project root using their respective filenames.



Open the `.pbix` files in Power BI Desktop to explore the dashboards.



\## Skills Demonstrated



\- Data Analytics

\- Data Cleaning and Transformation

\- Exploratory Data Analysis

\- Python Programming

\- Advanced SQL

\- Relational Database Management

\- Customer Segmentation

\- Business Intelligence

\- Data Visualization

\- Business Reporting



\## Project Status



Core Python analysis, SQL analysis, database preparation and three Power BI dashboards have been developed. Documentation and GitHub publication are being finalized.



\---



\*\*Note:\*\* This is an independent analytical project using historical marketplace data. Findings describe the dataset and should not be interpreted as current marketplace performance.



