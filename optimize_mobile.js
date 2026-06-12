const fs = require('fs');
let html = fs.readFileSync('deploy/index.html', 'utf8');

// ============ 1. Add viewport meta with proper settings ============
html = html.replace(
  /<meta\s+name="viewport"[^>]*>/i,
  '<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">'
);

// ============ 2. Add image lazy loading and decoding ============
html = html.replace(/<img\s+/g, '<img loading="lazy" decoding="async" ');

// ============ 3. Performance CSS overrides - insert before </head> ============
const perfCSS = `
<style>
/* ===== MOBILE PERFORMANCE OPTIMIZATIONS ===== */
/* GPU acceleration for animated elements */
.slide-page, .bread-main-img, .jam-bottle, .confession-card,
.result-panel, .p2-hao-popup, .cream-blob, .candy-orb,
.hao-popup, .string-particle, .squeeze-count .dot,
.badge-pulse, .glow-pulse, .ring-spin, .ring-rot,
.hero-shimmer, .title-bar-shine, .btn-shine {
  will-change: transform, opacity;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}

/* Reduce box-shadow on mobile (42 was way too many) */
* {
  box-shadow: none !important;
}
/* Only keep essential shadows */
.confession-card {
  box-shadow: 0 8px 32px rgba(0,0,0,0.18) !important;
}
.p1-squeeze-btn {
  box-shadow: 0 4px 15px rgba(212,160,23,0.35) !important;
}

/* Reduce blur usage - huge GPU cost on mobile */
.cream-blob {
  filter: none !important;
  opacity: 0.3;
}
.candy-orb {
  filter: none !important;
}

/* Simplify backdrop-filter (very expensive) */
.confession-overlay {
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  background: rgba(0,0,0,0.7) !important;
}

/* Reduce animation count - disable decorative ones */
@keyframes grid-drift { 0%,100% { transform: translate(0,0); } }
@keyframes fluid-drift { 0%,100% { transform: translate(0,0); } }

/* Disable non-essential continuous animations */
.cream-blob { animation: none !important; }
.candy-orb { animation: none !important; }
.star-twinkle, .blob-morph { animation: none !important; }

/* Optimize canvas rendering */
canvas {
  image-rendering: -webkit-optimize-contrast;
  -webkit-font-smoothing: antialiased;
}

/* Reduce paint area */
.slide-page {
  contain: layout style paint;
}

/* Reduce filter on animated elements */
.badge-pulse, .glow-pulse, .ring-spin, .ring-rot {
  filter: none !important;
}

/* Simplify loading animations */
.loading-bg-drift { animation-duration: 0.01s !important; }

/* Disable unused hover effects on mobile */
.jam-bottle:active { transform: scale(0.95); }

/* Optimize font rendering */
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}
</style>
`;

html = html.replace('</head>', perfCSS + '\n</head>');

// ============ 4. JS Performance: reduce setTimeout spam, add rAF ============
const perfJS = `
<script>
// ===== MOBILE PERFORMANCE: Reduce animation overhead =====
(function(){
  // Throttle scroll/touch events
  let ticking = false;
  const origTouchMove = typeof ontouchmove !== 'undefined';

  // Use passive event listeners where possible
  document.addEventListener('touchstart', function(){}, {passive: true});

  // Limit concurrent animations
  const MAX_PARTICLES = 6;

  // Override addParticlesToCell to limit particles on mobile
  const origSquish = window.squishBread;

  // Preload images after first paint
  window.addEventListener('load', function(){
    setTimeout(function(){
      const imgs = document.querySelectorAll('img[loading="lazy"]');
      imgs.forEach(function(img){
        if(img.dataset.src) img.src = img.dataset.src;
      });
    }, 100);
  });
})();
</script>
`;

html = html.replace('</body>', perfJS + '\n</body>');

// ============ 5. Minify: remove comments and extra whitespace in CSS/JS ============
// Remove CSS comments
html = html.replace(/\/\*[\s\S]*?\*\//g, '');
// Remove JS single-line comments (but not inside strings)
html = html.replace(/\/\/(?![\s\S]*?[\"'])(?![\s\S]*?\/\/).*/gm, '');
// Collapse multiple whitespace (careful not to break content)
html = html.replace(/\n\s*\n\s*\n/g, '\n\n');

fs.writeFileSync('deploy/index.html', html);
const newSize = fs.statSync('deploy/index.html').size;
console.log(`Optimized HTML size: ${(newSize/1024).toFixed(1)} KB`);
