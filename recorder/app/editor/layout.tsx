import React from "react";
import styles from "./editor_layout.module.scss";

export default function ({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className={styles.wrapper}>
      {children}
    </div>
  );
}
