# Research Notes: AI Social Media Automation & APIs

**Author:** Ali Ammar Haider  
**Topic:** Social Media APIs, Automated Scheduling Architectures, and Prompt Engineering  
**Date:** July 23, 2026  

---

## 1. Social Media API Reference & Auth Workflows

Integrating automation engines into live production systems requires establishing OAuth 2.0 validation pipelines:

### A. Meta Graph API (Instagram & Facebook)
- **Authentication**: Requires a Meta Developer Account, a registered App, Facebook Login integration, and a Page Access Token with `instagram_basic` and `instagram_content_publish` scopes.
- **Workflow**:
  1. Upload the media file to a public CDN (e.g. AWS S3).
  2. Send a `POST` request to `/{instagram-business-account-id}/media` to create an item container.
  3. Poll the Graph API to check processing status.
  4. Send a `POST` request to `/{instagram-business-account-id}/media_publish` using the container ID to publish.

### B. LinkedIn Community Management API
- **Authentication**: OAuth 2.0 authorization code flow to obtain a Member Access Token with `w_member_social` or `w_organization_social` scope.
- **Workflow**:
  1. Construct a UGC Post payload matching the LinkedIn schema (`ugcPosts` endpoint).
  2. Send a JSON request specifying the author (e.g., `urn:li:person:abcdef123`), post visibility (`PUBLIC`), and commentary text containing the caption and links.

### C. X (Twitter) API v2
- **Authentication**: OAuth 1.0a User Context (API Keys and Access Tokens) or OAuth 2.0 Authorization Code Flow with PKCE.
- **Workflow**:
  1. Initialize Tweepy client passing authorization tokens.
  2. Call `client.create_tweet(text=caption)` returning the tweet ID.
  3. Strict 280-character ceiling applies for standard accounts (longer for X Premium, though standard API uses 280-char cutoff).

---

## 2. Queueing & Scheduling Architecture

To automate posting over a 7-day period without manual client activation, we propose an asynchronous task execution queue:

```text
+-----------------------+      Save      +--------------------------+
|  Streamlit Scheduler  | -------------> | PostgreSQL Campaign Table|
+-----------------------+                +--------------------------+
                                                      ^
                                                      | Fetch due posts
                                                      v
                                         +--------------------------+
                                         |    Celery Beat Worker    |
                                         +--------------------------+
                                                      |
                                                      | Trigger task
                                                      v
+-----------------------+  Post Content  +--------------------------+
|   Social Media APIs   | <------------- |   Celery Event Worker    |
+-----------------------+                +--------------------------+
```

- **Cron Triggers**: A Celery Beat worker runs every 15 minutes, query-filtering the database for posts where `scheduled_time <= NOW()` and `status == 'QUEUED'`.
- **Worker Execution**: Celery workers pick up the task, hit the DALL-E/Midjourney APIs for image generation, host the asset on an S3 bucket, and then hit the social media publishing APIs.

---

## 3. Prompt Engineering for Educational Content

For tutoring platforms, image prompts must translate abstract educational topics (e.g. coding loops, equations, spreadsheets) into visually engaging, professional graphics:

- **Style Presets**:
  - *Isometric Digital Art*: Good for LinkedIn tech posts.
  - *Cinematic Photo*: Good for Facebook community features showing student workspaces.
  - *Flat Vector UI*: Good for Instagram carousel slides detailing coding syntax.
- **Negative Prompts**: Exclude low-quality artifacts, distorted texts, warped laptop keyboards, and busy background clutter to keep the visuals looking premium.
