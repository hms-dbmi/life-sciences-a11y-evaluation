/**
 * This script collects all accessibility issues from a list of URLs using axe-core.
 * This script should be ran first before running the summarize-reports.js script.
 */
const { AxeBuilder } = require('@axe-core/playwright');
const playwright = require('playwright');
const fs = require('fs');
const csv = require('csv-parse');
const cliProgress = require('cli-progress');
const axios = require('axios');

/** configure input data */
const TIME_STAMP_FOLDER_NAME = process.argv[2];
if (!TIME_STAMP_FOLDER_NAME) {
  console.error('Please provide a timestamp folder name as an argument.');
  return;
}
const basePath = `../data/${TIME_STAMP_FOLDER_NAME}`;
const inputFolder = `${basePath}/input`;
const outputFolder = `${basePath}/results`;

(async () => {
  // const multiBar = new cliProgress.MultiBar();
  // const bars = {};

  /**
   * Folder names under the input folder correspond to resource categories.
   * For example, URLs found under the `data_portal` folder are set to `data_portal` category.
   */
  const resourceCategories = (await fs.readdirSync(inputFolder)).filter(file => !file.includes('.'));
  for (let rc = 0; rc < resourceCategories.length; rc++) {

    const resource_category = resourceCategories[rc];
    /** Get all files in the input folder */
    const categoryFolder = `${inputFolder}/${resource_category}`;
    const files = (await fs.readdirSync(categoryFolder)).filter(file => file.endsWith('.csv'));
    for (let i = 0; i < files.length; i++) {

      /** Read a file */
      const file = `${categoryFolder}/${files[i]}`;
      // const category = FILES[i].split('.csv')[0];

      let notYetPrintedStartProgree = true;

      fs.readFile(file, (error, data) => {
        csv.parse(data, { columns: true }, async (error, rows) => {
          // bars[i] = multiBar.create(rows.length, 0);
          for (let j = 0; j < rows.length; j++) {
            // bars[i].update(j+1);

            /** Read a row and fill in missing data */
            const row = rows[j];
            const { url } = row;

            if ([
              'https://uspis.gov',
              'https://cb.imsc.res.in/imppat',
              'http://memprotmd.bioch.ox.ac.uk',
              'http://www.ijo.cn/gjyken/ch/index.aspx',
              'http://www.medbc.com/annals/',
              'http://www.lifespanjournal.it/',
              'http://www.cjrm.ca/',
              'http://xuebao.bjmu.edu.cn/EN/1671-167X/home.shtml',
              'http://ytlx.whrsm.ac.cn/EN/1000-7598/home.shtml'
            ].indexOf(url) !== -1) continue;

            let { website_id, page_id, page_type } = row;
            if (!website_id) website_id = `${resource_category}-row-${j}`;
            if (!page_type) page_type = 'unknown';

            const SAVE_FOLDER = `${outputFolder}/${resource_category}`;
            if (!fs.existsSync(SAVE_FOLDER)) {
              // If the file does not exist, create one.
              fs.mkdirSync(SAVE_FOLDER, { recursive: true });
            }

            const savePathBase = `${SAVE_FOLDER}/${website_id}_${page_id}_${page_type}`;
            const savePath = `${savePathBase}.json`;
            if (fs.existsSync(savePath)) continue; // This means the report already exists.
            const savePathFailedFile = `${savePathBase}_failed.json`;
            if (fs.existsSync(savePathFailedFile)) continue; // This means the report already exists.
            const savePath404File = `${savePathBase}_failed_by_404.json`;
            if (fs.existsSync(savePath404File)) continue; // This means the report already exists.

            if (notYetPrintedStartProgree) {
              console.log(`[${file}] ${(j / rows.length * 100).toPrecision(4)}% at ${url}`);
              notYetPrintedStartProgree = false;
            }

            /** Check if the website is working or not */
            try {
              await axios.get(url, {
                signal: AbortSignal.timeout(10000) // Aborts request after 10 seconds
              });
            } catch (error) {
              if (error.response?.status == 404) {
                console.error(`[${(j / rows.length * 100).toPrecision(4)}] This URL ${url} has the 404 page.`);
                fs.writeFile(savePath404File, '404', error => { });
              } else {
                fs.writeFile(savePathFailedFile, `${error.response?.status}`, error => { });
              }
              continue;
            }

            /** Evaluate and save reports */
            const browser = await playwright.chromium.launch({ headless: true });
            try {
              const context = await browser.newContext();
              const page = await context.newPage();
              await page.goto(url, { waitUntil: 'networkidle', timeout: 10000 });
              const results = await new AxeBuilder({ page }).analyze();
              fs.writeFile(savePath, JSON.stringify(results), error => {
                if (error) console.error(error);
              });
            } catch (e) {
              fs.writeFile(savePathFailedFile, '', error => { });
              console.error(website_id, url, e);
            }
            await browser.close();
          };
        });
      });
    }
  }
  // multiBar.stop();
})();
