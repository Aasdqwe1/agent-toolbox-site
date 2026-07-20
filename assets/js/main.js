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

// 从同域 release-info.json 读取最新构建信息（由 GitHub Actions 每小时同步）
(function () {
  const FALLBACK = 'https://github.com/Aasdqwe1/agent-toolbox/releases';

  const els = {
    badge: document.getElementById('hero-badge'),
    btn: document.getElementById('dl-btn'),
    stableBtn: document.getElementById('dl-stable-btn'),
    title: document.getElementById('dl-title'),
    meta: document.getElementById('dl-meta'),
    version: document.getElementById('version-value'),
    changelogDesc: document.getElementById('changelog-desc'),
  };
  if (!els.btn) return;

  function fmtDate(iso) {
    try { return new Date(iso).toLocaleDateString('zh-CN'); } catch { return iso; }
  }

  fetch('assets/release-info.json')
    .then((r) => r.json())
    .then((data) => {
      const ci = data && data.ci;
      const stable = data && data.stable;

      if (ci) {
        els.btn.href = ci.download_url;
        els.btn.setAttribute('download', ci.asset_name);
        els.title.textContent = '最新 CI 构建';
        const commit = ci.commit || '';
        els.meta.textContent = `${commit ? 'commit ' + commit + ' · ' : ''}${ci.size_mb} MB · ${fmtDate(ci.published_at)}`;
      } else {
        throw new Error('no ci');
      }

      if (stable) {
        els.stableBtn.href = stable.download_url;
        els.stableBtn.textContent = `下载正式版 ${stable.tag}`;
        if (els.badge) els.badge.textContent = `Android MCP Server · ${stable.tag}`;
        if (els.version) els.version.textContent = stable.tag;
        if (els.changelogDesc) els.changelogDesc.textContent = `当前版本 ${stable.tag}`;
      }
    })
    .catch(() => {
      els.btn.href = FALLBACK;
      els.title.textContent = '最新构建版';
      els.meta.textContent = '点击前往 GitHub Releases 下载';
      if (els.stableBtn) els.stableBtn.href = FALLBACK;
    });
})();
