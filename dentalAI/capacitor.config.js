// Dental AI for iOS and Android (Capacitor).
//
// The app opens the Dental AI web application from your Dental AI server, so every
// feature, fix and model update on the server reaches the app at once. The server
// address lives in server.json; set it with:  DENTAI_SERVER_URL=https://… npm run sync
const fs = require('fs');
const path = require('path');

const { url } = JSON.parse(fs.readFileSync(path.join(__dirname, 'server.json'), 'utf8'));

/** @type {import('@capacitor/cli').CapacitorConfig} */
module.exports = {
  appId: 'io.automiz.dentalai',
  appName: 'Dental AI',
  webDir: 'www',
  backgroundColor: '#f8fbfe',
  appendUserAgent: 'DentalAIApp/1.0',
  server: {
    url,
    cleartext: url.startsWith('http://'),   // only for a local test server; use https in production
    errorPath: 'offline.html',              // shown when the server cannot be reached
  },
  android: {
    allowMixedContent: false,
  },
  ios: {
    contentInset: 'always',                 // keep pages clear of the notch and status bar
  },
  plugins: {
    SplashScreen: {
      launchShowDuration: 1200,
      launchAutoHide: true,
      backgroundColor: '#ffffff',
      showSpinner: false,
      androidScaleType: 'CENTER_INSIDE',
    },
    SystemBars: {
      insetsHandling: 'css',                // pages stay clear of the Android status and navigation bars
      style: 'LIGHT',
    },
  },
};
