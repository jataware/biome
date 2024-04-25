"use client";
import React, { useState } from "react";
import Image from "next/image";
import styles from "./editor_page.module.scss";
import { InputText } from 'primereact/inputtext';
import { classNames } from 'primereact/utils';
import { InputTextarea } from 'primereact/inputtextarea';
import { FloatLabel } from "primereact/floatlabel";
import { Card } from 'primereact/card';
import Link from 'next/link';

function StepRow({step, index}) {
  return (
    <div>
      <div>
        Check
      </div>
      <h4>
        <span>
          {index}
        </span>
        <span>
          Event: {step.type}
        </span>
      </h4>
      <div>
      </div>
    </div>
  );
}

const steps = [
  {
    name: "",
    type: "click",
    image: "",
    params: [],
    description: "",
    selected: true,
  },
  {
    name: "",
    type: "scroll",
    image: "",
    params: [],
    description: "",
    selected: true,
  },
  {
    name: "",
    type: "click",
    image: "",
    params: [],
    description: "",
    selected: true,
  },
];

export default function(props) {
  const [taskDescription, setTaskDescription] = useState('');
  return (
    <div className={styles.wrapper}>
      <nav>
        <Link
          className="p-button font-bold"
          style={{color: "white"}}
          href="/"
        >
          Back
        </Link>
      </nav>

      <br />

      <div className={styles.heading}>
        <h2>
          Task: Task Download Cart from GDC Case ID C3L-01355
        </h2>
      </div>


      <div className={styles.description}>
        <div className="flex flex-column gap-2">
          <label htmlFor="description">Description</label>
          <InputTextarea
            id="description"
            autoResize
            value={taskDescription}
            onChange={(e) => setTaskDescription(e.target.value)}
            rows={4}
            cols={60}
          />
        </div>
      </div>

      <br />

      <div className={styles.center}>
        <h3>Review Recording Steps</h3>
        {steps.map((step, idx) => (
          <StepRow
            key={`${step.name}-${step.type}-${idx}`}
            step={step}
            index={idx}
          />
        ))}
      </div>

    </div>
  );
}
