# Data Cleaning Scripts
import pandas as pd 

walmart_sales_df = pd.read_csv('/Users/tylermcgirt/Documents/Data Projects/walmart_sales_analytics/data/raw/WalmartSQL repository.csv', delimiter=',', parse_dates=['dtme'])


#walmart_sales_df['dtme'] = pd.to_datetime(walmart_sales_df['dtme'])

walmart_sales_df['day'] = walmart_sales_df['dtme'].dt.day
walmart_sales_df['month'] = walmart_sales_df['dtme'].dt.month
walmart_sales_df['year'] = walmart_sales_df['dtme'].dt.year

walmart_sales_df[['date', 'time']] = walmart_sales_df['dtme'].str.split('T', expand=True)

walmart_sales_df.to_csv('/Users/tylermcgirt/Documents/Data Projects/walmart_sales_analytics/data/processed/processed_walmart_sales_data.csv')

print(walmart_sales_df.head(10))