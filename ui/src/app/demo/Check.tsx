'use client';

import { useState } from "react";

import { Checkbox } from 'primereact/checkbox';

export function Check() {

  const [checked, setChecked] = useState(false);

  return (
    <div className="">
      <Checkbox
        onChange={e => setChecked(e.checked)}
        checked={checked}
        inputId="ingredient1" name="pizza" value="Cheese"
      />
      <label htmlFor="ingredient1" className="ml-2">Cheese</label>
    </div>
  );
}
