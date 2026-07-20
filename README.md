# Agent Toolbox 官网

[![部署](https://img.shields.io/badge/GitHub%20Pages-已部署-36d6e7)](https://aasdqwe1.github.io/agent-toolbox-site/)

**Agent Toolbox** 的官方静态网站，用于展示这个 Android 端 MCP 服务端应用的特性、工具集、架构与更新日志。

- 源码仓库：<https://github.com/Aasdqwe1/agent-toolbox>

## 技术栈

纯静态站点，零构建、零运行时依赖：

| 文件 | 说明 |
|------|------|
| `index.html` | 主页面（单页，含锚点导航） |
| `assets/css/style.css` | 冷色调主题样式 |
| `assets/js/main.js` | 导航滚动样式 + 进入视口淡入动画 + 读取本地构建信息 |
| `assets/favicon.png` | 站点图标（圆角渐变方块） |
| `assets/release-info.json` | 由 GitHub Actions 自动同步的最新构建元数据 |
| `404.html` | 自定义 404 页面 |

## 下载（自动同步最新构建）

下载按钮不直接调用 `api.github.com`（浏览器端容易被限流），而是读取同域的 `assets/release-info.json`：

- `.github/workflows/update-release-info.yml` 每小时调用 GitHub API 拉取 `Aasdqwe1/agent-toolbox` 的 releases；
- 同时记录 **最新 CI 构建**（`latest` 滚动预发布）和 **最新正式版**（非 prerelease）；
- 自动生成 `assets/release-info.json` 并提交，GitHub Pages 重新部署；
- 页面 JS 从同域 JSON 读取后直接设置下载链接与版本信息，稳定可靠；
- 同步失败或文件缺失时回退到 Releases 页面，不影响可用性。

要求：Android 7.0+（API 24），arm64-v8a 架构。

## 本地预览

```bash
# 任选其一，在仓库根目录启动本地服务器
python3 -m http.server 8080
# 然后浏览器访问 http://localhost:8080
```

## 部署（GitHub Pages）

本仓库通过 **GitHub Pages** 从 `main` 分支根目录自动部署，访问地址：

> https://aasdqwe1.github.io/agent-toolbox-site/

如需修改内容，直接编辑 `index.html` / `assets/` 后提交推送即可，GitHub Pages 会自动重新构建发布。

## CDN 说明

- 本站点由 **GitHub Pages 托管，已默认接入 Fastly 全球 CDN**，世界各地访问都有边缘缓存加速，无需额外配置。
- **jsDelivr 不适合做整站镜像**：它对 `index.html` 等 HTML 文件会 301 重定向到 `raw.githubusercontent.com`，并不真正经 jsDelivr 边缘节点分发，因此无法用它来加速 HTML 首页。
- 若需要更强的可控加速（自定义缓存策略、中国大陆优化、HTTP/3、压缩等），推荐方案是 **绑定自定义域名 + Cloudflare**（或部署到 Cloudflare Pages / Netlify）。这需要你拥有一个域名，并在仓库 Settings → Pages 中设置自定义域名、将 DNS 指向 Cloudflare。需要的话我可以提供具体步骤或直接帮你配好 CNAME 与 DNS 记录。

## 目录结构

```
agent-toolbox-site/
├── index.html
├── 404.html
├── README.md
├── .github/
│   ├── workflows/update-release-info.yml   # 每小时同步最新构建信息
│   └── scripts/gen-release-info.py
└── assets/
    ├── css/style.css
    ├── js/main.js
    ├── favicon.png
    └── release-info.json                    # 最新构建元数据（自动生成）
```
