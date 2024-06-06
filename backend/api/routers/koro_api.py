from fastapi import APIRouter, Request, HTTPException
from typing import Optional

# TODO: Use Replay pydantic model instead of dict
from lib.models import Replay

router = APIRouter(
    prefix="/koro",
    tags=["koro"],
    responses={404: {"description": "Not Found"}}
)

@router.post("/replay_recording")
def replay_recording(
    platform: str,
    action_name: str,
    request: Request,
    parameters: dict = {},
    show_elements: Optional[bool] = False,
    width: int = 1920,
    height: int = 1080,
    experimental_xpath_support: bool = False,
):
    import jobs.koro

    record = koro_records(platform, action_name)

    if record is None:
        return {
            "status": "ERROR",
            "message": f"No koro action record found for this {platform}:{action_name}",
            "data": None,
        }

    job = request.app.state.global_state.job_queue.enqueue_call(
        func=jobs.koro.replay_recording,
        args=[record, parameters, show_elements, (width, height), experimental_xpath_support],
    )
    return {"queued": True, "job_id": job.id}

@router.get("/{platform}/records")
def koro_records(
    platform: str,
    request: Request,
    action_name: Optional[str] = None
):
    
    if action_name:
        must = [
                        {"match": {"platform": platform}},
                        {"match": {"action": action_name}}
                    ]
    else:
        must = [{"match": {"platform": platform}}]

    q = {
        "query":{
            "bool": {
                "must": must
            }
        }
    }

    result = request.app.state.global_state.es.search(index='koro_records', body=q)['hits']['hits']
    if len(result) > 0:
        return [res['_source'] for res in result]

    return None

# TODO: Use Replay pydantic model instead of dict
@router.post("/save_recording")
def koro_save(
    action: dict,
    request: Request
):
    if not ('platform' in action.keys() and 'action' in action.keys()):
        return HTTPException(status_code=400, detail="Invalid koro record provided.")
    
    platform = action['platform']
    action_name = action['action']
    existing = koro_records(platform, request, action_name)

    if existing:
        existing[0]["record"] = action["record"]

        request.app.state.global_state.es.update(index='koro_records', id=f"{platform}_{action_name}", body={'doc': existing[0]})
    else:
        d = action
        request.app.state.global_state.es.index(index='koro_records', id=f"{platform}_{action_name}", body=d)

@router.get("/{platform}/{action_name}/params")
def koro_params(
    platform: str,
    action_name: str,
    request: Request
):
    q = {
        "query":{
            "bool": {
                "must": [
                        {"match": {"platform": platform}},
                        {"match": {"action": action_name}}
                    ]
            }
        }
    } 

    result = request.app.state.global_state.es.search(index='koro_records', body=q)['hits']['hits']
    if len(result) > 0:
        action = result[0]['_source']

        action_params = {}
        for step in action['record']:
            if step['type'] == 'click' and 'params' in step.keys():
                params = step['params'] 
                param = params['name']

                if params['type'] == 'text':
                    action_params[param] = "str"
                elif params['type'] == 'buttons' or params['type'] == 'dropdown':
                    action_params[param] = [p['text'] for p in params['options'].values()]

        return action_params

    return None