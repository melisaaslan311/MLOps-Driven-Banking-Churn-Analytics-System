import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os
import sys
from typing import Optional

# Path configuration
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(root_dir)

from config.settings import MYSQL_URI


# Page configuration
st.set_page_config(
    page_title="MLOps-Driven-Banking-Churn-Analytics-System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .stMetric:hover {
        box-shadow: 0 2px 6px rgba(0,0,0,0.12);
        transition: box-shadow 0.3s ease;
    }
    .stMetric label {
        font-size: 0.9rem !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
    h1 {
        color: #1f77b4;
        font-weight: 600;
        font-size: 2rem !important;
        margin-bottom: 0.5rem !important;
    }
    h2 {
        color: #2c3e50;
        font-size: 1.3rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.8rem !important;
    }
    h3 {
        color: #2c3e50;
        font-size: 1.1rem !important;
        margin-top: 1rem !important;
    }
    .insight-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        border-radius: 6px;
        margin: 0.8rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .insight-box h4 {
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    .insight-box p {
        font-size: 0.9rem !important;
        margin: 0.3rem 0 !important;
    }
    .insight-box strong {
        color: #2c3e50;
        font-weight: 600;
    }
    hr {
        margin: 1rem 0 !important;
    }
    /* Streamlit default spacing adjustments */
    .element-container {
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_database_connection():
    """Create and cache database connection"""
    try:
        engine = create_engine(MYSQL_URI, pool_pre_ping=True)
        return engine
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return None


@st.cache_data(ttl=600)
def load_data(_engine) -> Optional[pd.DataFrame]:
    """Load customer data with caching (10 min TTL)"""
    try:
        df = pd.read_sql("SELECT * FROM customers", _engine)
        return df
    except SQLAlchemyError as e:
        st.error(f"Error loading data: {str(e)}")
        return None


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calculate key performance indicators"""
    return {
        'total_customers': len(df),
        'churned_customers': df['churn'].sum(),
        'churn_rate': df['churn'].mean() * 100,
        'active_customers': len(df) - df['churn'].sum(),
        'avg_credit_score': df['credit_score'].mean(),
        'avg_age': df['age'].mean() if 'age' in df.columns else None,
        'avg_balance': df['balance'].mean() if 'balance' in df.columns else None
    }


def render_kpi_cards(kpis: dict):
    """Render KPI metrics in cards"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📈 Total Customers",
            value=f"{kpis['total_customers']:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="⚠️ Churned Customers",
            value=f"{kpis['churned_customers']:,}",
            delta=f"{kpis['churn_rate']:.2f}%"
        )
    
    with col3:
        st.metric(
            label="✅ Active Customers",
            value=f"{kpis['active_customers']:,}",
            delta=f"{100 - kpis['churn_rate']:.2f}%"
        )
    
    with col4:
        st.metric(
            label="💳 Avg Credit Score",
            value=f"{kpis['avg_credit_score']:.0f}"
        )


def plot_credit_score_distribution(df: pd.DataFrame):
    """Create interactive credit score distribution chart"""
    st.subheader("📊 Credit Score Distribution")
    
    fig = px.histogram(
        df,
        x='credit_score',
        nbins=50,
        labels={'credit_score': 'Credit Score', 'count': 'Number of Customers'},
        color_discrete_sequence=['#1f77b4'],
        height=350
    )
    
    fig.update_layout(
        showlegend=False,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=11),
        margin=dict(l=40, r=40, t=20, b=40)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def plot_churn_by_geography(df: pd.DataFrame):
    """Create churn analysis by geography"""
    st.subheader("🌍 Churn Analysis by Geography")
    
    # Get geography columns (supports both 'country_' and 'geography_' prefixes)
    geo_cols = [col for col in df.columns if col.startswith('country_') or col.startswith('geography_')]
    
    if not geo_cols:
        st.warning("No geography data available")
        return
    
    # Create data for plotting
    geo_data = []
    for col in geo_cols:
        # Handle both 'country_' and 'geography_' prefixes
        if col.startswith('country_'):
            country = col.replace('country_', '')
        else:
            country = col.replace('geography_', '')
            
        total = df[col].sum()
        churned = df[df['churn'] == 1][col].sum()
        churn_rate = (churned / total * 100) if total > 0 else 0
        
        geo_data.append({
            'Country': country,
            'Total Customers': int(total),
            'Churned': int(churned),
            'Churn Rate (%)': churn_rate
        })
    
    geo_df = pd.DataFrame(geo_data)
    
    # Create grouped bar chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Active',
        x=geo_df['Country'],
        y=geo_df['Total Customers'] - geo_df['Churned'],
        marker_color='#2ecc71'
    ))
    
    fig.add_trace(go.Bar(
        name='Churned',
        x=geo_df['Country'],
        y=geo_df['Churned'],
        marker_color='#e74c3c'
    ))
    
    fig.update_layout(
        barmode='stack',
        xaxis_title='Country',
        yaxis_title='Customers',
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=11),
        height=350,
        margin=dict(l=40, r=40, t=20, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display churn rates table
    st.dataframe(
        geo_df.style.format({
            'Total Customers': '{:,.0f}',
            'Churned': '{:,.0f}',
            'Churn Rate (%)': '{:.2f}%'
        }).background_gradient(subset=['Churn Rate (%)'], cmap='Reds'),
        use_container_width=True,
        hide_index=True
    )


def plot_additional_insights(df: pd.DataFrame):
    """Create additional visualization insights"""
    col1, col2 = st.columns(2)
    
    with col1:
        if 'age' in df.columns:
            st.subheader("👥 Age Distribution")
            fig = px.box(
                df,
                x='churn',
                y='age',
                color='churn',
                labels={'churn': 'Churn Status', 'age': 'Age'},
                color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
                height=300
            )
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=11),
                margin=dict(l=40, r=40, t=20, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if 'balance' in df.columns:
            st.subheader("💰 Balance Distribution")
            fig = px.histogram(
                df,
                x='balance',
                color='churn',
                nbins=30,
                labels={'balance': 'Account Balance', 'churn': 'Churned'},
                color_discrete_map={0: '#2ecc71', 1: '#e74c3c'},
                barmode='overlay',
                height=300
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=11),
                margin=dict(l=40, r=40, t=20, b=40)
            )
            st.plotly_chart(fig, use_container_width=True)


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar filters and return filtered dataframe"""
    st.sidebar.header("🔍 Filters")
    
    # Credit score range filter
    if 'credit_score' in df.columns:
        min_score, max_score = st.sidebar.slider(
            "Credit Score Range",
            int(df['credit_score'].min()),
            int(df['credit_score'].max()),
            (int(df['credit_score'].min()), int(df['credit_score'].max()))
        )
        df = df[(df['credit_score'] >= min_score) & (df['credit_score'] <= max_score)]
    
    # Churn status filter
    churn_filter = st.sidebar.radio(
        "Customer Status",
        ["All", "Active Only", "Churned Only"],
        index=0
    )
    
    if churn_filter == "Active Only":
        df = df[df['churn'] == 0]
    elif churn_filter == "Churned Only":
        df = df[df['churn'] == 1]
    
    # Geography filter
    geo_cols = [col for col in df.columns if col.startswith('country_') or col.startswith('geography_')]
    if geo_cols:
        # Extract country names from column names
        if geo_cols[0].startswith('country_'):
            countries = [col.replace('country_', '') for col in geo_cols]
        else:
            countries = [col.replace('geography_', '') for col in geo_cols]
        
        # Create a mapping of display names to original column names
        country_to_col = {country: col for country, col in zip(countries, geo_cols)}
        
        selected_countries = st.sidebar.multiselect(
            "Select Countries",
            countries,
            default=countries
        )
        
        if selected_countries:
            # Map back to original column names
            selected_geo_cols = [country_to_col[c] for c in selected_countries]
            mask = df[selected_geo_cols].sum(axis=1) > 0
            df = df[mask]
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Filtered Records:** {len(df):,}")
    
    return df


def main():
    """Main application function"""
    # Header
    st.title("📊 MLOps-Driven-Banking-Churn-Analytics-System")
    st.caption("Comprehensive analysis of customer churn patterns and trends")
    st.divider()
    
    # Database connection
    engine = get_database_connection()
    if engine is None:
        st.error("Failed to connect to database. Please check your configuration.")
        st.stop()
    
    # Load data
    with st.spinner("Loading data..."):
        df = load_data(engine)
    
    if df is None or df.empty:
        st.error("No data available. Please check your database.")
        st.stop()
    
    # Apply filters
    df_filtered = render_sidebar_filters(df)
    
    # Calculate and display KPIs
    kpis = calculate_kpis(df_filtered)
    render_kpi_cards(kpis)
    
    # Visualizations
    plot_credit_score_distribution(df_filtered)
    
    plot_churn_by_geography(df_filtered)
    
    plot_additional_insights(df_filtered)
    
    # Data insights
    st.divider()
    st.subheader("💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
        <h4 style="color: #1f77b4; margin-top: 0;">📊 Churn Overview</h4>
        <p><strong>Churn Rate:</strong> <span style="color: #e74c3c; font-size: 1.1rem; font-weight: 700;">{kpis['churn_rate']:.2f}%</span></p>
        <p><strong>Churned:</strong> {kpis['churned_customers']:,} customers</p>
        <p><strong>Retention:</strong> <span style="color: #2ecc71; font-weight: 600;">{100 - kpis['churn_rate']:.2f}%</span></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="insight-box">
        <h4 style="color: #1f77b4; margin-top: 0;">💼 Customer Metrics</h4>
        <p><strong>Avg Credit Score:</strong> <span style="font-size: 1.1rem; font-weight: 600;">{kpis['avg_credit_score']:.0f}</span></p>
        <p><strong>Active:</strong> {kpis['active_customers']:,}</p>
        <p><strong>Total Records:</strong> {kpis['total_customers']:,}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Data explorer
    with st.expander("📋 View Raw Data"):
        st.dataframe(
            df_filtered,
            use_container_width=True,
            hide_index=True
        )
        
        # Download button
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Data as CSV",
            data=csv,
            file_name="banking_churn_data.csv",
            mime="text/csv"
        )
    
    # Footer
    st.divider()
    st.caption("Dashboard built with Streamlit • Data refreshes every 10 minutes")


if __name__ == "__main__":
    main()
   # streamlit run dashboard/app.py

