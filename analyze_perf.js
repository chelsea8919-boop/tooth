const fs = require('fs');
const html = fs.readFileSync('deploy/index.html','utf8');
const styleMatch = html.match(/<style[^>]*>([\s\S]*?)<\/style>/);
if(!styleMatch) { console.log('no style'); process.exit(); }
const css = styleMatch[0];

// Count @keyframes with expensive properties
const lines = css.split('\n');
let currentKf = '';
let layoutThrash = [];
let compositeOnly = [];
let kfNames = [];

for (let i = 0; i < lines.length; i++) {
  const kfMatch = lines[i].match(/@keyframes\s+([\w-]+)/);
  if (kfMatch) {
    currentKf = kfMatch[1];
    kfNames.push(currentKf);
  }
  if (currentKf && lines[i].includes('}')) {
    currentKf = '';
  }
}

// Count animation usages in CSS
const animUsages = css.match(/animation:[^;]+/g) || [];
console.log(`@keyframes count: ${kfNames.length}`);
console.log(`Animation usage count: ${animUsages.length}`);
console.log(`\nKeyframes list:`);
kfNames.forEach((n,i) => console.log(`  ${i+1}. ${n}`));

// Count transition usages
const transUsages = css.match(/transition:[^;]+/g) || [];
console.log(`\nTransition count: ${transUsages.length}`);

// Find will-change
const willChange = css.match(/will-change/g) || [];
console.log(`will-change count: ${willChange.length}`);

// Check for backdrop-filter (very expensive on mobile)
const backdrop = css.match(/backdrop-filter/g) || [];
console.log(`backdrop-filter count: ${backdrop.length}`);

// Check for box-shadow on animated elements
const boxShadow = css.match(/box-shadow/g) || [];
console.log(`box-shadow count: ${boxShadow.length}`);

// Check for filter
const filter = css.match(/filter:/g) || [];
console.log(`filter: count: ${filter.length}`);

// Count blur
const blur = css.match(/blur/g) || [];
console.log(`blur count: ${blur.length}`);

console.log(`\n=== Potential Issues ===`);
if (backdrop.length > 3) console.log(`WARNING: ${backdrop.length} backdrop-filter uses - very expensive on mobile`);
if (filter.length > 5) console.log(`WARNING: ${filter.length} filter uses - GPU intensive`);
if (blur.length > 5) console.log(`WARNING: ${blur.length} blur uses - expensive on mobile`);
if (boxShadow.length > 10) console.log(`WARNING: ${boxShadow.length} box-shadow uses`);
if (willChange.length === 0) console.log(`WARNING: No will-change hints for GPU acceleration`);
