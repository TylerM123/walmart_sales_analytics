import dash
from dash import dcc, html, callback
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from datetime import date
import plotly.graph_objs as go


# Replace with the correct path to your dataset
walmart_sales_df = pd.read_csv('/Users/tylermcgirt/Documents/Data Projects/walmart_sales_analytics/data/raw/WalmartSQL repository.csv')

walmart_sales_df['dtme'] = pd.to_datetime(walmart_sales_df['dtme'])  # convert 'dtme' column to datetime



# a) Cities with the highest sales (Top 10)
top_cities = walmart_sales_df.groupby('city')['total'].sum().nlargest(10)

# b) Top 5 products bought by male members
male_top_products = walmart_sales_df[(walmart_sales_df['gender'] == 'Male') & (walmart_sales_df['customer_type'] == 'Member')].groupby('product_line')['quantity'].sum().nlargest(5)

# c) Top 5 products bought by female members
female_top_products = walmart_sales_df[(walmart_sales_df['gender'] == 'Female') & (walmart_sales_df['customer_type'] == 'Member')].groupby('product_line')['quantity'].sum().nlargest(5)

# d) Most popular time of day to buy a product
popular_time_of_day = walmart_sales_df['time_of_day'].value_counts().idxmax()

# e) Number of orders change over time for each city
orders_over_time = walmart_sales_df.groupby(['city', pd.Grouper(key='dtme', freq='ME')])['invoice_id'].count().unstack(0)

# f) Top products sold on a given date (Example: 2019-01-05)
given_date = '2019-01-05'
top_products_on_date = walmart_sales_df[walmart_sales_df['dtme'] == given_date].groupby('product_line')['quantity'].sum().nlargest(1)

# Calculate the 80th percentile of the total purchase values
top_20_percent_cutoff = walmart_sales_df['total'].quantile(0.80)

# Filter the dataset to include only the top 20% of purchases
top_20_percent_df = walmart_sales_df[walmart_sales_df['total'] >= top_20_percent_cutoff]


#initialize dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# dash figures

# Now create the scatter plot for the filtered data
fig_a = px.scatter(top_20_percent_df, x='dtme', y='total',
                 title='Top 20% of Purchases by Date',
                 labels={'total': 'Total Purchase Value', 'dtme': 'Date'},
                 color='time_of_day',  # This will color-code the points by the time of day
                 hover_data=['invoice_id'])  # Shows invoice ID on hover

fig_a.update_layout(
    plot_bgcolor='#333',
    paper_bgcolor='#333',
    font_color='#fff',
    autosize=True,
    xaxis_title='Date',
    yaxis_title='Total Purchase Value',
    xaxis=dict(
        tickformat="%Y-%m-%d",
        type='category'  # This forces the x-axis to be treated as categorical, which may be necessary if not all dates are represented
    )
)


# fig_b
fig_b = px.bar(male_top_products.reset_index(), x='product_line', y='quantity',
               title='Top 5 Product Categories Bought by Male Members',
               labels={'quantity': 'Quantity Sold', 'product_line': 'Product Line'})
fig_b.update_layout(
    {
    'plot_bgcolor': '#333',
    'paper_bgcolor': '#333',
    'font': {
        'color': '#fff'
    },
},
autosize = True
)

# fig_c
fig_c = px.bar(female_top_products.reset_index(), x='product_line', y='quantity',
               title='Top 5 Product Categories Bought by Female Members',
               labels={'quantity': 'Quantity Sold', 'product_line': 'Product Line'})
fig_c.update_layout(
    {
    'plot_bgcolor': '#333',
    'paper_bgcolor': '#333',
    'font': {
        'color': '#fff'
    },
},
autosize = True
)

# fig_d
time_of_day_counts = walmart_sales_df['time_of_day'].value_counts()
fig_d = px.bar(time_of_day_counts, x=time_of_day_counts.index, y=time_of_day_counts.values,
               title='Popularity of Purchase Times',
               labels={'y': 'Number of Purchases', 'index': 'Time of Day'})
fig_d.update_layout(
    {
    'plot_bgcolor': '#333',
    'paper_bgcolor': '#333',
    'font': {
        'color': '#fff'
    },
},
autosize = True
)

# fig_e


# sidebar definition
sidebar = html.Div(
    [
        html.H2("Sidebar"),
        html.Hr(),
        html.P("A simple sidebar layout with navigation links"),
        html.Div([
            html.A("Home", href="/", className="sidebar-link"),
            html.A("Page 1", href="/page-1", className="sidebar-link"),
            html.A("Page 2", href="/page-2", className="sidebar-link"),
            # More links can be added here
        ], className='sidebar-link-wrapper'),
        html.Div(
            [
                dcc.DatePickerSingle(
                    id='date-picker',
                    min_date_allowed=walmart_sales_df['dtme'].min().date(),
                    max_date_allowed=walmart_sales_df['dtme'].max().date(),
                    initial_visible_month=walmart_sales_df['dtme'].min().date(),
                    date=str(walmart_sales_df['dtme'].min().date())
                )
            ],
            className='datepicker'
        ),
    ],
    className='sidebar_style',
)

content_page_1 = html.Div(
    [   html.Div(
            [
                html.H1('Consumer Trends'),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(figure = fig_a, className='dash-graph')
                                    ]
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(figure = fig_b, className='dash-graph')
                                    ]
                                )
                            ],className= 'grid-container'
                        ),
                        html.Br(),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Graph(figure = fig_c, className='dash-graph')
                                    ]
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(figure = fig_d, className='dash-graph')
                                    ]
                                )
                            ],className= 'grid-container'
                        ),
                    ],
                    className='container'
                ),
            ],
            className="content-wrapper"
        ) 
    ],
    id="content_page_1", 
    className='content_style_page_one'
)

content_page_2 = html.Div(
    [
        html.Div(
            [

            ],
            id='Page 2', 
            className='content-wrapper'
        )
    ],
    id='content_page_2',
    className="content_style_page_two"
)

content_page_3 = html.Div(
    [
        html.H1('Page 2')
    ],
    id='content_page_3',
    className="content_style_page_three"
)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content_page_1 or content_page_2 or content_page_3
])

@app.callback(Output(content_page_1 or content_page_2 or content_page_3, "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return content_page_1
    elif pathname == "/page-2":
        return content_page_2
    elif pathname == "/page-3":
        return content_page_3
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", style={"color": "red"}),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised...")
        ]
    )

# Callbacks for updating graphs
@app.callback(
    Output('top-cities-sales', 'figure'),
    Output('top-male-products', 'figure'),
    Output('top-female-products', 'figure'),
    Output('popular-time-of-day', 'children'),
    Output('orders-over-time', 'figure'),
    Output('top-products-on-date', 'figure'),
    Input('date-picker', 'date')
)

def update_metrics(selected_date):
    # Perform the analyses here based on the selected_date for the last metric
    # For simplicity, the detailed data processing is omitted

    # Example visualizations
    fig_cities = px.bar(walmart_sales_df, x='city', y='total')  # Update with your actual analysis
    fig_male_products = px.bar(walmart_sales_df, x='product_line', y='quantity')  # Update accordingly
    fig_female_products = px.bar(walmart_sales_df, x='product_line', y='quantity')  # Update accordingly
    popular_time = f"Most Popular Time of Day: {'Your Time Here'}"  # Update accordingly
    fig_orders_over_time = px.line(walmart_sales_df, x='dtme', y='total')  # Update with actual analysis
    fig_top_products_on_date = px.bar(walmart_sales_df[walmart_sales_df['dtme'] == pd.to_datetime(selected_date)], x='product_line', y='quantity')  # Update accordingly

    return fig_cities, fig_male_products, fig_female_products, popular_time, fig_orders_over_time, fig_top_products_on_date


if __name__ == "__main__":
    app.run_server(debug=True)
