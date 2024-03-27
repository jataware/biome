'use client';

import React, { useState } from "react";
import styles from "./page.module.scss";
import { Toolbar } from "primereact/toolbar";
import { Avatar } from "primereact/avatar";
import { InputText } from "primereact/inputtext";

// import Image from "next/image";

import AddSourceDialog from './AddSourceDialog';

import { classNames } from 'primereact/utils';

import Categories from './Categories';
import Sources from './Sources';

export default function Home() {

  const [category, setCategory] = useState({name: 'all', code: 'all'});

  const startContent = (
    <Avatar image="https://primefaces.org/cdn/primevue/images/avatar/amyelsner.png" shape="circle" />
  );

  const centerContent = (
    <span className="p-input-icon-left">
      <i className="pi pi-search" />
      <InputText placeholder="Search" />
    </span>
  );

  return (
    <div className={styles.root}>
      <header>
        <Toolbar
          start={startContent}
          center={centerContent}
          end={AddSourceDialog}
          className={classNames("shadow-4", styles.toolbar)}
        />
      </header>
      <section className={styles.heading}>
        <Avatar className={styles.logo} image="logo.png" shape="circle" size="xlarge"/>
        <h1 className="text-6xl">DataSource Browser</h1>
      </section>
      <div className={styles.apisLayout}>
        <aside className={styles.aside}>
          <Categories 
            selectedCategory={category}
            onCategoryChange={setCategory}
          />
        </aside>
        <main className={styles.main}>
          <Sources category={category} />
        </main>
        <footer className={styles.footer}>
        </footer>
      </div>
    </div>
  );
}
