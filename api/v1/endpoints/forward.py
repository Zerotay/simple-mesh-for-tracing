from fastapi import APIRouter, Request

router = APIRouter()

@router.api_route("/{full_path:path}", methods=["GET"])
def forward_subpath(full_path: str, request: Request):
    return {
        "method": request.method,
        "path": full_path,
        "headers": dict(request.headers)
    }