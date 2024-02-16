const { AxeBuilder } = require('@axe-core/playwright');
const playwright = require('playwright');
const fs = require('fs');
const csv = require('csv-parse');
const cliProgress = require('cli-progress');

const TIME_STAMP_FOLDER_NAME = 'JAN-10-2024';

(async () => {
  const multiBar = new cliProgress.MultiBar();
  const bars = {};

  const FILES = [
    'data-portal_pages.csv', 
    // 'journal-portal_pages.csv',
    // 'gov_pages.csv',
    // 'nei-data-portal_pages.csv',
    // 'nih-data-portal_pages.csv'
  ];
  
  for(let i = 0; i < FILES.length; i++) {
    const file = `${TIME_STAMP_FOLDER_NAME}/${FILES[i]}`;
    fs.readFile(file, (error, data) => {
      csv.parse(data, { columns: true }, async (error, rows) => {
        bars[i] = multiBar.create(rows.length, 0);
        for (let j = 0; j < rows.length; j++) {
          bars[i].update(j);
          const row = rows[j];
          const { page_id, url, page_type } = row;

          // Let's collect non-home pages only
          if(page_type === 'home') continue;

          // Manually skip pages that are not working with axe-core
          if(page_id === 'nih-24') continue;
          
          const SAVE_PATH = `${file.split('_')[0]}/${page_id}.json`;
          if(fs.existsSync(SAVE_PATH)) continue;
          const SAVE_FAILED_PATH = `${file.split('_')[0]}/${page_id}_failed.json`;
          if(fs.existsSync(SAVE_FAILED_PATH)) continue;          
          const browser = await playwright.chromium.launch({ headless: true });
          try {
            const context = await browser.newContext();
            const page = await context.newPage();
            await page.goto(url);
            await page.waitForLoadState('networkidle', { timeout: 10000 });
            const results = await new AxeBuilder({ page }).analyze();
            fs.writeFile(SAVE_PATH, JSON.stringify(results), error => {
              // if (error) console.error(error);
            });
          } catch (e) {
            fs.writeFile(SAVE_FAILED_PATH, '', error => {});
            // console.error(e);
          }
          await browser.close();
        };
      });
    });
  }
  multiBar.stop();
})();