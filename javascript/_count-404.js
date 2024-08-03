const fs = require('fs');
const files = fs.readdirSync('../data/08-01-2024/results/data-portal');
console.log(
  files,
  files.filter(file => file.includes('404')).length
);
