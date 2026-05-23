const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  console.log('Navegando para /reverso...');
  await page.goto('http://localhost:4321/reverso/');
  await page.waitForLoadState('networkidle');
  
  // Verificar o HTML da logo
  const logoHref = await page.evaluate(() => {
    const brand = document.querySelector('.v2-header__brand');
    return brand ? brand.getAttribute('href') : null;
  });
  console.log(`Logo href no DOM: "${logoHref}"`);
  
  // Scroll down
  console.log('Scroll down para 800px...');
  await page.evaluate(() => window.scrollTo(0, 800));
  await page.waitForTimeout(500);
  
  const scrollBeforeClick = await page.evaluate(() => window.scrollY);
  console.log(`ScrollY antes do clique: ${scrollBeforeClick}`);
  
  // Clicar na logo
  console.log('Clicando na logo...');
  await page.click('.v2-header__brand');
  await page.waitForTimeout(800);
  
  // Verificar resultado
  const urlAfter = page.url();
  const scrollAfter = await page.evaluate(() => window.scrollY);
  
  console.log(`URL após clique: ${urlAfter}`);
  console.log(`ScrollY após clique: ${scrollAfter}`);
  
  // Critério de aprovação
  const urlOk = urlAfter.includes('/reverso');
  const scrollOk = scrollAfter < 100;
  
  console.log('\n--- RESULTADO ---');
  console.log(`URL permaneceu em /reverso? ${urlOk ? 'SIM' : 'NÃO'}`);
  console.log(`Scroll voltou ao topo? ${scrollOk ? 'SIM' : 'NÃO'}`);
  console.log(`VEREDICTO: ${urlOk && scrollOk ? 'APROVADO' : 'REPROVADO'}`);
  
  await browser.close();
})();
