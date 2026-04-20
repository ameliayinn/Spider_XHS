<p align="center">
  <a href="https://github.com/ameliayinn/Spider_XHS" target="_blank">
    <picture>

    </picture>
  </a>
</p>

<div align="center">

# Spider_XHS

**Professional Xiaohongshu (RED) Data Scraping & Omnichannel Operations Solution & Agent Skills**

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/nodejs-20%2B-green)](https://nodejs.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

[English](./README_en.md) | [中文](./README.md)

</div>

> **In the explosion era of AI large models, the essence of content operations competition is efficiency.**
> This project encapsulates the fully functional data scraping and content publishing capabilities of the Xiaohongshu platform, providing reliable and stable underlying API support for developers building AI operations agents.

**⚠️ This project is strictly for learning and communication purposes. Any commercial use is prohibited, and violators bear all consequences.**

---

## Why this project?

```
Scrape Competitor Notes ──► [Spider_XHS] ──► Your AI Agent (Rewrite / Generate / Analyze) ──► Auto Upload & Publish
                             ▲                                                                    │
                             └──────────── Fetch Data / Manage Account ◄──────────────────────────┘
```

Xiaohongshu does not offer an open or complete content operations API. To integrate AI large models for batch content scraping, smart rewriting, and one-click publishing, the prerequisite is the ability to **read and write platform data stably**. Spider_XHS solves exactly this problem:

- Reverse-engineered the signature algorithms of Xiaohongshu PC Web and Creator Platform (x-s / x-t / x-s-common / x_b3_traceid / sign / q-signature parameters)
- Encapsulated all core HTTP interfaces with transparent signature processing
- Covers three major scenarios simultaneously: **Data Scraping** (PC Web), **Content Publishing** (Creator Platform), and **KOL Data** (Pugongying)

**You build the AI brain, we connect the neural network to Xiaohongshu.**

---

## ⭐ Features Implemented

| Module | Feature | Status |
|--------|---------|--------|
| **Xiaohongshu PC** | QR Code Login / SMS Login | ✅ |
| | Get all channels & recommended notes on homepage | ✅ |
| | Get user profile info / self account info | ✅ |
| | Get all published / liked / collected notes of a user | ✅ |
| | Get note details (watermark-free images & videos) | ✅ |
| | Search notes & search users | ✅ |
| | Get note comments | ✅ |
| | Get unread messages / @mentions / likes & collects / new followers | ✅ |
| **Creator Platform** | QR Code Login / SMS Login | ✅ |
| | Upload image gallery posts | ✅ |
| | Upload video posts | ✅ |
| | View published posts list | ✅ |
| **Pugongying (KOL)** | Get KOL list & detailed data | ✅ |
| | Get KOL follower persona & historical trends | ✅ |
| | Send collaboration invitation | ✅ |
| **Qianfan Platform** | Get distributor list & detailed data | ✅ |
| | Get distributor partnered categories / shops / products | ✅ |

---

## 🤖 Integrate with AI Agents

Spider_XHS is naturally suited as the data foundation for AI operational agents. Here are a few typical setups:

### Scenario 1: Competitor Scraping + AI Rewriting + Auto Publishing

```python
from apis.xhs_pc_apis import XHS_Apis
from apis.xhs_creator_apis import XHS_Creator_Apis

pc_api = XHS_Apis()
creator_api = XHS_Creator_Apis()

# 1. Scrape competitor note
success, msg, note = pc_api.get_note_info(note_url, cookies_str)

# 2. Let AI rewrite (integrates with any large model)
rewritten = your_ai_agent(note['content'])   # GPT / Claude / Qwen / Local Model

# 3. Automatically upload to Creator platform
creator_api.post_note({
    "title": rewritten['title'],
    "desc": rewritten['desc'],
    "media_type": "image",
    "images": [...],
    ...
}, creator_cookies_str)
```

### Scenario 2: Keyword Monitoring + AI Intelligence Analysis

```python
# Search for the latest notes of a specific keyword, let AI analyze trends
success, msg, notes = pc_api.search_some_note(query, require_num, cookies_str, ...)
analysis = your_ai_agent(notes)
```

### Scenario 3: KOL Screening + Smart Matching

```python
from apis.xhs_pugongying_apis import PuGongYingAPI

pgy = PuGongYingAPI()
# Get KOL data of target categories, let AI evaluate match score
kol_list = pgy.get_some_user(num=50, cookies=cookies)
best_kols = your_ai_agent(kol_list, brand_profile)
```

---

## 🧩 Skills Support

The project now supports capability integration based on skills. It can be used directly as the underlying capability repository of `Spider_XHS`, or introduced by upper-layer Agent toolchains through standardized skills.

---

## 🛠️ Quick Start

### ⛳ Requirements

- Python 3.10+
- Node.js 20+

### 🎯 Install Dependencies

```bash
pip install -r requirements.txt
npm install
```

### 🎨 Configure Cookie

Enter your login Cookie in the `.env` file at the root of the project:

```
COOKIES='your_cookie_here'
```

How to get Cookie: After logging into Xiaohongshu via PC browser, press `F12` to open Developer Tools → Network → Fetch/XHR → Find any request → Copy the `cookie` field from request headers.

> **Note: It must be a Cookie from a logged-in session, otherwise it will not work.**

### 🚀 Run the Project

```bash
python main.py
```

### 🐳 Docker Deployment (Optional)

```bash
docker build -t spider_xhs .
docker run -e COOKIES='your_cookie_here' spider_xhs
```

---

## 📁 Repository Structure

```
Spider_XHS/
├── main.py                          # Main entry: scraper usage examples
├── apis/
│   ├── xhs_pc_apis.py               # Complete PC APIs (Scraping)
│   ├── xhs_creator_apis.py          # Creator APIs (Upload & Publish)
│   ├── xhs_pc_login_apis.py         # PC Login (QR code/SMS)
│   ├── xhs_creator_login_apis.py    # Creator platform login
│   ├── xhs_pugongying_apis.py       # Pugongying APIs (KOL data)
│   └── xhs_qianfan_apis.py          # Qianfan APIs (Distributor data)
├── xhs_utils/
│   ├── common_util.py               # Initialization utils (Read .env)
│   ├── cookie_util.py               # Cookie parsing
│   ├── data_util.py                 # Data processing (Save Excel, download media)
│   ├── xhs_util.py                  # PC signature algorithms encapsulated
│   ├── xhs_creator_util.py          # Creator signature algorithms encapsulated
│   ├── xhs_pugongying_util.py       # Pugongying utils
│   └── xhs_qianfan_util.py          # Qianfan utils
├── static/
│   ├── xhs_main_260411.js           # PC signature core JS (Latest version)
│   ├── xhs_creator_260411.js        # Creator platform signature core JS
│   └── ...
├── .env                             # Cookie config (Do not commit to git)
├── requirements.txt
├── Dockerfile
└── package.json
```

---

## 🗝️ Important Notes

- `main.py` is the entry point for scraping, modify the calling logic according to your needs.
- `apis/xhs_pc_apis.py` contains all interfaces for PC data scraping.
- `apis/xhs_creator_apis.py` contains interfaces for Creator platform publishing.
- Cookies have a lifespan and need to be reacquired once expired.
- It is highly recommended to use proxies (via `proxies` param) to reduce the risk of account bans.

---

## 🍥 Changelog

| Date | Description |
|------|-------------|
| 23/08/09 | First commit |
| 23/09/13 | Added two fields to API params, fixed image download issues, fixed 404 on some pages |
| 23/09/16 | Fixed big video encoding issues, added error handling |
| 23/09/18 | Refactored code, added retry mechanisms |
| 23/09/19 | Added feature: Download search results |
| 23/10/05 | Added feature: Skip already downloaded, get detailed note & user info |
| 23/10/08 | Uploaded to PyPI, installable via pip install |
| 23/10/17 | Search & download now supports sorting (General / Hot / Latest) |
| 23/10/21 | Added GUI, uploaded to release v2.1.0 |
| 23/10/28 | Fix Bug: Fixed search feature hidden bug |
| 25/03/18 | Updated API, fixed partial issues |
| 25/06/07 | Updated search interface, separated video and image gallery downloads, added creator APIs |
| 25/07/15 | Updated xs version56 & Xiaohongshu creator interfaces |
| 26/04/11 | Refactored creator APIs (image/video upload), added Pugongying KOL API, added Qianfan Distributor API, updated signature algorithm to latest |

---

## 🧸 Extra Information

1. Thank you for the Star ⭐ and Follow. The project will continue to be updated.
2. PRs and Issues are welcome.

---

## 💡 Acknowledgements

This project's code changes are based on [cv-cat/Spider_XHS](https://github.com/cv-cat/Spider_XHS).
