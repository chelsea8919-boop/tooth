const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const imgDir = path.join(__dirname, 'deploy', 'images');
const files = fs.readdirSync(imgDir).filter(f => f.endsWith('.png'));

(async () => {
  let totalBefore = 0, totalAfter = 0;
  for (const file of files) {
    const fp = path.join(imgDir, file);
    const before = fs.statSync(fp).size;
    totalBefore += before;

    // Convert PNG to WebP with quality 70 (much smaller, good quality)
    const outPath = fp.replace('.png', '.webp');
    await sharp(fp)
      .webp({ quality: 70, effort: 4 })
      .toFile(outPath);

    const after = fs.statSync(outPath).size;
    totalAfter += after;
    const ratio = ((1 - after/before) * 100).toFixed(0);
    console.log(`${file}: ${(before/1024).toFixed(0)}KB -> ${(after/1024).toFixed(0)}KB (-${ratio}%)`);
  }
  console.log(`\nTotal: ${(totalBefore/1024/1024).toFixed(2)}MB -> ${(totalAfter/1024/1024).toFixed(2)}MB (-${((1-totalAfter/totalBefore)*100).toFixed(0)}%)`);
})();
