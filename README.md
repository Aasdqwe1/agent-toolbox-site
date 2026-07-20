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
| `assets/js/main.js` | 导航滚动样式 + 进入视口淡入动画 + 实时拉取最新 CI 构建 |
| `assets/favicon.png` | 站点图标（圆角渐变方块） |

## 下载（实时最新 CI 构建）

下载按钮由前端 JS 调用 GitHub API（`/repos/Aasdqwe1/agent-toolbox/releases`）实时获取：

- 优先取 `latest` 预发布（推送 `main` 触发的滚动 CI 构建，APK 名含 commit sha）；
- 若 `latest` 不存在，则回退到最新正式版 Release；
- 按钮 `href` 自动指向最新 APK 的 `browser_download_url`，并显示大小与发布时间；
- API 受限/失败时回退到 Releases 页面，不影响页面可用性。

要求：Android 7.0+（API 24），arm64-v8a 架构。
| `404.html` | 自定义 404 页面 |

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

## 目录结构

```
agent-toolbox-site/
├── index.html
├── 404.html
├── README.md
└── assets/
    ├── css/style.css
    └── js/main.js
```
