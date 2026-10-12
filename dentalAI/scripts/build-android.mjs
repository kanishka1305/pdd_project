// Builds the Android debug APK: android/app/build/outputs/apk/debug/app-debug.apk
import { spawnSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const android = join(dirname(fileURLToPath(import.meta.url)), '..', 'android');
const windows = process.platform === 'win32';
// Full path: some shells do not run programs from the current folder
const gradlew = join(android, windows ? 'gradlew.bat' : 'gradlew');
const run = spawnSync(windows ? `"${gradlew}"` : gradlew, ['assembleDebug', ...process.argv.slice(2)],
                      { cwd: android, stdio: 'inherit', shell: windows });
process.exit(run.status ?? 1);
