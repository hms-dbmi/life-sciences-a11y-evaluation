const axios = require('axios')
// url = 'https://github.com/sdfsdfdfdsf';
url = 'http://bidd.nus.edu.sg/group/cjttd/'
axios.get(url, {
    signal: AbortSignal.timeout(10000) // Aborts request after 10 seconds
 })
    .catch((error) => {
        console.log(error);
        if (error.response?.status == 404) {
            console.error(`This URL ${url} has 404 page`);
        }
    });