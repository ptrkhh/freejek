from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
def health_check() -> str:
    return "pong"
