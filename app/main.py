# -*- coding: utf-8 -*-
# Create Time: 02/22 2022
# Author: Yunquan (Clooney) Gu
import sqlalchemy.exc
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app.db import database
from app.models.schema import Player

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['0.0.0.0'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], )

db = database()


@app.on_event("startup")
async def start_up():
    await db.begin()


@app.post("/api/v1/player", status_code=200)
async def create_new_player(*, player: Player):
    logger.info(f"[Request] Create new player - [{player.username}]")
    try:
        new_player = await db.create_new_player(username=player.username)
        return JSONResponse(
            {
                "username": new_player.username,
                "player_id": new_player.player_id
            },
            status_code=200)
    except Exception as e:
        logger.exception(e)
        return JSONResponse({"error_message": "Some kind of unspecified error has occurred!"},
                            status_code=400)


@app.get("/api/player/{player_id}/")
async def retrieve(player_id: str):
    logger.info(f"[Request] Retrieve player with id [{player_id}]")
    try:
        player = await db.retrieve(id=player_id)
        return JSONResponse(
            {
                "username": player.username,
                "player_id": player.player_id,
                "xp": player.xp,
                "gold": player.gold
            },
            status_code=200)
    except sqlalchemy.exc.NoResultFound:
        return JSONResponse({"error_message": "No such a player!"},
                            status_code=400)
    except Exception as e:
        logger.exception(e)
        return JSONResponse({"error_message": "Some kind of unspecified error has occurred!"},
                            status_code=400)


@app.put("/api/player/{player_id}/", status_code=200)
async def update_item(player_id: str, updated_player: Player):
    logger.info(f"[Request] Update player with id [{player_id}] to [{updated_player}]")
    updated_player.player_id = player_id
    try:
        if await db.update(id=player_id, updated_player=updated_player):
            player = await db.retrieve(id=player_id)
            return JSONResponse(player.dict(),
                                status_code=200)
        else:
            return JSONResponse(
                {"error_message": "No such a player"},
                status_code=400)
    except Exception as e:
        logger.exception(e)
        return JSONResponse({"error_message": "Some kind of unspecified error has occurred!"},
                            status_code=400)

@app.get("/api/leaderboards")
async def get_top_k(sortby:str, size: int):
    if sortby not in ["gold", "xp"]:
        return JSONResponse({"error_message": "Wrong option! use [gold] or [xp]"},
                            status_code=400)
    results = await db.topk(sortby, size)
    return JSONResponse([i.dict() for i in results],
                        status_code=200)
