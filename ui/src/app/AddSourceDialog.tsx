import React, { useState, useEffect, useRef } from "react";
import s from "./add_source.module.scss";
import { InputText } from "primereact/inputtext";
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { classNames } from "primereact/utils";
import { ColorPicker } from 'primereact/colorpicker';
import { MultiSelect } from 'primereact/multiselect';
import { Timeline } from 'primereact/timeline';
import { Card } from 'primereact/card';

import { InputTextarea } from 'primereact/inputtextarea';

// import { ProgressSpinner } from 'primereact/progressspinner';

import { Divider } from 'primereact/divider';

import { ScrollPanel } from 'primereact/scrollpanel';

enum Step {
  url = "url",
  scan = "scan",
  review = "review",
  submit = "submit"
}

enum ScanStep {
  inputUri,
  reviewLinks,
  scanningBest,
  generating,
  done
}

const AnimatedTimeline = () => {

  const [loadingScanStep, setLoadingScanStep] = useState(ScanStep.inputUri);

  const rawEvents = [
    {
      status: 'Scanning Input URI',
      date: '10:30',
      color: '#9C27B0',
      // image: 'game-controller.jpg', // TODO?
      index: ScanStep.inputUri
    },
    {
      status: 'Reviewing Links',
      date: '14:00',
      // icon: 'pi pi-cog',
      color: '#673AB7',
      index: ScanStep.reviewLinks
    },
    {
      status: 'Selecting Best Source',
      date: '16:15',
      icon: 'pi pi-shopping-cart',
      color: '#FF9800',
      index: ScanStep.scanningBest
    },
    {
      status: 'Generating Data',
      date: '10:00',
      icon: 'pi pi-check',
      color: '#607D8B',
      index: ScanStep.generating
    }
  ];

  const [events, setEvents] = useState([rawEvents[0]]);

  useEffect(() => {
    const timer = setTimeout(() => {
      setEvents(current => {
        if (current.length > 3) {
          setLoadingScanStep(ScanStep.done);
          return current;
        }

        setLoadingScanStep(loadingScanStep + 1);
        const nextEvent = rawEvents[loadingScanStep + 1];

        return [...current, nextEvent];
      });
    }, 2000);
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

  // These were inside customizeContent: Card
  // {
  //   item.image && <img src={`https://primefaces.org/cdn/primereact/images/product/${item.image}`} alt={item.name} width={200} className="shadow-1" />
  // }
  // <p> Culpa ratione quam perferendis esse.</p>

  const customizedContent = (item) => {
    return (
      <Card
        title={item.status}
        subTitle={item.date}
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



export default function AddSource() {

  const randomColor = "#000000".replace(/0/g, function() { return (~~(Math.random() * 16)).toString(16); });

  const [visible, setVisible] = useState(false);
  const [step, setStep] = useState(Step.url);
  const [color, setColor] = useState(randomColor);
  const [sourceUri, setSourceUri] = useState('');

  const sourceUriInputRef = useRef(null);

  function closeAndReset() {
    setStep(Step.url);
    setVisible(false);
  }

  function gotoScan() {
    // TODO make http request to server to start process
    setSourceUri(sourceUriInputRef.current.value);
    setStep(Step.scan);
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
        closeOnEscape={step === Step.url}
        maximizable
        className={classNames(s.dialogWrapper, s[step])}
        onHide={closeAndReset}
      >
        {step === Step.url && (
          <div
            className="flex flex-column align-items-end"
          >
            <div className="inline-flex flex-column gap-2 w-full">

              <span className="p-input-icon-left">
                <i className="pi pi-globe" />
                <InputText
                  className={s.urlBox}
                  ref={sourceUriInputRef}
                  placeholder="https://www.data.gov"
                />
              </span>

            </div>
            <div className="flex pt-3">
              <Button
                className={s.confirmSourceButton}
                label="Start Import"
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
              <AnimatedTimeline />
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

  // <div>
  //   <label htmlFor="color-picker">Color:&nbsp;</label>
  //   <ColorPicker
  //     id="color-picker"
  //     value={color}
  //     onChange={(e) => setColor(e.value)}
  //   />
  // </div>
