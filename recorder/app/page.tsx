"use client";
import { useState, useRef, useEffect } from "react";
import Image from "next/image";
import styles from "./page.module.css";
import Link from 'next/link';
import { ButtonGroup } from 'primereact/buttongroup';
import { Button } from "primereact/button";
import { InputText } from "primereact/inputtext"

export default function Home() {

  const webviewRef = useRef(null);

  useEffect(() => {
    console.log('mounted..');
    if (window.eapi) {
      window.eapi.setTitle('Scooter Web Recorder');
    }

    if (webviewRef.current) {
      console.log('webviewRef.current', webviewRef.current);
    }
  }, []);

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
        <nav>
          <Link
            className="p-button font-bold"
            href="/editor">
            Editor
          </Link>
        </nav>

        <br />

        <div>
          <Button onClick={openFile}>
            Select File Demo
          </Button>
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
            value="https://google.com"
          />
        </div>

        <webview
          ref={webviewRef}
          style={{width: "100%", height: "93%", padding: '0', margin: '0'}}
          className="scrollbar"
          autosize="on"
          src="https://www.google.com/"
          id="webview"
        ></webview>
      </div>
    </div>
  );
}
