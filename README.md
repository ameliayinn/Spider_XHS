# 小红书点赞收藏批量管理

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/nodejs-20%2B-green)](https://nodejs.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

[English](./README_en.md) | [中文](./README.md)

**⚠️ 本项目仅供学习交流使用，禁止任何商业化行为，如有违反，后果自负**

---

## ⭐ 已实现功能

| 模块 | 功能 | 状态 |
|------|------|------|
| **小红书 PC 端** | 二维码登录 / 手机验证码登录 | ✅ |
| | 获取主页所有频道 & 推荐笔记 | ✅ |
| | 获取用户主页信息 / 自己的账号信息 | ✅ |
| | 获取用户发布 / 喜欢 / 收藏的所有笔记 | ✅ |
| | 获取笔记详细内容（无水印图片 & 视频） | ✅ |
| | 搜索笔记 & 搜索用户 | ✅ |
| | 获取笔记评论 | ✅ |
| | 获取未读消息 / 评论@提醒 / 点赞收藏 / 新增关注 | ✅ |
| **创作者平台** | 二维码登录 / 手机验证码登录 | ✅ |
| | 上传图集作品 | ✅ |
| | 上传视频作品 | ✅ |
| | 查看已发布作品列表 | ✅ |
| **蒲公英平台** | 获取 KOL 博主列表 & 详细数据 | ✅ |
| | 获取博主粉丝画像 & 历史趋势 | ✅ |
| | 发起合作邀请 | ✅ |
| **千帆平台** | 获取分销商列表 & 详细数据 | ✅ |
| | 获取分销商合作品类 / 店铺 / 商品信息 | ✅ |

---

## 🤖 接入 AI 智能体

Spider_XHS 天然适合作为 AI 运营 Agent 的数据底座，以下是几种典型用法：

### 场景一：竞品笔记采集 + AI 改写 + 自动发布

```python
from apis.xhs_pc_apis import XHS_Apis
from apis.xhs_creator_apis import XHS_Creator_Apis

pc_api = XHS_Apis()
creator_api = XHS_Creator_Apis()

# 1. 采集竞品笔记
success, msg, note = pc_api.get_note_info(note_url, cookies_str)

# 2. 交给 AI 改写（接入任意大模型）
rewritten = your_ai_agent(note['content'])   # GPT / Claude / Qwen / 本地模型

# 3. 自动上传到创作者平台
creator_api.post_note({
    "title": rewritten['title'],
    "desc": rewritten['desc'],
    "media_type": "image",
    "images": [...],
    ...
}, creator_cookies_str)
```

### 场景二：关键词监控 + AI 情报分析

```python
# 搜索指定关键词的最新笔记，交给 AI 分析趋势
success, msg, notes = pc_api.search_some_note(query, require_num, cookies_str, ...)
analysis = your_ai_agent(notes)
```

### 场景三：KOL 筛选 + 智能匹配

```python
from apis.xhs_pugongying_apis import PuGongYingAPI

pgy = PuGongYingAPI()
# 获取目标类目的 KOL 数据，交给 AI 评估匹配度
kol_list = pgy.get_some_user(num=50, cookies=cookies)
best_kols = your_ai_agent(kol_list, brand_profile)
```

---

## 🧩 Skills 支持

当前项目已经支持基于 skills 的能力接入，既可以直接作为 `Spider_XHS` 的底层能力仓库使用，也可以通过标准化 skills 方式被上层 Agent 工具链引入。


---

## 🎨 爬虫效果图

### 处理后的所有用户

### 某个用户所有的笔记

### 某个笔记具体的内容

### 保存的 Excel
![image](https://github.com/user-attachments/assets/707f20ed-be27-4482-89b3-a5863bc360e7)

---

## 🛠️ 快速开始

### ⛳ 环境要求

- Python 3.10+
- Node.js 20+

### 🎯 安装依赖

```bash
pip install -r requirements.txt
npm install
```

### 🎨 配置 Cookie

在项目根目录的 `.env` 文件中填入你的登录 Cookie：

```
COOKIES='your_cookie_here'
```

Cookie 获取方式：浏览器登录小红书后，按 `F12` 打开开发者工具 → 网络 → Fetch/XHR → 找任意一个请求 → 复制请求头中的 `cookie` 字段。

![image](https://github.com/user-attachments/assets/6a7e4ecb-0432-4581-890a-577e0eae463d)

![image](https://github.com/user-attachments/assets/5e62bc35-d758-463e-817c-7dcaacbee13c)

> **注意：必须是登录后的 Cookie，未登录状态无效。**

### 🚀 运行项目

```bash
python main.py
```

### 🐳 Docker 部署（可选）

```bash
docker build -t spider_xhs .
docker run -e COOKIES='your_cookie_here' spider_xhs
```

---

## 📁 项目结构

```
Spider_XHS/
├── main.py                          # 主入口：爬虫调用示例
├── apis/
│   ├── xhs_pc_apis.py               # 小红书PC端完整API（采集）
│   ├── xhs_creator_apis.py          # 创作者平台API（上传发布）
│   ├── xhs_pc_login_apis.py         # PC端登录（二维码/手机验证码）
│   ├── xhs_creator_login_apis.py    # 创作者平台登录
│   ├── xhs_pugongying_apis.py       # 蒲公英平台API（KOL数据）
│   └── xhs_qianfan_apis.py          # 千帆平台API（分销商数据）
├── xhs_utils/
│   ├── common_util.py               # 初始化工具（读取.env配置）
│   ├── cookie_util.py               # Cookie解析
│   ├── data_util.py                 # 数据处理（Excel保存、媒体下载）
│   ├── xhs_util.py                  # PC端签名算法封装
│   ├── xhs_creator_util.py          # 创作者平台签名算法封装
│   ├── xhs_pugongying_util.py       # 蒲公英平台工具
│   └── xhs_qianfan_util.py          # 千帆平台工具
├── static/
│   ├── xhs_main_260411.js           # PC端签名核心JS（最新版）
│   ├── xhs_creator_260411.js        # 创作者平台签名核心JS（最新版）
│   └── ...
├── .env                             # Cookie配置（不要提交到git）
├── requirements.txt
├── Dockerfile
└── package.json
```

---

## 🗝️ 注意事项

- `main.py` 是爬虫入口，可根据需求修改调用逻辑
- `apis/xhs_pc_apis.py` 包含所有 PC 端数据接口
- `apis/xhs_creator_apis.py` 包含创作者平台发布接口
- Cookie 有时效性，失效后需重新获取
- 建议配合代理（proxies 参数）使用，降低封号风险

---

## 🍥 更新日志

| 日期 | 说明 |
|------|------|
| 23/08/09 | 首次提交 |
| 23/09/13 | API 更改 params 增加两个字段，修复图片无法下载，修复部分页面无法访问报错 |
| 23/09/16 | 修复较大视频编码问题，加入异常处理 |
| 23/09/18 | 代码重构，加入失败重试 |
| 23/09/19 | 新增下载搜索结果功能 |
| 23/10/05 | 新增跳过已下载功能，获取更详细的笔记和用户信息 |
| 23/10/08 | 上传至 PyPI，可通过 pip install 安装 |
| 23/10/17 | 搜索下载新增排序方式（综合 / 热门 / 最新） |
| 23/10/21 | 新增图形化界面，上传至 release v2.1.0 |
| 23/10/28 | Fix Bug：修复搜索功能隐藏问题 |
| 25/03/18 | 更新 API，修复部分问题 |
| 25/06/07 | 更新 search 接口，区分视频和图集下载，新增创作者平台 API |
| 25/07/15 | 更新 xs version56 & 小红书创作者接口 |
| 26/04/11 | 重构创作者平台 API（图集 / 视频上传），新增蒲公英 KOL 数据 API，新增千帆分销商 API，签名算法升级至最新版 |

---

## 🧸 额外说明

1. 感谢 Star ⭐ 和 Follow，项目会持续更新
2. 欢迎 PR 和 Issue。

---

## 💡 Acknowledgements

本项目代码基于 [cv-cat/Spider_XHS](https://github.com/cv-cat/Spider_XHS) 仓库进行了定制化修改与封装。
