const fs = require('fs');


// each row of the output table will have
// page_id<string> | issue_id<string> | violations<number> | passes<number>

const table = {};

['data-portal', 'journal-portal'].forEach(d_or_j => {
    fs.readdir(`JAN-10-2024/${d_or_j}`, (error, files) => {
        files.forEach((file, i) => {
            const page_id = file.split('.')[0];
            table[page_id] = {};
            fs.readFile(`JAN-10-2024/${d_or_j}/${file}`, (error, report) => {
                const results = JSON.parse(report);
                ['violations', 'passes'].forEach(v_or_p => {
                    results[v_or_p].forEach(issue => {
                        const { id: issueId, impact, tags, description, help, helpUrl, nodes } = issue;
                        if(impact !== 'critical') return;
                        if(!table[page_id][issueId]) table[page_id][issueId] = {};
                        table[page_id][issueId][v_or_p] = nodes.length;
                    });
                });
    
                /** Save a CSV file */
                let csvContent = ''; // 'page_id,issue_id,violations,passes\n';
                // Object.keys(table).forEach(page => {
                Object.keys(table[page_id]).forEach(issue => {
                    const { violations, passes } = table[page_id][issue];
                    csvContent += `${page_id},${issue},${violations ?? 0},${passes ?? 0}\n`;
                });
                // });
                fs.appendFile(`JAN-10-2024/${d_or_j}_aggregated_results.csv`, csvContent, error => {
                    if(error) console.error(error);
                });
            });
        });
    });
});