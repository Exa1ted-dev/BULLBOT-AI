# BULLBOT - AI-Powered Reddit Misinformation Detection & Response Bot

**BULLBOT** is an autonomous Reddit bot that runs 24/7 for free. It detects misinformation, verifies claims using real sources, and replies with AI-generated, fact-checked comments. It’s designed to patrol high-risk subreddits and help curb the spread of false or misleading content.

Until a public dashboard is live, you can follow its activity on [Reddit](https://www.reddit.com/user/BULLBOT_AI/).

---

## Features

- **Targeted Reddit Scraper** – Scrapes recent posts from specified subreddits using [PRAW](https://praw.readthedocs.io/).
- **Misinformation Classifier** – Identifies likely false claims using a [Hugging Face Space](https://huggingface.co/spaces/Exa1ted-dev/BULLBOT-post-classification).
- **Fact Search Engine** – Uses [SerpAPI](https://serpapi.com/) to query Google and find relevant articles.
- **Article Summarizer** – Summarizes sources using [Newspaper3k](https://newspaper.readthedocs.io/en/latest/).
- **AI Response Generation** – Crafts professional, cited responses using a dynamically constructed prompt and [DeepSeek-R1](https://huggingface.co/deepseek-ai/DeepSeek-R1).
- **Autonomous Commenting** – Posts the generated reply directly to Reddit, fully hands-free.
- **Persistent Storage** – Logs all replies and metadata to [Supabase](https://supabase.com/).
- **Keep-Alive Pinger** - Pings the Render web service every 10 minutes to keep it awake with [GitHub-Actions](https://docs.github.com/en/actions)

---

## Tech Stack

- **[Python](https://www.python.org/)** – Core language
- **[PRAW](https://praw.readthedocs.io/)** – Reddit API wrapper
- **[Hugging Face Transformers + Inference API](https://huggingface.co/)** – Classification and generation models
- **[SerpAPI](https://serpapi.com/)** – Google Search automation
- **[Newspaper3k](https://newspaper.readthedocs.io/)** – Article content parsing and summarizing
- **[Flask](https://flask.palletsprojects.com/)** – Lightweight web server
- **[Render](https://render.com/)** – Cloud deployment and 24/7 uptime
- **[Supabase](https://supabase.com/)** – Postgres DB + RESTful backend

---

## Roadmap

- Add image analysis for post context and support for image-only misinformation
- Launch a public dashboard to visualize BULLBOT’s activity and impact
- Upgrade hosting and AI methods to allow higher scale (more posts, faster response)
- Build a user-friendly template to let others deploy their own versions

---

## License

This project is licensed under the **MIT License**.

---

## Author

**Created by Maxx Witlox** – [@Exa1ted-dev](https://github.com/Exa1ted-dev)

**If you like this project or find it interesting, feel free to give it a** 🌟 **!**
