/**
 * This script collects all accessibility issues from a list of URLs using axe-core.
 * This script should be ran first before running the summarize-reports.js script.
 */
const { AxeBuilder } = require('@axe-core/playwright');
const playwright = require('playwright');
const fs = require('fs');
const csv = require('csv-parse');
const cliProgress = require('cli-progress');

/** configure input data */
const TIME_STAMP_FOLDER_NAME = process.argv[2];
if(!TIME_STAMP_FOLDER_NAME) {
  console.error('Please provide a timestamp folder name as an argument.');
  return;
}
const BASE_PATH = `../data/${TIME_STAMP_FOLDER_NAME}`;
const INPUT_FOLDER = `${BASE_PATH}/input`;

(async () => {
  const multiBar = new cliProgress.MultiBar();
  const bars = {};

  /** Get all files in the input folder */
  const FILES = (await fs.readdirSync(INPUT_FOLDER)).filter(file => file.endsWith('.csv'));

  for(let i = 0; i < FILES.length; i++) {

    /** Read a file */
    const file = `${INPUT_FOLDER}/${FILES[i]}`;
    const category = FILES[i].split('.csv')[0];

    fs.readFile(file, (error, data) => {
      csv.parse(data, { columns: true }, async (error, rows) => {
        bars[i] = multiBar.create(rows.length, 0);
        for (let j = 0; j < rows.length; j++) {
          bars[i].update(j+1);

          /** Read a row and fill in missing data */
          const row = rows[j];
          const { url } = row;
          let { page_id, page_type } = row;
          if(!page_id) page_id = `${category}${j}`;
          if(!page_type) page_type = 'unknown';

          const SAVE_FOLDER = `${BASE_PATH}/reports/${category}`;
          if(!fs.existsSync(SAVE_FOLDER)) {
            // If the file does not exist, create one.
            fs.mkdirSync(SAVE_FOLDER, { recursive: true });
          }

          const SAVE_PATH_BASE = `${SAVE_FOLDER}/${page_id}_${page_type}`;
          const SAVE_PATH = `${SAVE_PATH_BASE}.json`;
          if(fs.existsSync(SAVE_PATH)) continue; // This means the report already exists.
          const SAVE_FAILED_PATH = `${SAVE_PATH_BASE}_failed.json`;
          if(fs.existsSync(SAVE_FAILED_PATH)) continue; // This means the report already exists.

          /** Evaluate and save reports */
          const browser = await playwright.chromium.launch({ headless: true });
          try {
            const context = await browser.newContext();
            const page = await context.newPage();
            await page.goto(url, { waitUntil: 'networkidle', timeout: 50000 });
            const results = await new AxeBuilder({ page }).analyze();
            fs.writeFile(SAVE_PATH, JSON.stringify(results), error => {
              if (error) console.error(error);
            });
          } catch (e) {
            fs.writeFile(SAVE_FAILED_PATH, '', error => {});
            console.error(e);
          }
          await browser.close();
        };
      });
    });
  }
  multiBar.stop();
})();
