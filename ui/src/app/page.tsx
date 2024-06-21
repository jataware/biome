'use client';

import React, { useState, useEffect } from "react";
import styles from "./page.module.scss";
import { Toolbar } from "primereact/toolbar";
import { Avatar } from "primereact/avatar";
import { InputText } from "primereact/inputtext";
import { Panel } from 'primereact/panel';

import { Checkbox } from "primereact/checkbox";
// import Image from "next/image";

import AddSourceDialog from './AddSourceDialog';

import { classNames } from 'primereact/utils';

import Categories from './Categories';
import Sources from './Sources';

const AccessControlFilters = ({ }) => {

  const categories = [
    { name: 'open', key: 'open' },
    { name: 'controlled', key: 'controlled' },
  ];

  const [selectedCategories, setSelectedCategories] = useState([categories[1]]);

  const onCategoryChange = (e) => {
    let _selectedCategories = [...selectedCategories];

    if (e.checked)
      _selectedCategories.push(e.value);
    else
      _selectedCategories = _selectedCategories.filter(category => category.key !== e.value.key);

    setSelectedCategories(_selectedCategories);
  };

  return (
    <div className={styles.accessFilters}>
      <h4>Access</h4>
      <div className="flex flex-column gap-1">
        {categories.map((category) => {
          return (
            <div key={category.key} className="flex align-items-center">
              <Checkbox inputId={category.key} name="category" value={category} onChange={onCategoryChange} checked={selectedCategories.some((item) => item.key === category.key)} />
              <label htmlFor={category.key} className="ml-2">
                {category.name}
              </label>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default function Home() {

  const [category, setCategory] = useState({ name: 'all', code: 'all' });

  const [sourceList, setSourceList] = useState([]);
    
  function fetchSources() {
    fetch('/api/sources')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        // console.log('data', data.sources);
        setSourceList(data.sources);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }

  function searchSources(query) {
    if (query === '') {
      fetchSources();
    } else {
      const params = new URLSearchParams({ query }).toString();
      fetch('/api/sources?' + params, {
        method: 'GET',
      })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          setSourceList(data);
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    }
  }

  useEffect(() => {
    fetchSources();
  }, []);


  const startContent = (
    <Avatar shape="circle" />
  );

  const centerContent = (
    <span className="p-input-icon-left">
      <i className="pi pi-search" />
      <InputText placeholder="Search" onChange={(e) => searchSources(e.target.value)} />
    </span>
  );

  return (
    <div className={styles.root}>
      <header>
        <Toolbar
          start={startContent}
          center={centerContent}
          end={() => (<AddSourceDialog onRegisterDone={fetchSources} />)}
          className={classNames("shadow-4", styles.toolbar)}
        />
      </header>
      <section className={styles.heading}>
        <Avatar className={styles.logo} image="logo.png" shape="circle" size="xlarge" />
        <h1 className="text-6xl">DataSource Manager</h1>
      </section>
      <div className={styles.apisLayout}>
        <aside className={styles.aside}>
          <Categories
            title="Categories"
            options={[
              { name: 'all', code: 'all' },
              { name: 'genomics', code: 'genomics' },
              { name: 'imaging', code: 'imaging' }
            ]}
            selectedCategory={category}
            onCategoryChange={setCategory}
          />

          <Categories
            title="Data Types"
            options={[
              { name: 'all', code: 'all' },
              { name: 'Proteogenomics', code: 'proteogenomics' },
              { name: 'molecular', code: 'molecular' },
              { name: 'clinical', code: 'clinical' }
            ]}
            selectedCategory={category}
            onCategoryChange={setCategory}
          />

          <AccessControlFilters />

        </aside>
        <main className={styles.main}>
            <Sources 
              category={category} 
              sources={sourceList} 
              onSourceClick={(source) => {
                setSelectedSource(source);
                setIsDrawerOpen(true);
              }}
            />
        </main>
        {/* <footer className={styles.footer}>
        </footer> */}
      </div>
    </div>
  );
}
