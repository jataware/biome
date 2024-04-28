"use client";
import { useState, useRef, useEffect } from "react";
import Image from "next/image";
import styles from "./page.module.scss";
import Link from 'next/link';
import { ButtonGroup } from 'primereact/buttongroup';
import { Button } from "primereact/button";
import { InputText } from "primereact/inputtext"

export default function Home() {

  const webviewRef = useRef(null);

  const [webSource, setWebSource] = useState("https://hello.com");

  const searchBoxRef = useRef(null);

  useEffect(() => {
    console.log('mounted..');
    if (window.eapi) {
      window.eapi.setTitle('Scooter Web Recorder');
    }

  }, []);

  function handleSearchBarKey(event) {
    if (event.key === "Enter") {
      console.log('pressed enter');
      navigateToPage(searchBoxRef.current.value);
    }
  }

  function navigateToPage(value) {
    const urlPattern = /(\w+:?\w*)?(\S+)(:\d+)?(\/|\/([\w#!:.?+=&%!\-\/]))?/;

    if (urlPattern.test(value)) {
      if (value.startsWith("http")) {
        setWebSource(value);
      } else {
        setWebSource(`https://${value}`);
      }
    }
    // TODO else http invalid- show an error, dont nav?
    // or perform a web search instead?
  }

  function debug() {
    console.log('debug');
    // window.eapi.inspectWebView();
    // window.eapi.clientSetWebView(webviewRef.current);
    // const retrieved = window.eapi.getWebView();
    // console.log('eapi get web view res', retrieved);

    if (webviewRef.current) {
      const view = webviewRef.current;
      console.log('webviewRef.current', view);
      // console.log(view.window);
      // console.log('parent', view.parent) // undefined
      console.log('view keys', Object.keys(view))
      const win = view.contentWindow;
      console.log('win?', win)
      // cross-origin frame kicks in:
      console.log('doc?', win.document)
    }
  }

  const pingpong = async () => {
    // NOTE eapi doesnt have to catch all properties
    const response = await window.eapi.ping();
    console.log(response) // prints out 'pong'
  };

  async function openFile() {
    pingpong();
    const filepath = await window.eapi.openFile();
    console.log('file path', filepath);
  }

  return (
    <div className={styles.wrapper}>

      <main className={styles.main}>
        {/*Koro log-like widget*/}

        <h4>Events</h4>

        {/* TODO */}
        <div className={styles.logs}>
        </div>

        <br />

        <nav className={styles.nav}>
          <Link
            className="p-button"
            style={{textDecoration: "none"}}
            href="/editor">
            Editor
          </Link>
          <Button label="Save" />
        </nav>

        <div className={styles.miscDebug}>
          <section>
            <Button outlined onClick={openFile}>
              Select File Demo
            </Button>
            <Button text label="Debug" onClick={debug}/>
          </section>
        </div>

      </main>

      {/*Browser webview area*/}
      <div className={styles.browser}>

        {/*Navigation Row*/}
        <div className={styles.browserNav}>

          <ButtonGroup>
            {/*Back Button*/}
            <Button icon="pi pi-chevron-left" />

            {/*Forward Button*/}
            <Button icon="pi pi-chevron-right" />

            {/*Reload Button*/}
            <Button icon="pi pi-refresh" />
          </ButtonGroup>

          &nbsp;

          {/*URL Input*/}
          <InputText
            variant="filled"
            onKeyPress={handleSearchBarKey}
            ref={searchBoxRef}
            placeholder={webSource}
          />

        </div>

        <webview
          ref={webviewRef}
          style={{width: "100%", height: "93%", padding: '0', margin: '0'}}
          className="scrollbar"
          autosize="on"
          src={webSource}
          id="webview"
          disablewebsecurity="true"
          webpreferences="allowRunningInsecureContent"
        ></webview>
      </div>
    </div>
  );
}
