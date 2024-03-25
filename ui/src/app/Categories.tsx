'use client';

import React, { useState } from "react";
import s from './categories.module.scss';
import { ListBox } from 'primereact/listbox';

const Categories = ({selectedCategory, onCategoryChange}) => {

  const cities = [
    { name: 'all', code: 'all' },
    { name: 'lung', code: 'NY' },
    { name: 'pancreas', code: 'RM' },
    { name: 'kidney', code: 'LDN' },
    { name: 'liver', code: 'IST' },
    { name: 'skin', code: 'PRS' },
    { name: 'brain', code: 'PRS' },
    { name: 'thyroid', code: 'PRS' },
    { name: 'bone', code: 'PRS' },
    { name: 'esophageal', code: 'PRS' },
  ];

  return (
    <div className={s.root}>
      <h4>Categories</h4>

      <ListBox
        value={selectedCategory}
        onChange={(e) => onCategoryChange(e.value)}
        options={cities}
        optionLabel="name"
        className={s.listbox}
      />
    </div>
  );
}

export default Categories;
