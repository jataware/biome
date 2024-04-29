
Web Recorder. Navigate to a target website, press the "Record" button, and interact with the
web portal to capture interaction events. Once done, Save and proceed to the Review/Editing
step to analyze captured content, create interacted-element screenshots and json metadata needed
to replay the recordings by the Scooter/Koro runner.

## Requirements

- nodejs / npm

## Initial setup

```
npm install
```

## Running

On two different terminals:

Web View
```
npm run dev
```

Electron App
```
npm start
```

## App Overview

`electron.js`, let's call it `main`, contains the main startup program for the electron desktop app. Electron and a desktop app are used to
work around limitations on access cross-domain DOMs when embedding external content that we wish to capture recordings/events from.

`preload.js` is injected js code to the main browser window created by `main`. This gives our "renderer"/"view" content access to `nodejs` and ability to communicate with `main`. Let's call this the `renderer`. This `renderer` will contain the html/css/js app that displays the recorder/editor layout and contains js browser app logic.

`preload-view.js` is injected into a `webview`, which is a child html tag of the `renderer` content. We call it `webview`, although we could come up with other markup-agnostic terms such as target-website-container, "iframe" (different than webview, but more familiar outside the context of electron), or other names to signify that it is a portal to embed a 3rd party website target to record events to.

## Building for Production (electron desktop app)
 TODO
 - Set up isDev/isProd flags
 - Ensure React Editor app is built to known html/js dist/build folder
 - Switch on `main` to decide which editor app to load depending on dev|prod env
 - Run `electron` build command to create executable binaries.
 - Later: Alternate approach to inject a webview electron tag into a local react app (lab).

## TODOs

- Setup to use dev url (localhost React app) on dev, else use built js assets for viewer on prod.
There are some guide on this around, it's a matter of addressing it.
- Build and test by others.
- Configure so running one dev command starts both the react view server and the electron app (couple blog posts on this on the web)
