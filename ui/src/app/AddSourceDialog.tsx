import React, { useState } from "react";
import s from "./add_source.module.scss";
import { Avatar } from "primereact/avatar";
import { InputText } from "primereact/inputtext";

import { Button } from 'primereact/button';

import { Dialog } from 'primereact/dialog';

import { classNames } from 'primereact/utils';

export default function AddSource() {

  const [visible, setVisible] = useState(false);

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
        maximizable
        style={{ width: '50vw', height: '35vh' }}
        className={s.dialogWrapper}
        onHide={() => setVisible(false)}
      >

        <div
          className="flex flex-column align-items-end"
        >

          <div className="inline-flex flex-column gap-2">

            <span className="p-input-icon-left">
              <i className="pi pi-globe" />
              <InputText
                className={s.urlBox}
                placeholder="https://www.data.gov"
              />
            </span>

          </div>
          <div className="flex pt-3">
            <Button
              className={s.confirmSourceButton}
              label="Start Import"
              onClick={(e) => setVisible(false)}
              text
            />
          </div>
        </div>



      </Dialog>
    </div>
  );

}
