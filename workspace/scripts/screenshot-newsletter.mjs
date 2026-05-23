import { chromium } from 'playwright';
import { readFileSync } from 'fs';

const htmlPath = process.argv[2];
const slug = process.argv[3];

if (!htmlPath || !slug) {
  console.error('Uso: node screenshot-newsletter.mjs <html-path> <slug>');
  process.exit(1);
}

const htmlContent = readFileSync(htmlPath, 'utf-8');

// Wrap em estrutura completa de email
const wrappedHtml = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Newsletter Preview</title>
</head>
<body style="margin:0; padding:32px 16px; background-color:#f5f5f5; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <div style="max-width:600px; margin:0 auto; background-color:#ffffff; padding:32px 24px; border-radius:8px;">
    ${htmlContent}
  </div>
</body>
</html>
`;

(async () => {
  const browser = await chromium.launch({ headless: true });
  
  // Desktop 600px
  const pageDesktop = await browser.newPage({ viewport: { width: 700, height: 800 } });
  await pageDesktop.setContent(wrappedHtml, { waitUntil: 'networkidle' });
  await pageDesktop.screenshot({ 
    path: `/Users/guiavila/Documents/Projetos IA Gui Ávila/Jade - Time Gui Ávila/workspace/output/newsletter/screenshots/${slug}-desktop-600.png`, 
    fullPage: true 
  });
  
  // Mobile 375px
  const pageMobile = await browser.newPage({ viewport: { width: 375, height: 667 } });
  await pageMobile.setContent(wrappedHtml, { waitUntil: 'networkidle' });
  await pageMobile.screenshot({ 
    path: `/Users/guiavila/Documents/Projetos IA Gui Ávila/Jade - Time Gui Ávila/workspace/output/newsletter/screenshots/${slug}-mobile-375.png`, 
    fullPage: true 
  });
  
  await browser.close();
  console.log(`Screenshots salvos:`);
  console.log(`- ${slug}-desktop-600.png`);
  console.log(`- ${slug}-mobile-375.png`);
})();
