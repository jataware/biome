"use client";
import React, { useState, useEffect } from "react";
import Image from "next/image";
import Link from 'next/link';

import { InputText } from 'primereact/inputtext';
import { classNames } from 'primereact/utils';
import { InputTextarea } from 'primereact/inputtextarea';
import { FloatLabel } from "primereact/floatlabel";
import { Card } from 'primereact/card';
import { Checkbox } from 'primereact/checkbox';
import { ButtonGroup } from 'primereact/buttongroup';
import { Button } from 'primereact/button';


import styles from "./editor_page.module.scss";


function StepRow({step, index}) {

  const [checked, setChecked] = useState(true);

  return (
    <Card
      className={styles.stepCard}
    >
      <div className={styles.cardBody}>
        <Checkbox
          className={styles.cardCheckbox}
          onChange={e => setChecked(e.checked)}
          checked={checked}
        />

        <div className={styles.cardDetails}>
          <h2>
            <span>{`${index}.`}</span>&nbsp;
            {`${step.type}`}
          </h2>

          <div>
            <div className={styles.cardScreenshot}>
              <img src={step.image} height={40} />
            </div>

          </div>
        </div>

        <div className={styles.actions}>
          {/* <h4>Actions</h4> */}
          <ButtonGroup>
            <Button
              onClick={() => {console.log('clicked'); }}
              text label="Debug" severity="success" />
            <Button
              onClick={() => {alert('hi')}}
              text label="Retake" severity="warning" />
            {Boolean(step.params?.length) && (
              <Button text label="Params" severity="primary" />
            )}
          </ButtonGroup>
        </div>

      </div>

    </Card>
  );
}

const steps = [
  {
    name: "",
    type: "click",
    image: "controls/sign-in.png",
    params: [],
    description: "",
    selected: true,
  },
  {
    name: "",
    type: "scroll",
    image: "controls/email.png",
    params: [],
    description: "",
    selected: true,
  },
  {
    name: "",
    type: "click",
    image: "controls/share.png",
    params: [{image: "controls/view-source.png"}],
    description: "",
    selected: true,
  },
];

export default function(props) {
  const [taskDescription, setTaskDescription] = useState('');

  useEffect(() => {
    if (window.eapi) {
      window.eapi.setTitle('Scooter Web Recorder: Editor');
    }

  }, []);

  function goToRecorder() {
    console.log('go to recorder clicked', window.eapi);
    if (window.eapi) {
      window.eapi.goToRecorder();
    }
  }

  return (
    <div className={styles.wrapper}>
      <nav>
        <Button
          onClick={goToRecorder}
          className={styles.backLink}
          icon="pi pi-angle-left"
          label="Back"
        />
      </nav>

      <br />

      <div className={styles.heading}>
        <h1>
          <span className={styles.taskPre}>Task:</span>&nbsp;
          <span className={styles.taskName}>Download Cart from GDC Case ID C3L-01355</span>
        </h1>
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

      <div className={styles.steps}>

        <h2>Review Recording Steps</h2>

        <section className={styles.stepsHeaderRow}>
          <h4>
            Keep?
          </h4>
          <h4>
            &nbsp;
            Properties
          </h4>
          <h4>
            Actions
          </h4>
        </section>

        <div className={styles.stepList}>
        <div>
          {steps.map((step, idx) => (
            <StepRow
              key={`${step.name}-${step.type}-${idx}`}
              step={step}
              index={idx}
            />
          ))}
        </div>
        </div>
      </div>

    </div>
  );
}
