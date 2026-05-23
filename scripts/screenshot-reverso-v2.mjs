#!/usr/bin/env node
/**
 * Screenshot headless da página /reverso-v2
 * Desktop 1280x720 + Mobile 390x844 (JPEG quality 70)
 * Playwright headless OBRIGATÓRIO
 */

import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { mkdir } from 'fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const OUTPUT_DIR = join(__dirname, '../workspace/output/screenshots-revisao');
const URL = 'http://localhost:4321/reverso-v2';

async function main() {
  // Garantir diretório existe
  await mkdir(OUTPUT_DIR, { recursive: true });

  const browser = await chromium.launch({
    headless: true  // SEMPRE headless (Regra feedback_playwright_sempre_headless.md)
  });

  try {
    // Desktop 1280x720
    const pageDesktop = await browser.newPage({
      viewport: { width: 1280, height: 720 },
      deviceScaleFactor: 1,
    });

    // Desabilitar animações de reveal (evitar falso positivo "página quebrada")
    await pageDesktop.addStyleTag({
      content: `
        .v2-reveal {
          opacity: 1 !important;
          transform: none !important;
          animation: none !important;
        }
      `
    });

    await pageDesktop.goto(URL, { waitUntil: 'networkidle' });
    await pageDesktop.waitForTimeout(1500); // Aguarda Aurora/animações estabilizarem

    const desktopPath = join(OUTPUT_DIR, '2026-05-19-reverso-v2-desktop.jpg');
    await pageDesktop.screenshot({
      path: desktopPath,
      fullPage: true,
      type: 'jpeg',
      quality: 70
    });
    console.log(`✓ Desktop screenshot: ${desktopPath}`);
    await pageDesktop.close();

    // Mobile 390x844
    const pageMobile = await browser.newPage({
      viewport: { width: 390, height: 844 },
      deviceScaleFactor: 2,
      isMobile: true,
      hasTouch: true,
    });

    await pageMobile.addStyleTag({
      content: `
        .v2-reveal {
          opacity: 1 !important;
          transform: none !important;
          animation: none !important;
        }
      `
    });

    await pageMobile.goto(URL, { waitUntil: 'networkidle' });
    await pageMobile.waitForTimeout(1500);

    const mobilePath = join(OUTPUT_DIR, '2026-05-19-reverso-v2-mobile.jpg');
    await pageMobile.screenshot({
      path: mobilePath,
      fullPage: true,
      type: 'jpeg',
      quality: 70
    });
    console.log(`✓ Mobile screenshot: ${mobilePath}`);
    await pageMobile.close();

  } finally {
    await browser.close();
  }

  console.log('\n✅ Screenshots prontos');
  console.log(`📂 ${OUTPUT_DIR}`);
  console.log(`🔗 http://localhost:4321/reverso-v2\n`);
}

main().catch(err => {
  console.error('❌ Erro:', err);
  process.exit(1);
});
