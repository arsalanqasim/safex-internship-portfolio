"""Streamlit UI for the Predictive Dashboard Tutor Module.

Developer: Ali Ammar Haider
Target Company: LearnHub Academy (Online Tutoring Platform)
"""

from __future__ import annotations

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from src.modules.registry import MODULE_REGISTRY
from src.modules.predictive_dashboard_tutor.engine import PredictiveDashboardTutorEngine


def render_ui() -> None:
    # 1. Instantiate the forecasting engine
    engine = PredictiveDashboardTutorEngine()
    
    try:
        # Run forecasting computations
        results = engine.run_forecast()
    except Exception as exc:
        st.error("Failed to load data or run the forecasting model.")
        st.exception(exc)
        return
        
    metadata = MODULE_REGISTRY["week4"]["predictive_dashboard_tutor"]
    
    # 2. Hero Banner
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-badge">📊 Predictive Analytics Agent</div>
            <div class="hero-title">{metadata["title"]}</div>
            <div class="hero-subtitle">
                Developer: <strong>{metadata["developer"]}</strong> ({metadata["role"]}) · <code>{metadata["email"]}</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 3. Project Scope Information & Specifications Expander
    with st.expander("📌 Module Specifications & Business Context", expanded=False):
        st.write(f"**Assigned Stack**: {' · '.join(metadata['tech'])}")
        st.write(f"**Business Context**: LearnHub Academy — an online tutoring platform (continuing Week 3 case).")
        st.write(
            "**Primary Objective**: Forecast student enrollments for the upcoming month using a simple "
            "Linear Regression model fitted on 24 months of historical operations."
        )
        st.write(
            "⚠️ **Disclaimer**: The historical operational dataset used here contains simulated (synthetic) data "
            "designed for demonstration and testing purposes during this internship."
        )

    # 4. Summary Metrics Row
    latest_actual = results["latest_actual"]
    forecast_value = results["forecast_value"]
    growth_abs = results["growth_absolute"]
    growth_pct = results["growth_percentage"]
    avg_enrollment = results["average_enrollment"]
    
    st.markdown("### 📊 Key Enrollment Forecast Metrics")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(
            label="Latest Actual (Month 24)",
            value=f"{latest_actual} Students",
        )
    with m2:
        # Expected growth indicator
        growth_indicator = "+" if growth_abs >= 0 else ""
        st.metric(
            label="Next-Month Forecast (Month 25)",
            value=f"{forecast_value} Students",
            delta=f"{growth_indicator}{growth_abs} ({growth_indicator}{growth_pct:.1f}%) expected",
            delta_color="normal" if growth_abs >= 0 else "inverse",
        )
    with m3:
        st.metric(
            label="Historical Average Enrollment",
            value=f"{avg_enrollment:.1f} Students",
        )
    with m4:
        st.metric(
            label="Model Fit Accuracy (R²)",
            value=f"{results['r2_score']:.3f}",
            help="Coefficient of determination measuring the linear fit accuracy. Perfect fit is 1.000."
        )

    # 5. Core Layout Columns: Visualization & Data Table
    col_plot, col_data = st.columns([3, 2])
    
    df = results["dataset"]
    
    # Get active UI theme for Matplotlib styling
    theme = st.session_state.get("ui_theme_choice", "Light")
    is_dark = theme == "Dark"
    
    with col_plot:
        st.markdown("### 📈 Historical vs. Predicted Trend Line")
        
        # Plot Matplotlib chart
        fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=150)
        
        # Color palettes matching Light/Dark themes
        bg_color = "#151b24" if is_dark else "#ffffff"
        text_color = "#f8fafc" if is_dark else "#172033"
        grid_color = "#334155" if is_dark else "#dce3ec"
        line_color = "#5eead4" if is_dark else "#0f766e" # Teal accent
        pred_color = "#f43f5e" if is_dark else "#b91c1c" # Rose/Red
        forecast_color = "#22c55e" # Green
        
        fig.patch.set_facecolor(bg_color)
        ax.set_facecolor(bg_color)
        
        # Spine styling
        for spine in ["top", "right"]:
            ax.spines[spine].set_visible(False)
        for spine in ["left", "bottom"]:
            ax.spines[spine].set_color(grid_color)
            ax.spines[spine].set_linewidth(1.0)
            
        # Grid lines
        ax.grid(True, linestyle=":", alpha=0.5, color=grid_color)
        
        # Plot historical data points and linear regression fit line
        ax.plot(
            df["Month_Index"],
            df["Enrollments"],
            label="Historical Actuals",
            color=line_color,
            marker="o",
            markersize=5,
            linewidth=2,
            zorder=3
        )
        ax.plot(
            df["Month_Index"],
            df["Predicted_Enrollments"],
            label="Regression Best-Fit Line",
            color=pred_color,
            linestyle="--",
            linewidth=1.8,
            zorder=2
        )
        
        # Highlight forecast for Month 25
        ax.scatter(
            [25],
            [results["forecast_raw"]],
            color=forecast_color,
            marker="*",
            s=120,
            label="Month 25 Forecast",
            zorder=4
        )
        
        # Labeling
        ax.set_title("Enrollment Forecast (Month 1 to 25)", fontsize=10, fontweight="bold", color=text_color)
        ax.set_xlabel("Month Index", fontsize=8, color=text_color)
        ax.set_ylabel("Students Enrolled", fontsize=8, color=text_color)
        
        ax.tick_params(colors=text_color, labelsize=7)
        ax.set_xlim(0.5, 25.5)
        ax.set_xticks(list(range(1, 26, 2)) + [25])
        
        ax.legend(
            loc="upper left",
            frameon=True,
            facecolor=bg_color,
            edgecolor=grid_color,
            fontsize=7,
            labelcolor=text_color
        )
        
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig) # Prevent figure leakage

    with col_data:
        st.markdown("### 📋 Enrollment Data Records")
        
        # Prepare tabular representation of historical dataset and forecast
        table_df = df[["Month_Index", "Month_Label", "Enrollments", "Revenue", "Lead_Conversion_Rate"]].copy()
        
        # Add next-month forecast row
        forecast_row = pd.DataFrame([{
            "Month_Index": 25,
            "Month_Label": "2026-09 (Forecast)",
            "Enrollments": int(round(forecast_value)),
            "Revenue": None,
            "Lead_Conversion_Rate": None,
        }])
        
        display_df = pd.concat([table_df, forecast_row], ignore_index=True)
        display_df.columns = ["Index", "Month", "Enrollments", "Revenue ($)", "Conv. Rate (%)"]
        
        # Render table with streamlit dataframe
        st.dataframe(
            display_df,
            width="stretch",
            hide_index=True,
            height=320,
        )
        st.caption("ℹ️ *Month 25 shows the predicted enrollment generated by the Linear Regression model.*")

    st.divider()

    # 6. Dynamic Business Recommendations Section
    st.markdown("### 💡 Data-Driven Recommendations")
    st.caption("These business insights are evaluated dynamically based on computed metrics and conversion patterns of the dataset.")
    
    rec_list = results["recommendations"]
    
    col_rec1, col_rec2, col_rec3 = st.columns(3)
    
    # Recommendation 1: Operations/Recruiting
    with col_rec1:
        st.markdown("##### 👥 Tutor Staffing & Operations")
        if results["slope"] > 0:
            st.info(rec_list[0])
        else:
            st.warning(rec_list[0])
            
    # Recommendation 2: Funnel Optimization
    with col_rec2:
        st.markdown("##### 🎯 Marketing & Lead Funnel")
        # Check if recent conversion was below historical average
        avg_c = float(df["Lead_Conversion_Rate"].mean())
        recent_c = float(df["Lead_Conversion_Rate"].iloc[-3:].mean())
        if recent_c < avg_c:
            st.warning(rec_list[1])
        else:
            st.success(rec_list[1])
            
    # Recommendation 3: Capacity Planning
    with col_rec3:
        st.markdown("##### 🏢 Administrative Capacity")
        max_act = int(df["Enrollments"].max())
        if forecast_value > max_act:
            st.warning(rec_list[2])
        else:
            st.success(rec_list[2])

    # 7. Model Specs Footer
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(
        f"**Algorithm**: Ordinary Least Squares (OLS) Linear Regression | "
        f"**R²**: {results['r2_score']:.4f} | **MAE**: {results['mae']:.2f} | "
        f"**Disclaimer**: Data is simulated. Model assumes linear continuation of historical growth."
    )
