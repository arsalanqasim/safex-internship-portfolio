"""Predictive Analytics Engine for LearnHub Academy Enrollment Forecasting.

Developer: Ali Ammar Haider
Target Company: LearnHub Academy (Online Tutoring Platform)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Any
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


class PredictiveDashboardTutorEngine:
    """Handles data loading, linear regression modeling, and dynamic business recommendations."""

    def __init__(self, data_path: str | Path | None = None) -> None:
        if data_path is None:
            self.data_path = Path(__file__).resolve().parent / "data" / "learnhub_enrollment_data.csv"
        else:
            self.data_path = Path(data_path)
            
        self.developer = "Ali Ammar Haider"
        self.role = "Group Member"
        self.email = "ahwheh688@gmail.com"
        self.tech_stack = ["Python", "scikit-learn", "Pandas", "Matplotlib", "Streamlit"]

    def load_data(self) -> pd.DataFrame:
        """Load and return the 24-month historical dataset."""
        if not self.data_path.exists():
            raise FileNotFoundError(f"Historical data file not found at: {self.data_path}")
        return pd.read_csv(self.data_path)

    def run_forecast(self) -> Dict[str, Any]:
        """Train Linear Regression and generate predictions and metrics."""
        df = self.load_data()
        
        # Prepare features (X) and target (y)
        X = df[["Month_Index"]].values
        y = df["Enrollments"].values
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Historical predictions (fit line)
        y_pred = model.predict(X)
        df["Predicted_Enrollments"] = y_pred
        
        # Calculate regression slope (coefficient) and intercept
        slope = float(model.coef_[0])
        intercept = float(model.intercept_)
        
        # Forecast next month (Month 25)
        next_month_index = np.array([[25]])
        next_month_pred = float(model.predict(next_month_index)[0])
        next_month_forecast = int(round(next_month_pred))
        
        # Performance metrics
        r2 = r2_score(y, y_pred)
        mae = mean_absolute_error(y, y_pred)
        
        # Summary metrics
        latest_actual = int(y[-1])
        avg_enrollment = float(np.mean(y))
        
        growth_abs = next_month_forecast - latest_actual
        growth_pct = (growth_abs / latest_actual) * 100 if latest_actual > 0 else 0.0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(df, slope, next_month_forecast)
        
        return {
            "dataset": df,
            "slope": slope,
            "intercept": intercept,
            "forecast_value": next_month_forecast,
            "forecast_raw": next_month_pred,
            "r2_score": r2,
            "mae": mae,
            "latest_actual": latest_actual,
            "average_enrollment": avg_enrollment,
            "growth_absolute": growth_abs,
            "growth_percentage": growth_pct,
            "recommendations": recommendations,
        }

    def _generate_recommendations(self, df: pd.DataFrame, slope: float, forecast_val: int) -> list[str]:
        """Dynamically calculate dataset conditions and generate exactly 3 business recommendations."""
        recommendations = []
        
        # Condition 1: Operations/Recruiting based on trend (slope direction)
        if slope > 0:
            rec_1 = (
                f"Prepare to recruit additional tutors: The linear trend shows positive growth "
                f"(regression slope = {slope:.2f} enrollments/month). With the forecast indicating a "
                f"further enrollment increase next month, adding tutor resources is recommended to maintain "
                f"student-to-tutor ratios and class quality."
            )
        else:
            rec_1 = (
                f"Audit student retention: The linear trend is flat or declining "
                f"(regression slope = {slope:.2f} enrollments/month). It is recommended to deploy student feedback "
                f"surveys and audit course completion rates to identify friction points and prevent churn."
            )
        recommendations.append(rec_1)
        
        # Condition 2: Lead Conversion Audit
        # Calculate historical conversion rate mean (24 months) and recent conversion rate mean (last 3 months)
        avg_conv = float(df["Lead_Conversion_Rate"].mean())
        recent_conv = float(df["Lead_Conversion_Rate"].iloc[-3:].mean())
        
        # Calculate if marketing spend has been stable over recent months (last 3 months variance is low)
        recent_marketing_std = float(df["Marketing_Spend"].iloc[-3:].std())
        marketing_is_stable = recent_marketing_std < 50.0  # considered stable if standard deviation of last 3 months is small
        
        if recent_conv < avg_conv:
            marketing_status = "stable" if marketing_is_stable else "varying"
            rec_2 = (
                f"Optimize registration funnel: Recent 3-month lead conversion rate ({recent_conv:.2f}%) "
                f"has dropped below the 24-month historical average ({avg_conv:.2f}%), while marketing spend has been "
                f"relatively {marketing_status}. We recommend auditing checkout page UX and simplifying the signup form "
                f"to recover conversion efficiency."
            )
        else:
            rec_2 = (
                f"Capitalize on conversion health: Recent 3-month lead conversion rate ({recent_conv:.2f}%) "
                f"exceeds or matches the 24-month baseline ({avg_conv:.2f}%). We recommend documenting recent email "
                f"templates and social media hooks to capture key patterns and scale them for future outreach campaigns."
            )
        recommendations.append(rec_2)
        
        # Condition 3: Administrative Load Capacity Check
        max_actual = int(df["Enrollments"].max())
        if forecast_val > max_actual:
            rec_3 = (
                f"Audit administrative capacity: The next-month enrollment forecast ({forecast_val}) exceeds the "
                f"historical 24-month maximum ({max_actual} students). We recommend reviewing server capacities, "
                f"support ticketing workflows, and student onboarding sequences to ensure they can handle this record load."
            )
        else:
            rec_3 = (
                f"Maintain standard capacity limits: The next-month enrollment forecast ({forecast_val}) remains "
                f"within historical capacity limits (max actual = {max_actual} students). Standard class slot "
                f"allocations and onboarding queues should be maintained while monitoring weekly registration rates."
            )
        recommendations.append(rec_3)
        
        return recommendations
