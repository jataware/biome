from fastapi import FastAPI, HTTPException

from .integrations import initialize_adhoc

integrations = initialize_adhoc()
app = FastAPI()


def raise_on_invalid_integration(integration: str) -> None:
    if integration not in [
            integration_data["slug"]
            for (integration_data, _) in integrations.apis.values()
        ]:
        raise HTTPException(status_code=403, detail=f"The requested integration `{integration}` does not exist.")


@app.get("/list_integrations")
def list_integrations() -> dict[str, dict[str, str]]:
    return {
        name: {
            integration_data["slug"]: integration_data["description"]
        } for name, (integration_data, _) in integrations.apis.items()
    }


@app.get("/consult_integration_documentation/{integration}")
def consult_integration_documentation(integration: str, query: str):
    raise_on_invalid_integration(integration)
    try:
        response = integrations.ask_api(integration, query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/draft_integration_code/{integration}")
def draft_integration_code(integration: str, query: str):
    raise_on_invalid_integration(integration)
    try:
        response = integrations.use_api(integration, query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
