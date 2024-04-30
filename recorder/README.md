
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

## Running for Development

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

1. Build react webapp: `npm run build-web`
2. Copy electron assets to `webapp` dist folder: `npm run build-electron`
3. Create electron packages: `npm run package`

## TODOs

- Build and test by others.
- Configure so running one dev command starts both the react view server and the electron app (couple blog posts on this on the web)
- Able to include node_modules links in final version of prod/packaged app.
 - Later: Alternate approach to inject a webview electron tag into a local react app (lab).
