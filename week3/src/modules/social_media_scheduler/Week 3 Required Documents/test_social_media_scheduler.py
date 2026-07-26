"""Tests for Ali Ammar Haider's AI Social Media Scheduler Engine."""

from __future__ import annotations

import pandas as pd
from src.modules.social_media_scheduler.engine import SocialMediaSchedulerEngine


def test_calendar_generation_basic():
    """Verify that calendar generates exactly 7 days with correct structure."""
    engine = SocialMediaSchedulerEngine()
    df = engine.generate_calendar(
        company="LearnHub Academy",
        audience="University Students",
        tone="Friendly",
        platforms=["LinkedIn", "Instagram"],
        topics=["Python Basics", "AI Tools"]
    )
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 7
    expected_cols = [
        "Day", "Platform", "Topic", "Caption", "Hashtags", 
        "Image Prompt", "Optimal Time", "Char Count", "Meets Limit"
    ]
    for col in expected_cols:
        assert col in df.columns


def test_platform_specific_twitter_limit():
    """Verify that X (Twitter) posts respect the character limit."""
    engine = SocialMediaSchedulerEngine()
    df = engine.generate_calendar(
        company="LearnHub Academy",
        audience="University Students",
        tone="Motivational",
        platforms=["X (Twitter)"],
        topics=["Python Basics"]
    )
    
    for _, row in df.iterrows():
        assert row["Platform"] == "X (Twitter)"
        assert row["Char Count"] <= 280
        assert row["Meets Limit"] is True


def test_tone_variation():
    """Verify that changing tone modifies the caption intro styling."""
    engine = SocialMediaSchedulerEngine()
    
    caption_prof = engine.generate_caption(
        company="LearnHub",
        topic="AI Tools",
        tone="Professional",
        platform="LinkedIn",
        audience="Students",
        index=0
    )
    
    caption_friendly = engine.generate_caption(
        company="LearnHub",
        topic="AI Tools",
        tone="Friendly",
        platform="LinkedIn",
        audience="Students",
        index=0
    )
    
    assert "Expert Insights" in caption_prof
    assert "Hey there" in caption_friendly


def test_image_prompt_generation():
    """Verify that image prompts are generated with topic details."""
    engine = SocialMediaSchedulerEngine()
    prompt = engine.generate_image_prompt("Python Basics", 1)
    
    assert "Python Basics" in prompt
    assert "--ar 16:9" in prompt


def test_engine_info():
    """Verify developer name is correct."""
    engine = SocialMediaSchedulerEngine()
    info = engine.get_info()
    
    assert info["developer"] == "Ali Ammar Haider"
    assert info["status"] == "Production Ready"
