const { AxeBuilder } = require('@axe-core/playwright');
const playwright = require('playwright');
const fs = require('fs');
const csv = require('csv-parse');
const cliProgress = require('cli-progress');

const TIME_STAMP = 'JAN-10-2024';

(async () => {
  const multiBar = new cliProgress.MultiBar();
  const bars = {};

  const files = [
    'gov_pages.csv'
  ];
  
  for(let i = 0; i < files.length; i++) {
    const file = files[i];
    fs.readFile(file, (error, data) => {
      csv.parse(data, { columns: false }, async (error, rows) => {
        bars[i] = multiBar.create(rows.length, 0);

        for (let j = 0; j < rows.length; j++) {
          bars[i].update(j);
          const url = rows[j][0];
          // const { id, page_type, page_id, url } = row;
          const SAVE_PATH = `${TIME_STAMP}/${file.split('_')[0]}/${j}.json`;
          if(fs.existsSync(SAVE_PATH)) continue;
          try {
            const browser = await playwright.chromium.launch({ headless: true });
            const context = await browser.newContext();
            const page = await context.newPage();
            await page.goto(url);
            await page.waitForLoadState('networkidle', { timeout: 10000 });
            const results = await new AxeBuilder({ page }).analyze();
            await browser.close();
            // console.log(results['violations'].length);
            fs.writeFile(SAVE_PATH, JSON.stringify(results), error => {
              // if (error) console.error(error);
            });
          } catch (e) {
            // console.error(e);
          }
        };
      });
    });
  }
  multiBar.stop();
})();