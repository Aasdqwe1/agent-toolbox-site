// 导航栏滚动样式
const nav = document.getElementById('nav');
const onScroll = () => {
  if (window.scrollY > 12) nav.classList.add('scrolled');
  else nav.classList.remove('scrolled');
};
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// 页脚年份
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// 进入视口时的淡入动画
const cards = document.querySelectorAll('.card, .tool-group, .arch-col, .step, .flow, .meta-item, .download-card');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.style.opacity = '1';
        e.target.style.transform = 'translateY(0)';
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  cards.forEach((el) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(16px)';
    el.style.transition = 'opacity .5s ease, transform .5s ease';
    io.observe(el);
  });
}

// 实时拉取最新 CI 构建（GitHub API，无需认证，支持 CORS）
(function () {
  const REPO = 'Aasdqwe1/agent-toolbox';
  const FALLBACK = 'https://github.com/Aasdqwe1/agent-toolbox/releases';
  const btn = document.getElementById('dl-btn');
  const title = document.getElementById('dl-title');
  const meta = document.getElementById('dl-meta');
  if (!btn) return;
  async function load() {
    try {
      const res = await fetch(`https://api.github.com/repos/${REPO}/releases?per_page=20`, {
        headers: { 'Accept': 'application/vnd.github+json' }
      });
      if (!res.ok) throw new Error('http');
      const releases = await res.json();
      if (!Array.isArray(releases)) throw new Error('fmt');
      const pick = releases.find((r) => r.tag_name === 'latest' && !r.draft) ||
        [...releases].filter((r) => !r.draft).sort((a, b) => new Date(b.published_at) - new Date(a.published_at))[0];
      if (!pick || !pick.assets || !pick.assets.length) throw new Error('none');
      const asset = pick.assets[0];
      btn.href = asset.browser_download_url;
      btn.setAttribute('download', asset.name);
      const size = (asset.size / 1048576).toFixed(1);
      const date = new Date(pick.published_at).toLocaleDateString('zh-CN');
      const m = asset.name.match(/latest-(.{7})/);
      if (pick.tag_name === 'latest') {
        title.textContent = '最新 CI 构建';
        meta.textContent = `commit ${m ? m[1] : ''} · ${size} MB · ${date}`;
      } else {
        title.textContent = pick.tag_name;
        meta.textContent = `${size} MB · ${date}`;
      }
    } catch (e) {
      btn.href = FALLBACK;
      title.textContent = '最新构建版';
      meta.textContent = '点击前往 GitHub Releases 下载';
    }
  }
  load();
})();
