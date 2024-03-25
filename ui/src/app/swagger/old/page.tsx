'use client';
import SwaggerUI from "swagger-ui-react";
import "swagger-ui-react/swagger-ui.css";

const url="https://petstore.swagger.io/v2/swagger.json";

const Old = () => <SwaggerUI url={url} />

export default Old;
