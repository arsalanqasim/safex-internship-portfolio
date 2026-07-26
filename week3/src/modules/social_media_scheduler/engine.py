"""AI Social Media Scheduler & Caption Generator Engine.

Developer: Ali Ammar Haider
Target Company: Online Tutoring Platform
Description: Simulates an AI content planning agent that generates 7-day social media posts,
             platform-specific captions, image prompts, and optimal posting times.
"""

from __future__ import annotations

from typing import List, Dict, Any
import pandas as pd
import random


class SocialMediaSchedulerEngine:
    """Handles content calendar generation, simulated AI caption writing, and image prompting."""

    def __init__(self):
        self.developer = "Ali Ammar Haider"
        self.status = "Production Ready"

        self.days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]

        # Call-To-Action templates
        self.ctas = [
            "Join our live interactive sessions today!",
            "Click the link in our bio to book your free trial class.",
            "Start your online learning journey with us now!",
            "Register today and unlock expert-led tutoring support.",
            "Visit our platform to connect with certified tutors!"
        ]

        # Topic-specific content assets for rich simulated generation
        self.topic_assets = {
            "python basics": {
                "hooks": [
                    "Did you know Python is the top programming language for AI and automation?",
                    "Python is simple to learn but incredibly powerful.",
                    "Ready to write your very first line of code?"
                ],
                "points": [
                    "Clean, readable syntax that feels like English.",
                    "Endless career opportunities in AI, Data Science, and Web Dev.",
                    "Massive community support with millions of free libraries."
                ],
                "hashtags": ["#PythonProgramming", "#CodingBasics", "#LearnPython", "#CodeNewbie"]
            },
            "ai tools": {
                "hooks": [
                    "Are you using AI to double your study or work productivity?",
                    "AI tools are changing the face of education and software development.",
                    "Work smarter, not harder—leveraging AI is a superpower."
                ],
                "points": [
                    "Automate repetitive research and summarization tasks.",
                    "Use AI as an interactive, personal tutor to explain complex topics.",
                    "Write code, generate essays, and build presentations in minutes."
                ],
                "hashtags": ["#AITools", "#ArtificialIntelligence", "#TechTrends", "#ProductivityHacks"]
            },
            "career tips": {
                "hooks": [
                    "Technical skills get you interviews, but career habits get you hired.",
                    "Building a standout portfolio is key in today's tech market.",
                    "Looking to land your dream internship or entry-level job?"
                ],
                "points": [
                    "Create open-source projects on GitHub to demonstrate actual work.",
                    "Optimize your LinkedIn profile to attract recruiters directly.",
                    "Practice mock interviews and refine your soft communication skills."
                ],
                "hashtags": ["#CareerTips", "#TechCareers", "#JobPrep", "#Internships"]
            },
            "excel skills": {
                "hooks": [
                    "Stop manual data entry! Excel automation can save you hours of work.",
                    "Excel is still the world's most critical business tool.",
                    "VLOOKUP is good, but have you mastered XLOOKUP and Pivot Tables?"
                ],
                "points": [
                    "Clean raw datasets in seconds with Power Query.",
                    "Visualize financial and operations trends with dynamic charts.",
                    "Build dashboards that executive teams can understand at a glance."
                ],
                "hashtags": ["#ExcelTips", "#DataAnalytics", "#Spreadsheets", "#OfficeHacks"]
            },
            "scholarships": {
                "hooks": [
                    "Don't let tuition fees hold you back—hundreds of global scholarships are open.",
                    "Fund your educational dreams with international student grants.",
                    "Writing a strong personal statement is the key to winning any scholarship."
                ],
                "points": [
                    "Target fully-funded scholarships in Europe, USA, and Asia.",
                    "Keep your academic transcripts and recommendation letters ready.",
                    "Tailor your essays to match the donor organization's core values."
                ],
                "hashtags": ["#Scholarships", "#StudyAbroad", "#FinancialAid", "#StudentSuccess"]
            },
            "interview preparation": {
                "hooks": [
                    "The key to cracking any technical interview is structured preparation.",
                    "Don't memorize code—master problem-solving patterns.",
                    "Answering behavioral questions using the STAR method is a game changer."
                ],
                "points": [
                    "Understand recursion, binary trees, and sliding window concepts.",
                    "Communicate your thought process out loud while coding.",
                    "Ask insightful questions at the end of the interview to show interest."
                ],
                "hashtags": ["#InterviewPrep", "#CodingInterviews", "#TechJobs", "#LeetCode"]
            },
            "data analytics": {
                "hooks": [
                    "Data is the new gold, and knowing how to analyze it is a superpower.",
                    "Decisions backed by data always beat guesses.",
                    "Curious about how businesses predict future consumer trends?"
                ],
                "points": [
                    "Aggregate and query millions of rows using SQL.",
                    "Clean and manipulate data using Python's Pandas library.",
                    "Design interactive dashboards in Power BI or Tableau."
                ],
                "hashtags": ["#DataAnalytics", "#BigData", "#DataScience", "#AnalyticsTips"]
            }
        }

        # Default fallback asset for general educational content
        self.default_asset = {
            "hooks": [
                "Invest in yourself—daily learning leads to long-term success.",
                "Struggling with a difficult course? Expert help is just a click away.",
                "Upgrade your skill set with custom-tailored online tutoring."
            ],
            "points": [
                "Flexible learning hours tailored to your personal schedule.",
                "1-on-1 mentorship with certified academic and tech experts.",
                "Practical assignments and projects that build true confidence."
            ],
            "hashtags": ["#OnlineLearning", "#Elearning", "#EdTech", "#Tutors", "#PersonalGrowth"]
        }

        self.platform_limits = {
            "Instagram": 2200,
            "Facebook": 5000,
            "LinkedIn": 3000,
            "X (Twitter)": 280
        }

        self.platform_optimal_times = {
            "Instagram": "06:00 PM (Leisure Scrolling Peak)",
            "Facebook": "02:00 PM (Afternoon Engagement Peak)",
            "LinkedIn": "09:00 AM (Professional Workday Peak)",
            "X (Twitter)": "01:00 PM (Lunch Hour Scroll Peak)"
        }

    def _get_asset(self, topic: str) -> Dict[str, List[str]]:
        """Match topic string to corresponding assets or return default."""
        topic_lower = topic.lower().strip()
        for key, asset in self.topic_assets.items():
            if key in topic_lower or topic_lower in key:
                return asset
        return self.default_asset

    def generate_caption(
        self,
        company: str,
        topic: str,
        tone: str,
        platform: str,
        audience: str,
        index: int
    ) -> str:
        """Simulate an advanced AI caption generator based on platform-specific formatting rules."""
        asset = self._get_asset(topic)
        
        # Pick hook, points and hashtags deterministically based on index to keep output consistent
        hook = asset["hooks"][index % len(asset["hooks"])]
        points = asset["points"]
        cta = self.ctas[index % len(self.ctas)]
        
        platform_emoji = {
            "Instagram": "✨",
            "Facebook": "📘",
            "LinkedIn": "💼",
            "X (Twitter)": "🐦"
        }.get(platform, "📢")

        # Tone styling intro
        tone_intro = {
            "Professional": "Expert Insights:",
            "Friendly": "Hey there! 👋",
            "Motivational": "Dream big, learn daily! 🌟",
            "Promotional": "Exclusive Offer! 🎯"
        }.get(tone, "Highlights:")

        if platform == "X (Twitter)":
            # Twitter needs to be short and punchy (under 280 characters)
            caption = f"{platform_emoji} {hook}\n\n🎓 {company} offers 1-on-1 tutoring on {topic} for {audience.lower()}.\n\n🔗 {cta}"
            # Trim if needed (basic safety net for Twitter limits)
            if len(caption) > 250:
                caption = f"{platform_emoji} {hook}\n\n🎓 {company} helps you master {topic}!\n\n🔗 {cta}"
            return caption

        elif platform == "LinkedIn":
            # LinkedIn is professional, structured with paragraphs and bullets
            bullet_points = "\n".join([f"• {pt}" for pt in points])
            caption = (
                f"{platform_emoji} **{tone_intro} Master {topic}**\n\n"
                f"{hook}\n\n"
                f"At **{company}**, we specialize in helping {audience.lower()} build hands-on skills with 1-on-1 guidance:\n\n"
                f"{bullet_points}\n\n"
                f"💡 Ready to accelerate your professional growth?\n"
                f"👉 {cta}"
            )
            return caption

        elif platform == "Instagram":
            # Instagram is visually rich, separated with emojis, and calls to action
            bullet_points = "\n".join([f"⚡ {pt}" for pt in points])
            caption = (
                f"{platform_emoji} {tone_intro}\n\n"
                f"{hook}\n\n"
                f"Mastering {topic} has never been easier. **{company}** connects you with top-rated tutors tailored for {audience.lower()}: \n\n"
                f"{bullet_points}\n\n"
                f"📲 {cta}\n"
                f"👇 Save this post for later!"
            )
            return caption

        else:  # Facebook
            # Facebook is friendly, community oriented, asks for comments
            caption = (
                f"{platform_emoji} {tone_intro}\n\n"
                f"{hook}\n\n"
                f"At {company}, we are building a supportive learning community for {audience.lower()}. "
                f"Whether you want to learn {topic} from scratch or brush up on advanced techniques, we have got you covered!\n\n"
                f"💬 What is your biggest challenge when learning {topic}? Let us know in the comments below!\n\n"
                f"✨ {cta}"
            )
            return caption

    def generate_hashtags(self, topic: str, platform: str) -> str:
        """Generate platform-relevant hashtags for the topic."""
        asset = self._get_asset(topic)
        topic_tags = asset["hashtags"]
        
        # Add target niche hashtags
        niche_tags = ["#OnlineTutoring", "#EdTech", "#SkillUp"]
        
        all_tags = list(dict.fromkeys(topic_tags + niche_tags)) # deduplicate
        
        if platform == "X (Twitter)":
            # Twitter should only have 2-3 highly relevant tags
            return " ".join(all_tags[:2])
        elif platform == "LinkedIn":
            return " ".join(all_tags[:4])
        else:
            # Instagram/Facebook can support more tags
            return " ".join(all_tags[:6])

    def generate_image_prompt(self, topic: str, index: int) -> str:
        """Create a detailed visual prompt for image generators like DALL-E or Midjourney."""
        styles = [
            "3D isometric digital art style, glowing neon accents, modern tech aesthetic",
            "Minimalist flat vector illustration, pastel color palette, clean modern UI design",
            "Cinematic photorealistic shot, soft natural morning light, shallow depth of field",
            "Vibrant digital painting, conceptual education theme, high detail, 8k resolution"
        ]
        selected_style = styles[index % len(styles)]
        
        prompt = (
            f"A workspace with a laptop displaying a colorful interface about '{topic}', "
            f"surrounded by learning materials, notebook, and a coffee mug. "
            f"{selected_style}, hyperdetailed, clean composition --ar 16:9"
        )
        return prompt

    def generate_calendar(
        self,
        company: str,
        audience: str,
        tone: str,
        platforms: List[str],
        topics: List[str]
    ) -> pd.DataFrame:
        """Generate the complete 7-day social media content calendar."""
        if not platforms:
            platforms = ["Instagram"]

        if not topics:
            topics = ["General Educational Content"]

        calendar = []

        for i in range(7):
            topic = topics[i % len(topics)]
            platform = platforms[i % len(platforms)]

            caption = self.generate_caption(
                company=company,
                topic=topic,
                tone=tone,
                platform=platform,
                audience=audience,
                index=i
            )

            hashtags = self.generate_hashtags(topic, platform)
            image_prompt = self.generate_image_prompt(topic, i)
            optimal_time = self.platform_optimal_times.get(platform, "12:00 PM")
            
            # Combine caption and hashtags for final audit
            full_post_text = f"{caption}\n\n{hashtags}"
            char_count = len(full_post_text)
            
            limit = self.platform_limits.get(platform, 3000)
            meets_limit = char_count <= limit

            calendar.append({
                "Day": self.days[i],
                "Platform": platform,
                "Topic": topic,
                "Caption": caption,
                "Hashtags": hashtags,
                "Image Prompt": image_prompt,
                "Optimal Time": optimal_time,
                "Char Count": char_count,
                "Meets Limit": meets_limit
            })

        return pd.DataFrame(calendar)

    def get_info(self) -> Dict[str, str]:
        """Return developer and status details for registry sync."""
        return {
            "developer": self.developer,
            "status": self.status,
            "version": "Phase 2 (AI Simulated)",
            "description": "7-Day AI-Simulated Social Media Scheduler & Content Planner"
        }