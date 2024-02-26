const fs = require('fs');

const TIME_STAMP_FOLDER_NAME = 'JAN-10-2024';

(async () => {
    const issues = {}; // list of issues
    [
        // 'data-portal',
        // 'journal-portal', 
        // 'gov',
        // 'nei-data-portal',
        // 'nih-data-portal',
        'harvard-data-portal'
    ].forEach(async category => {
        const a11yResults = {};
        const files = await fs.readdirSync(`${TIME_STAMP_FOLDER_NAME}/reports/${category}`);
        await files.filter(d => !d.includes('failed')).forEach(async file => {
            const page_id = file.split('.')[0];
            a11yResults[page_id] = {};
            const report = await fs.readFileSync(`${TIME_STAMP_FOLDER_NAME}/reports/${category}/${file}`);
            const results = JSON.parse(report);
            ['violations', 'passes'].forEach(v_or_p => {
                results[v_or_p].forEach(issue => {
                    const { id: issueId, impact, tags, description, help, helpUrl, nodes } = issue;
                    if(!issues[issueId]) issues[issueId] = { impact, description, help, helpUrl };
                    if(!a11yResults[page_id][issueId]) a11yResults[page_id][issueId] = {};
                    a11yResults[page_id][issueId][v_or_p] = nodes.length;
                });
            });
        });
        /** Save CSV files */
        let csvContent = '';
        await Object.keys(a11yResults).forEach(page_id => {
            Object.keys(a11yResults[page_id]).forEach(issue => {
                const { violations, passes } = a11yResults[page_id][issue];
                csvContent += `${page_id},${issue},${violations ?? 0},${passes ?? 0}\n`;
            });
        });
        fs.writeFileSync(`${TIME_STAMP_FOLDER_NAME}/${category}_a11y_results.csv`, csvContent, error => {
            if(error) console.error(error);
        });
        let issuesContent = '';
        await Object.keys(issues).forEach(issueId => {
            const { impact, description, help, helpUrl } = issues[issueId];
            issuesContent += `${issueId},${impact},"${description}"\n`;
        });
        fs.writeFileSync(`${TIME_STAMP_FOLDER_NAME}/${category}_a11y_issues.csv`, issuesContent, error => {
            if(error) console.error(error);
        });
    });
})();