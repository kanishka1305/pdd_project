// Builds the app's local pages into www/ and records the server address. Run by `npm run sync`.
//   DENTAI_SERVER_URL=https://dental-ai.example.com npm run sync
// The pages are self-contained (logo and server address inlined): on Android the offline
// page is shown on the server's address, so relative files next to it cannot be loaded.
import { mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const serverFile = join(root, 'server.json');
const fromEnv = process.env.DENTAI_SERVER_URL;
const url = (fromEnv || JSON.parse(readFileSync(serverFile, 'utf8')).url).trim().replace(/\/+$/, '');

let parsed;
try { parsed = new URL(url); } catch { throw new Error(`DENTAI_SERVER_URL is not a valid address: ${url}`); }
if (!['http:', 'https:'].includes(parsed.protocol)) throw new Error('The server address must start with http:// or https://');
if (parsed.protocol === 'http:' && !/^(localhost|127\.0\.0\.1|10\.0\.2\.2|192\.168\.|10\.|172\.(1[6-9]|2\d|3[01])\.)/.test(parsed.hostname)) {
  console.warn(`Warning: ${url} is not https. Use https for any server outside a local test network.`);
}

writeFileSync(serverFile, JSON.stringify({ url }, null, 2) + '\n');
const www = join(root, 'www');
rmSync(www, { recursive: true, force: true });
mkdirSync(www, { recursive: true });
const logo = 'data:image/png;base64,' + readFileSync(join(root, 'branding', 'logo-full.png')).toString('base64');
for (const page of ['index.html', 'offline.html']) {
  const html = readFileSync(join(root, 'web-src', page), 'utf8')
    // the parsed address has no quotes or angle brackets left (they are percent-encoded)
    .replaceAll('"__DENTAI_SERVER_URL__"', JSON.stringify(parsed.href.replace(/[/]+$/, '')))
    .replaceAll('__DENTAI_LOGO__', logo);
  writeFileSync(join(www, page), html);
}
console.log(`Dental AI app → ${url}`);
