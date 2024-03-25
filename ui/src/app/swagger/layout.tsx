

export default function Swagger({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div>
      <h1>SwaggerEditor Integration</h1>
        <section>
          {children}
        </section>
    </div>
  );
}
