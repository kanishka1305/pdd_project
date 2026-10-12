# Dental AI — iOS and Android app

The Dental AI web application as a native app for iPhone, iPad and Android, built with
[Capacitor 8](https://capacitorjs.com). The app opens the Dental AI web application from your
Dental AI server (the FastAPI app in `../PDD-main`), so every feature, fix and model update on
the server reaches the app at once — nothing is duplicated here.

What the app adds on top of the web pages:

- **Downloads that work on a phone** — the colour DICOM, the ZIP package, STL, CSV and viewer
  screenshots are saved on the device and the share sheet opens (Save to Files, Drive, email,
  a DICOM viewer app). The web pages call `saveFile()` / `downloadUrl()` from
  `../PDD-main/app/static/js/app.js`, which do this in the app and a normal download in a browser.
- **An offline screen** (`web-src/offline.html`) when the server cannot be reached, with *Try again*
  and an automatic retry when the connection returns. `npm run sync` builds the app's local pages
  from `web-src/` into `www/` with the logo and server address built in (`www/` is generated).
- **The Android back button**, the app icon and the splash screen from the Dental AI logo.

## Requirements

| | |
|---|---|
| Both | Node.js 22 or newer, then `npm install` in this folder |
| Android | Android Studio (with its JDK 21) and the Android SDK 36 |
| iOS | A Mac with Xcode 26 (iOS apps can only be built on macOS) |

## Point the app at your Dental AI server

The server address is kept in `server.json`. Set it and update both native projects with:

```bash
DENTAI_SERVER_URL=https://dental-ai.your-clinic.com npm run sync
```

Use an **https** address for any real use (the App Store requires it). Plain http is only for
testing on your own computer or local network.

## Run it

**Android emulator** (this computer runs the server on port 8000; the emulator reaches it as `10.0.2.2`):

```bash
npm run sync:android-emulator
npm run open:android
```

Then press *Run* in Android Studio.

**Android phone on the same Wi-Fi** — start the server so the network can reach it
(`uvicorn app.main:app --host 0.0.0.0 --port 8000`), then use this computer's IP address:

```bash
DENTAI_SERVER_URL=http://192.168.1.20:8000 npm run sync
```

**Debug APK** (install it on any Android phone):

```bash
npm run build:android
```

The APK is `android/app/build/outputs/apk/debug/app-debug.apk`.

**iOS** — on a Mac, in this folder:

```bash
npm install
npm run sync:ios-simulator
npm run open:ios
```

In Xcode choose your team under *Signing & Capabilities*, pick a simulator or iPhone, and press *Run*.

## Release to the stores

- **Google Play:** Android Studio → *Build → Generate Signed App Bundle*, then upload the `.aab`.
- **App Store:** Xcode → *Product → Archive*, then *Distribute App*. The server address must be https.

App ID: `io.automiz.dentalai` (in `capacitor.config.js`; change it before the first store upload if needed).

## Change the icon or splash screen

Replace `branding/logo-mark.png` (the tooth) and `branding/logo-full.png` (with the name), then:

```bash
npm run icons
```

A 1024 px or larger original of the logo gives the sharpest store icons.
