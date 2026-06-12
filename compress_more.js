const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const imgDir = path.join(__dirname, 'deploy', 'images');
const files = fs.readdirSync(imgDir).filter(f => f.endsWith('.webp'));

(async () => {
  let totalBefore = 0, totalAfter = 0;
  for (const file of files) {
    const fp = path.join(imgDir, file);
    const before = fs.statSync(fp).size;
    totalBefore += before;

    const tmpFile = path.join(imgDir, 'tmp_' + file);
    await sharp(fp)
      .webp({ quality: 50, effort: 6 })
      .toFile(tmpFile);
    
    fs.unlinkSync(fp);
    fs.renameSync(tmpFile, fp);
    const after = fs.statSync(fp).size;
    totalAfter += after;
    console.log(`${file}: ${(before/1024).toFixed(0)}KB -> ${(after/1024).toFixed(0)}KB`);
  }
  console.log(`\nTotal: ${(totalBefore/1024/1024).toFixed(2)}MB -> ${(totalAfter/1024/1024).toFixed(2)}MB (-${((1-totalAfter/totalBefore)*100).toFixed(0)}%)`);
})();
