"""Streamlit UI for AI Social Media Scheduler & Caption Generator.

Developer: Ali Ammar Haider
Target Company: Online Tutoring Platform
"""

from __future__ import annotations

import json
import streamlit as st
import pandas as pd
from src.modules.social_media_scheduler.engine import SocialMediaSchedulerEngine


def render_ui() -> None:
    engine = SocialMediaSchedulerEngine()

    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-badge">Social Media Agent</div>
            <div class="hero-title">📅 AI Social Media Scheduler & Caption Generator</div>
            <div class="hero-subtitle">
                Generate, edit, and queue a 7-day optimized social media calendar tailored for an 
                online tutoring platform. Includes automated character audits, image prompts, and API integration proposals.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ⚙️ Campaign Configurations")
    
    col_a, col_b = st.columns(2)
    with col_a:
        company = st.text_input(
            "Tutoring Platform Name",
            value="LearnHub Academy",
            help="Name of the tutoring brand / company."
        )
        audience = st.text_input(
            "Target Audience",
            value="University Students",
            help="E.g., High Schoolers, Working Professionals, Coding Beginners."
        )
        tone = st.selectbox(
            "Tone of Voice",
            ["Professional", "Friendly", "Motivational", "Promotional"],
            help="Choose the messaging style for caption generation."
        )

    with col_b:
        platforms = st.multiselect(
            "Target Social Platforms",
            ["Instagram", "Facebook", "LinkedIn", "X (Twitter)"],
            default=["LinkedIn", "Instagram", "X (Twitter)"],
            help="Select platforms to distribute the 7-day schedule across."
        )
        topics_text = st.text_area(
            "Weekly Key Topics (One Topic Per Line)",
            value="Python Basics\nAI Tools\nCareer Tips\nExcel Skills\nScholarships\nInterview Preparation\nData Analytics",
            height=120,
            help="Topics will rotate daily through the 7-day campaign calendar."
        )

    topics = [t.strip() for t in topics_text.split("\n") if t.strip()]

    # Trigger Generation
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Generate & Audit 7-Day Campaign", type="primary", use_container_width=True):
        if not topics:
            st.error("Please enter at least one topic.")
            return
        if not platforms:
            st.error("Please select at least one social media platform.")
            return

        with st.spinner("Analyzing topics and generating optimized content..."):
            df = engine.generate_calendar(
                company=company,
                audience=audience,
                tone=tone,
                platforms=platforms,
                topics=topics
            )
            
            # Store generated data in session state for interactivity
            st.session_state.social_calendar_df = df
            st.session_state.social_campaign_ready = True
            st.session_state.edited_captions = {i: row["Caption"] for i, row in df.iterrows()}

    # Show results if available in session state
    if st.session_state.get("social_campaign_ready", False):
        df = st.session_state.social_calendar_df
        edited_captions = st.session_state.edited_captions

        st.success("✨ 7-Day Content Calendar Generated Successfully!")

        # Dashboard Summary Metrics
        st.markdown("### 📊 Campaign Health & Metrics")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("📅 Total Scheduled Posts", len(df))
        with m2:
            st.metric("📱 Platforms Covered", df["Platform"].nunique())
        with m3:
            st.metric("🎯 Niche Topics Rotated", df["Topic"].nunique())
        with m4:
            invalid_limits = sum(1 for i, row in df.iterrows() if len(f"{edited_captions[i]}\n\n{row['Hashtags']}") > engine.platform_limits.get(row["Platform"], 3000))
            if invalid_limits > 0:
                st.metric("⚠️ Limit Violations", f"{invalid_limits} Alert(s)", delta="-Action Needed", delta_color="inverse")
            else:
                st.metric("✅ Limit Check", "All Safe", delta="100% OK")

        # Interactive Calendar Board
        st.markdown("### 📅 Interactive Content Editor")
        st.info("💡 You can select any day tab below, preview and edit the AI-generated captions in real-time, and download the audited final calendar.")

        # Create tabs for days
        day_tabs = st.tabs([f"📅 {row['Day']} ({row['Platform']})" for _, row in df.iterrows()])

        for idx, row in df.iterrows():
            with day_tabs[idx]:
                col_c, col_d = st.columns([3, 2])
                
                with col_c:
                    st.markdown(f"#### **Topic:** {row['Topic']}")
                    
                    # Real-time caption editor
                    current_caption = edited_captions[idx]
                    new_caption = st.text_area(
                        "Edit Post Caption",
                        value=current_caption,
                        height=200,
                        key=f"edit_cap_{idx}"
                    )
                    st.session_state.edited_captions[idx] = new_caption

                    st.markdown("**Generated Hashtags:**")
                    st.code(row["Hashtags"], language="markdown")

                with col_d:
                    # Platform and Time Details
                    st.markdown(f"**Target Network:** `{row['Platform']}`")
                    st.markdown(f"**Recommended Optimal Time:** `{row['Optimal Time']}`")
                    
                    # Character check calculation
                    total_len = len(f"{new_caption}\n\n{row['Hashtags']}")
                    limit = engine.platform_limits.get(row["Platform"], 3000)
                    
                    st.markdown(f"**Character Audit:** `{total_len} / {limit}` characters")
                    if total_len > limit:
                        st.error(f"❌ Exceeds {row['Platform']} limit by {total_len - limit} characters!")
                    else:
                        st.success(f"✅ Within {row['Platform']} character limit.")

                    # DALL-E / Midjourney Visual Prompt
                    st.markdown("**Suggested Creative Asset / Image Prompt:**")
                    st.info(row["Image Prompt"])
                    
                    if st.button("🚀 Push to Queue", key=f"queue_btn_{idx}", use_container_width=True):
                        st.toast(f"Post for {row['Day']} pushed to scheduling engine pipeline!", icon="🚀")

        # Export Buttons
        st.markdown("### 💾 Export & Download Calendar")
        # Build updated DataFrame with edited captions
        final_df = df.copy()
        final_df["Caption"] = [st.session_state.edited_captions[i] for i in range(len(df))]
        final_df["Char Count"] = [len(f"{row['Caption']}\n\n{row['Hashtags']}") for _, row in final_df.iterrows()]
        
        # Add a column marking whether limits are still met
        final_df["Meets Limit"] = [
            row["Char Count"] <= engine.platform_limits.get(row["Platform"], 3000)
            for _, row in final_df.iterrows()
        ]

        csv_data = final_df.to_csv(index=False).encode("utf-8")
        
        # JSON formatting
        json_data = final_df.to_json(orient="records", indent=2)

        col_e, col_f = st.columns(2)
        with col_e:
            st.download_button(
                "📥 Download Content Calendar (CSV)",
                data=csv_data,
                file_name="tutoring_social_calendar.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_f:
            st.download_button(
                "📥 Download Content Calendar (JSON)",
                data=json_data,
                file_name="tutoring_social_calendar.json",
                mime="application/json",
                use_container_width=True
            )

        # API Proposal Playground
        st.markdown("---")
        st.markdown("### 🔌 API Integration & Automation Proposal")
        
        prop_tab1, prop_tab2, prop_tab3 = st.tabs([
            "🔗 Social API Integrations",
            "🧩 API Payload Schema",
            "🕰️ Automation Architecture"
        ])
        
        with prop_tab1:
            st.markdown(
                """
                To connect the **AI Social Media Scheduler** to live social platforms, we integrate with their official APIs:
                
                - **LinkedIn API (Community Management API)**: Shares posts on personal profiles or organization pages.
                - **Meta Graph API (Instagram & Facebook)**: Creates container media assets, uploads images, and schedules feed posts.
                - **X (Twitter) API v2 (Manage Tweets)**: Publishes status updates up to 280 characters.
                """
            )
            
            code_select = st.selectbox(
                "View Integration Code Example",
                ["LinkedIn Sharing SDK", "Meta Graph API (Instagram)", "X/Twitter Tweepy Client"]
            )
            
            if code_select == "LinkedIn Sharing SDK":
                st.code(
                    """
import requests

def post_to_linkedin(access_token, author_urn, text_content, hashtags):
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": f"{text_content}\\n\\n{hashtags}"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
                    """,
                    language="python"
                )
            elif code_select == "Meta Graph API (Instagram)":
                st.code(
                    """
import requests

def post_to_instagram(page_id, instagram_business_account_id, access_token, image_url, caption):
    # Step 1: Create media container
    container_url = f"https://graph.facebook.com/v18.0/{instagram_business_account_id}/media"
    container_payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }
    r = requests.post(container_url, data=container_payload).json()
    creation_id = r.get("id")
    
    # Step 2: Publish media container
    publish_url = f"https://graph.facebook.com/v18.0/{instagram_business_account_id}/media_publish"
    publish_payload = {
        "creation_id": creation_id,
        "access_token": access_token
    }
    res = requests.post(publish_url, data=publish_payload)
    return res.json()
                    """,
                    language="python"
                )
            else:
                st.code(
                    """
import tweepy

def post_to_twitter(api_key, api_secret, access_token, access_token_secret, tweet_text):
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )
    response = client.create_tweet(text=tweet_text)
    return response.data
                    """,
                    language="python"
                )

        with prop_tab2:
            st.markdown("Below is the structured JSON payload generated by the scheduler agent and pushed to the publishing queue API:")
            
            sample_payload = {
                "campaign_id": "CAMPAIGN-WEEK3-LEARNHUB",
                "target_platform": df.iloc[0]["Platform"],
                "scheduled_time_utc": "2026-07-27T13:00:00Z",
                "post_content": {
                    "text": edited_captions[0],
                    "hashtags": df.iloc[0]["Hashtags"],
                    "full_length": len(f"{edited_captions[0]}\n\n{df.iloc[0]['Hashtags']}")
                },
                "asset_creation": {
                    "image_generation_prompt": df.iloc[0]["Image Prompt"],
                    "aspect_ratio": "16:9"
                },
                "audit_status": {
                    "meets_limit": bool(df.iloc[0]["Meets Limit"]),
                    "character_limit": engine.platform_limits.get(df.iloc[0]["Platform"])
                }
            }
            st.json(sample_payload)

        with prop_tab3:
            st.markdown(
                """
                #### **Production Scheduling Architecture**
                
                The diagram below illustrates the fully automated scheduler agent pipeline. The engine generates posts, saves them to a database, and cron workers run tasks periodically to retrieve and publish them.
                """
            )
            st.markdown(
                """
                ```mermaid
                graph TD
                    A[Streamlit Scheduler UI] -->|Save Calendar| B[(PostgreSQL Database)]
                    B -->|Fetch Due Posts| C[Celery Beat Worker / Cron Scheduler]
                    C -->|Generate Visuals| D[DALL-E 3 Image API]
                    D -->|Return Image CDN Link| E[Publishing Task Executor]
                    E -->|POST Request| F{Social Media APIs}
                    F -->|Upload| G[LinkedIn API]
                    F -->|Upload| H[Meta Graph API]
                    F -->|Upload| I[X API v2]
                ```
                """,
                unsafe_allow_html=True
            )

    st.divider()
    info = engine.get_info()
    st.caption(
        f"**Developer:** {info['developer']} | **Status:** {info['status']} | **Version:** {info['version']}"
    )