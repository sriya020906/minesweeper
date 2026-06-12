let currentBoard = [];
let boardSize = 8;

async function loadBoard() {
    const response = await fetch("/board");
    const data = await response.json();

    currentBoard = data.board;

    boardSize = currentBoard.length;

    document.getElementById("moves").innerText =
        "Moves: " + data.moves;

    renderBoard();

    loadStats();
    loadLeaderboard();
}

function renderBoard() {

    const boardDiv =
        document.getElementById("board");

    boardDiv.innerHTML = "";

    boardDiv.style.gridTemplateColumns =
        `repeat(${boardSize}, 35px)`;

    for (let r = 0; r < boardSize; r++) {

        for (let c = 0; c < boardSize; c++) {

            const cell =
                document.createElement("div");

            cell.className = "cell";

            const value =
                currentBoard[r][c];

            if (value !== "X" && value !== "F") {
                cell.classList.add("revealed");
            }

            if (value === "X") {
                cell.innerText = "";
            }
            else if (value === "F") {
                cell.innerText = "🚩";
            }
            else if (value === "M") {
                cell.innerText = "💣";
            }
            else if (value === 0) {
                cell.innerText = "";
            }
            else {
                cell.innerText = value;
            }

            cell.addEventListener(
                "click",
                () => revealCell(r, c)
            );

            cell.addEventListener(
                "contextmenu",
                (e) => {
                    e.preventDefault();
                    flagCell(r, c);
                }
            );

            boardDiv.appendChild(cell);
        }
    }
}

async function revealCell(row, col) {

    const response = await fetch(
        "/reveal",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                row,
                col
            })
        }
    );

    const data =
        await response.json();

    if (data.board) {

        currentBoard =
            data.board;

        boardSize =
            currentBoard.length;

        renderBoard();
    }

    if (data.moves !== undefined) {
        document.getElementById("moves").innerText =
            "Moves: " + data.moves;
    }

    if (data.status === "win") {

        document.getElementById(
            "message"
        ).innerHTML =
            `<h2>🎉 You Win!</h2>
             <p>Time: ${data.time}s</p>
             <p>Moves: ${data.moves}</p>`;

        loadStats();
        loadLeaderboard();
    }

    if (data.status === "loss") {

        document.getElementById(
            "message"
        ).innerHTML =
            `<h2>💥 Game Over!</h2>
             <p>Time: ${data.time}s</p>
             <p>Moves: ${data.moves}</p>`;

        loadStats();
        loadLeaderboard();
    }
}

async function flagCell(row, col) {

    const response = await fetch(
        "/flag",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                row,
                col
            })
        }
    );

    const data =
        await response.json();

    currentBoard =
        data.board;

    boardSize =
        currentBoard.length;

    renderBoard();
}

async function newGame() {

    document.getElementById(
        "message"
    ).innerHTML = "";

    const difficulty =
        document.getElementById(
            "difficulty"
        ).value;

    const response =
        await fetch(
            "/new-game",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    difficulty
                })
            }
        );

    const data =
        await response.json();

    currentBoard =
        data.board;

    boardSize =
        currentBoard.length;

    document.getElementById(
        "moves"
    ).innerText = "Moves: 0";

    renderBoard();
}

async function loadStats() {

    const response =
        await fetch("/stats");

    const stats =
        await response.json();

    document.getElementById(
        "total_games"
    ).innerText =
        stats.total_games;

    document.getElementById(
        "wins"
    ).innerText =
        stats.wins;

    document.getElementById(
        "losses"
    ).innerText =
        stats.losses;

    document.getElementById(
        "win_percentage"
    ).innerText =
        stats.win_percentage + "%";

    document.getElementById(
        "best_time"
    ).innerText =
        stats.best_time;

    document.getElementById(
        "average_time"
    ).innerText =
        stats.average_time;
}

async function loadLeaderboard() {

    const response =
        await fetch(
            "/leaderboard"
        );

    const leaderboard =
        await response.json();

    const body =
        document.getElementById(
            "leaderboard-body"
        );

    body.innerHTML = "";

    leaderboard.forEach(item => {

        body.innerHTML += `
            <tr>
                <td>${item.difficulty}</td>
                <td>${item.moves}</td>
                <td>${item.time}</td>
            </tr>
        `;
    });
}

loadBoard();