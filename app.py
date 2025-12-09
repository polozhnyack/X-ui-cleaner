from fastapi import FastAPI, HTTPException, Header, Request
from pydantic import BaseModel
from cleaner import XUIcleaner
from config import DB_PATH, API_TOKEN



class DeleteRequest(BaseModel):
    identifier: str


class DeleteResponse(BaseModel):
    status: str
    uuid: str | None = None
    email: str | None = None
    inbounds_deleted: int | None = None
    tables_deleted: dict | None = None



app = FastAPI(
    title="XUI Cleaner Service",
    version="1.0.0"
)

cleaner = XUIcleaner(DB_PATH)


def check_api_key(x_api_key: str | None):
    if x_api_key != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API key")


@app.get("/")
async def root(request: Request):
    return {"status": "ok"}


@app.delete("/deleteclient", response_model=DeleteResponse)
async def delete_client(
    data: DeleteRequest,
    x_api_key: str | None = Header(default=None)
):
    check_api_key(x_api_key)

    result = cleaner.delete_client(data.identifier)

    if result["status"] == "not_found":
        raise HTTPException(status_code=404, detail="Client not found")

    return result