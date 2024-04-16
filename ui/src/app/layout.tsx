import type { Metadata } from "next";
import { Inter } from "next/font/google"; // TODO ?
import { PrimeReactProvider } from "primereact/api";
import "./globals.css";
// import "primereact/resources/themes/fluent-light/theme.css";

import "primereact/resources/themes/bootstrap4-light-blue/theme.css";
import "primeicons/primeicons.css";
import "primeflex/primeflex.css";

// import Script from 'next/script';
// <Script src="/swagger-editor.js" />

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "DataSource Manager",
  description: "DataSource Manager",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <PrimeReactProvider>
        <body className={inter.className}>
          {children}
        </body>
      </PrimeReactProvider>
    </html>
  );
}

