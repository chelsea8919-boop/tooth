const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'deploy', 'images');
const outDir = path.join(__dirname, 'deploy', 'images2');
fs.mkdirSync(outDir, {recursive: true});

const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.webp'));

(async () => {
  let totalBefore = 0, totalAfter = 0;
  for (const file of files) {
    const fp = path.join(srcDir, file);
    const before = fs.statSync(fp).size;
    totalBefore += before;

    await sharp(fp)
      .webp({ quality: 50, effort: 6 })
      .toFile(path.join(outDir, file));
    
    const after = fs.statSync(path.join(outDir, file)).size;
    totalAfter += after;
    console.log(`${file}: ${(before/1024).toFixed(0)}KB -> ${(after/1024).toFixed(0)}KB`);
  }
  console.log(`\nTotal: ${(totalBefore/1024/1024).toFixed(2)}MB -> ${(totalAfter/1024/1024).toFixed(2)}MB (-${((1-totalAfter/totalBefore)*100).toFixed(0)}%)`);
})();
