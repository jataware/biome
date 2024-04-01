'use client';

import React, { useState } from "react";
import s from './categories.module.scss';
import { ListBox } from 'primereact/listbox';

const Categories = ({title, options, selectedCategory, onCategoryChange}) => {

  return (
    <div className={s.root}>
      <h4>{title}</h4>

      <ListBox
        value={selectedCategory}
        onChange={(e) => onCategoryChange(e.value)}
        options={options}
        optionLabel="name"
        className={s.listbox}
      />
    </div>
  );
}

export default Categories;
