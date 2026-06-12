from fastapi import FastAPI
from fastapi import Request
from fastapi import Depends
from fastapi import Body

from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from database import engine
from database import get_db

from models import Base
from models import GameResult

from game import create_board
from game import reveal_cell
from game import reveal_all_mines
from game import toggle_flag
from game import check_win
from game import get_visible_board

import time

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


game_state = {
    "board": None,
    "difficulty": "easy",
    "moves": 0,
    "start_time": time.time(),
    "game_over": False
}


def start_new_game(difficulty="easy"):
    game_state["board"] = create_board(difficulty)
    game_state["difficulty"] = difficulty
    game_state["moves"] = 0
    game_state["start_time"] = time.time()
    game_state["game_over"] = False


start_new_game()


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.post("/new-game")
def new_game(data: dict = Body(...)):
    difficulty = data.get("difficulty", "easy")

    start_new_game(difficulty)

    return {
        "board": get_visible_board(game_state["board"])
    }


@app.get("/board")
def board():
    return {
        "board": get_visible_board(game_state["board"]),
        "moves": game_state["moves"]
    }


@app.post("/flag")
def flag(data: dict = Body(...)):
    row = data["row"]
    col = data["col"]

    toggle_flag(
        game_state["board"],
        row,
        col
    )

    return {
        "board": get_visible_board(game_state["board"])
    }


@app.post("/reveal")
def reveal(
    data: dict = Body(...),
    db: Session = Depends(get_db)
):
    if game_state["game_over"]:
        return {
            "message": "Game already finished"
        }

    row = data["row"]
    col = data["col"]

    board = game_state["board"]

    game_state["moves"] += 1

    cell = board[row][col]

    if cell["mine"]:

        reveal_all_mines(board)

        elapsed = round(
            time.time() - game_state["start_time"],
            2
        )

        result = GameResult(
            difficulty=game_state["difficulty"],
            result="loss",
            moves=game_state["moves"],
            completion_time=elapsed
        )

        db.add(result)
        db.commit()

        game_state["game_over"] = True

        return {
            "status": "loss",
            "board": get_visible_board(board),
            "moves": game_state["moves"],
            "time": elapsed
        }

    reveal_cell(board, row, col)

    if check_win(board):

        elapsed = round(
            time.time() - game_state["start_time"],
            2
        )

        result = GameResult(
            difficulty=game_state["difficulty"],
            result="win",
            moves=game_state["moves"],
            completion_time=elapsed
        )

        db.add(result)
        db.commit()

        game_state["game_over"] = True

        return {
            "status": "win",
            "board": get_visible_board(board),
            "moves": game_state["moves"],
            "time": elapsed
        }

    return {
        "status": "playing",
        "board": get_visible_board(board),
        "moves": game_state["moves"]
    }


@app.get("/stats")
def stats(db: Session = Depends(get_db)):
    games = db.query(GameResult).all()

    total_games = len(games)

    wins = len(
        [g for g in games if g.result == "win"]
    )

    losses = len(
        [g for g in games if g.result == "loss"]
    )

    win_percentage = 0

    if total_games:
        win_percentage = round(
            (wins / total_games) * 100,
            2
        )

    win_times = [
        g.completion_time
        for g in games
        if g.result == "win"
    ]

    best_time = min(win_times) if win_times else 0

    average_time = (
        round(
            sum(win_times) / len(win_times),
            2
        )
        if win_times
        else 0
    )

    return {
        "total_games": total_games,
        "wins": wins,
        "losses": losses,
        "win_percentage": win_percentage,
        "best_time": best_time,
        "average_time": average_time
    }


@app.get("/leaderboard")
def leaderboard(
    db: Session = Depends(get_db)
):
    results = (
        db.query(GameResult)
        .filter(GameResult.result == "win")
        .order_by(GameResult.completion_time.asc())
        .limit(10)
        .all()
    )

    return [
        {
            "difficulty": r.difficulty,
            "moves": r.moves,
            "time": r.completion_time
        }
        for r in results
    ]