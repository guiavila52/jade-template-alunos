import { chromium } from 'playwright';
import { writeFileSync, mkdirSync } from 'fs';
import { dirname } from 'path';

const url = 'http://localhost:4321/reverso-v2';
const outputDir = '/Users/guiavila/Documents/Projetos IA Gui Ávila/Jade - Time Gui Ávila/workspace/output/screenshots-revisao';

const shots = [
  { name: 'reverso-v2-desktop-light-FIXED', width: 1280, height: 720, theme: 'light' },
  { name: 'reverso-v2-mobile-light-FIXED', width: 390, height: 844, theme: 'light' },
  { name: 'reverso-v2-desktop-dark-FIXED', width: 1280, height: 720, theme: 'dark' },
  { name: 'reverso-v2-mobile-dark-FIXED', width: 390, height: 844, theme: 'dark' },
];

const browser = await chromium.launch({ headless: true });

for (const shot of shots) {
  const context = await browser.newContext({
    viewport: { width: shot.width, height: shot.height },
    deviceScaleFactor: 1,
    colorScheme: shot.theme,
  });

  const page = await context.newPage();

  // Forçar tema antes de carregar a página
  await page.addInitScript((theme) => {
    localStorage.setItem('v2-theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
  }, shot.theme);

  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);

  // Forçar tema novamente após carregamento
  await page.evaluate((theme) => {
    document.documentElement.setAttribute('data-theme', theme);
  }, shot.theme);

  // Desabilitar animations (memória feedback_revisor_desabilitar_animacoes_reveal.md)
  await page.addStyleTag({ content: `
    *, *::before, *::after {
      animation-duration: 0s !important;
      animation-delay: 0s !important;
      transition-duration: 0s !important;
    }
    .v2-reveal {
      opacity: 1 !important;
      transform: translateY(0) !important;
    }
  ` });

  await page.waitForTimeout(200);

  const path = `${outputDir}/${shot.name}.jpg`;
  mkdirSync(dirname(path), { recursive: true });
  
  await page.screenshot({
    path,
    type: 'jpeg',
    quality: 70,
    fullPage: true,
  });

  console.log(`✓ ${shot.name}.jpg`);
  await context.close();
}

await browser.close();
