import React, { useState, useEffect } from "react";
import { InputText } from 'primereact/inputtext';
import { classNames } from 'primereact/utils';
import { InputTextarea } from 'primereact/inputtextarea';
import { FloatLabel } from "primereact/floatlabel";
import { Card } from 'primereact/card';
import { Checkbox } from 'primereact/checkbox';
import { ButtonGroup } from 'primereact/buttongroup';
import { Button } from 'primereact/button';


import "./Editor.scss";


function StepRow({step, index}) {

  const [checked, setChecked] = useState(true);

  return (
    <Card
      className="stepCard"
    >
      <div className="cardBody">
        <Checkbox
          className="cardCheckbox"
          onChange={e => setChecked(e.checked)}
          checked={checked}
        />

        <div className="cardDetails">
          <h2>
            <span>{`${index}.`}</span>&nbsp;
            {`${step.type}`}
          </h2>

          <div>
            <div className="cardScreenshot">
              <img src={step.image} height={40} />
            </div>

          </div>
        </div>

        <div className="actions">
          <ButtonGroup>
            <Button
              onClick={() => {console.log('clicked'); }}
              text label="Debug" severity="success" />
            <Button
              onClick={() => {alert('hi')}}
              text label="Retake" severity="warning" />
            {Boolean(step.params?.length) && (
              <Button text label="Params" />
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

declare global {
  interface Window {
    eapi:any;
  }
}

export default function Editor(props) {
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
    <div className="wrapper">
      <nav>
        <Button
          onClick={goToRecorder}
          className="backLink"
          icon="pi pi-angle-left"
          label="Back"
        />
      </nav>

      <br />

      <div className="heading">
        <h1>
          <span className="taskPre">Task:</span>&nbsp;
          <span className="taskName">Download Cart from GDC Case ID C3L-01355</span>
        </h1>
      </div>

      <div className="description">
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

      <div className="steps">

        <h2>Review Recording Steps</h2>

        <section className="stepsHeaderRow">
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

        <div className="stepList">
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
