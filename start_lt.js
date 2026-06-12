const fs = require('fs');
const localtunnel = require('C:/Users/Ms.赵/.workbuddy/binaries/node/workspace/node_modules/localtunnel');

const LOG = 'C:/Users/Ms.赵/WorkBuddy/2026-05-29-task-3/tunnel_url.txt';

(async () => {
    try {
        fs.writeFileSync(LOG, 'connecting...');
        const tunnel = await localtunnel({ 
            port: 8080,
            subdomain: 'horsh-bread'
        });
        fs.writeFileSync(LOG, tunnel.url);
        
        setInterval(() => {}, 30000);
        
        tunnel.on('close', () => {
            fs.appendFileSync(LOG, '\nCLOSED');
            process.exit(0);
        });
        
        tunnel.on('error', (err) => {
            fs.appendFileSync(LOG, '\nERROR:' + err.message);
        });
    } catch (err) {
        // If subdomain taken, try without
        fs.appendFileSync(LOG, '\nSUBDOMAIN_FAILED:' + err.message);
        try {
            const tunnel = await localtunnel({ port: 8080 });
            fs.writeFileSync(LOG, tunnel.url);
            setInterval(() => {}, 30000);
        } catch (err2) {
            fs.writeFileSync(LOG, 'FINAL_FAIL:' + err2.message);
        }
    }
})();
