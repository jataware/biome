import React, { useState, useEffect, useRef } from "react";
import s from "./add_source.module.scss";
import { InputText } from "primereact/inputtext";
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { classNames } from "primereact/utils";
// import { ColorPicker } from 'primereact/colorpicker';
// import { MultiSelect } from 'primereact/multiselect';
import { Timeline } from 'primereact/timeline';
import { Card } from 'primereact/card';

import { InputTextarea } from 'primereact/inputtextarea';

// import { ProgressSpinner } from 'primereact/progressspinner';

import { Divider } from 'primereact/divider';

import { ScrollPanel } from 'primereact/scrollpanel';

enum Step {
  queue = "queue",
  url = "url",
  scan = "scan",
  review = "review",
  submit = "submit"
}

enum ScanStep {
  queue,
  url,
  logo,
  api,
  docs,
  generating, 
  done
}

const AnimatedTimeline = ({onDone}) => {

  const [loadingScanStep, setLoadingScanStep] = useState(ScanStep.queue);

  const rawEvents = [
    {
      status: 'Queueing Scan',
      date: '10:00',
      color: '#FF9800',

      // image: 'game-controller.jpg', // TODO?
      index: ScanStep.queue
    },
    {
      status: 'Scanning initial URL',
      date: '14:00',
      // icon: 'pi pi-cog',
      color: '#9C27B0',
      index: ScanStep.url
    },
    {
      status: 'Fetching logo',
      date: '16:00',
      // icon: 'pi pi-shopping-cart',
      color: '#9C27B0',
      index: ScanStep.logo
    },
    {
      status: 'Fetching API specification',
      date: '18:00',
      // icon: 'pi pi-check',
      color: '#9C27B0',
      index: ScanStep.api
    },
    {
      status: 'Fetching documentation',
      date: '20:00',
      // icon: 'pi pi-check',
      color: '#9C27B0',
      index: ScanStep.docs
    },
    {
      status: 'Generating data source',
      date: '22:00',
      // icon: 'pi pi-check',
      color: '#607D8B',
      index: ScanStep.generating
    }    
  ];

  const [events, setEvents] = useState([rawEvents[0]]);

  useEffect(() => {
    const timer = setTimeout(() => {
      setEvents(current => {
        if (current.length >= 6) {
          setLoadingScanStep(ScanStep.done);
          onDone();
          return current;
        }

        setLoadingScanStep(loadingScanStep + 1);
        const nextEvent = rawEvents[loadingScanStep + 1];

        return [...current, nextEvent];
      });
    }, 20000);
    return () => {
      clearTimeout(timer);
    }
  }, [loadingScanStep]);

  const customizedMarker = (item) => {
    return (
      <span
        className="flex w-2rem h-2rem align-items-center justify-content-center text-white border-circle z-1 shadow-1"
        style={{ backgroundColor: item.color }}
      >
        <i className={item.index === loadingScanStep ? 'pi pi-spin pi-spinner' : 'pi pi-check'}></i>
      </span>
    );
  };

  const customizedContent = (item) => {
    return (
      <Card
        title={item.status}
      >
      </Card>
    );
  };

  return (
    <div className="card relative h-full">
      <ScrollPanel className={s.scroller}>
        <Timeline
          value={events}
          align="alternate"
          className={s.customizedTimeline}
          marker={customizedMarker}
          content={customizedContent}
        />
      </ScrollPanel>
    </div>
  );
}

function makeid(length) {
  let result = '';
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const charactersLength = characters.length;
  let counter = 0;
  while (counter < length) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
  }
  return result;
}

export default function AddSource({onRegisterDone}) {

  const randomColor = "#000000".replace(/0/g, function() { return (~~(Math.random() * 16)).toString(16); });

  const [visible, setVisible] = useState(false);
  const [step, setStep] = useState(Step.queue);
  // const [color, setColor] = useState(randomColor);
  const [sourceUri, setSourceUri] = useState('');

  // const sourceUriInputRef = useRef(null);

  function closeAndReset() {
    setStep(Step.queue);
    setVisible(false);
  }

  function onRegisterSourceDone() {
    onRegisterDone();
    closeAndReset();
  }

  function gotoScan() {
    fetch('http://localhost:8001/api/scan', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify([{
        uris: [sourceUri],
        name: makeid(5)
      }])
    }).then(response => {
      if (response.ok) {
        return response.json();
      }
    }).then(data => {
      if (data.queued) {
        console.log('data queued successfully!');
        setStep(Step.scan);
      } else {
        console.log('Error check logs');
      }
    }).catch(err => {
      console.log('Error queueing job scan:', err);
    });
  }

  return (
    <div className="card flex justify-content-center">

      <Button
        className={s.addSourceButton}
        label="Add Source"
        icon="pi pi-globe"
        onClick={() => setVisible(true)}
      />

      <Dialog
        header="Add New Source"
        modal={false}
        visible={visible}
        closeOnEscape={step === Step.queue}
        maximizable
        className={classNames(s.dialogWrapper, s[step])}
        onHide={closeAndReset}
      >
        {step === Step.queue && (
          <div
            className="flex flex-column align-items-end"
          >
            <div className="inline-flex flex-column gap-2 w-full">

              <span className="p-input-icon-left">
                <i className="pi pi-globe" />
                <InputText
                  className={s.urlBox}
                  onChange={e => setSourceUri(e.target.value)}
                  value={sourceUri}
                  placeholder="https://www.data.gov"
                />
              </span>

            </div>
            <div className="flex pt-3">
              <Button
                className={s.confirmSourceButton}
                label="Start Import"
                disabled={!sourceUri}
                onClick={gotoScan}
                text
              />
            </div>
          </div>
        )}

        {/* TODO step individual component */}
        {step === Step.scan && (
          <div className={s.scanRoot}>

            <div className={s.scanLeftPane}>
              <AnimatedTimeline onDone={onRegisterSourceDone} />
            </div>

            <Divider layout="vertical" />

            <div className={s.scanRightPane}>

              <h5>Source: {sourceUri}</h5>

              <div className={s.scanRightContents}>
                <div className="flex flex-column gap-1">
                  <label htmlFor="name">Name</label>
                  <InputText id="name" aria-describedby="name-help" />
                  <small id="name-help">
                    Enter the organization name
                  </small>
                </div>

                <div className="flex flex-column gap-1">
                  <label htmlFor="initials">Initials</label>
                  <InputText id="initials" aria-describedby="initials-help" />
                  <small id="initials-help">
                    Organization Initials. Example: GDC
                  </small>
                </div>

                <span className="flex flex-column gap-1 p-float-label">
                  <InputTextarea
                    rows={2}
                    autoResize
                    id="description"
                    aria-describedby="description-help"
                  />
                  <label htmlFor="description">Description</label>
                  <small id="description-help">
                    Sentence or paragraph describing the data source.
                  </small>
                </span>

                <div className="flex flex-column gap-1">
                  <label htmlFor="logo-url">Logo URL</label>
                  <InputText id="logo-url" aria-describedby="logo-url-help" />
                  <small id="logo-url-help">
                    URL of Logo
                  </small>
                </div>

              </div> {/*scanRightContents*/}

            </div> {/*scanRightPane*/}

          </div>
        )}
      </Dialog>
    </div>
  );

}
