import random

DIFFICULTIES = {
    "easy": {
        "size": 8,
        "mines": 10
    },
    "medium": {
        "size": 12,
        "mines": 25
    },
    "hard": {
        "size": 16,
        "mines": 40
    }
}


def create_board(difficulty="easy"):
    config = DIFFICULTIES[difficulty]

    size = config["size"]
    mines = config["mines"]

    board = []

    for r in range(size):
        row = []

        for c in range(size):
            row.append({
                "mine": False,
                "revealed": False,
                "flagged": False,
                "count": 0
            })

        board.append(row)

    placed = 0

    while placed < mines:
        r = random.randint(0, size - 1)
        c = random.randint(0, size - 1)

        if not board[r][c]["mine"]:
            board[r][c]["mine"] = True
            placed += 1

    calculate_numbers(board)

    return board


def calculate_numbers(board):
    size = len(board)

    for r in range(size):
        for c in range(size):

            if board[r][c]["mine"]:
                continue

            count = 0

            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:

                    if dr == 0 and dc == 0:
                        continue

                    nr = r + dr
                    nc = c + dc

                    if (
                        0 <= nr < size and
                        0 <= nc < size and
                        board[nr][nc]["mine"]
                    ):
                        count += 1

            board[r][c]["count"] = count


def reveal_cell(board, row, col):
    size = len(board)

    if not (0 <= row < size and 0 <= col < size):
        return

    cell = board[row][col]

    if cell["revealed"]:
        return

    if cell["flagged"]:
        return

    cell["revealed"] = True

    if cell["count"] != 0:
        return

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:

            if dr == 0 and dc == 0:
                continue

            nr = row + dr
            nc = col + dc

            if 0 <= nr < size and 0 <= nc < size:
                reveal_cell(board, nr, nc)


def toggle_flag(board, row, col):
    cell = board[row][col]

    if cell["revealed"]:
        return

    cell["flagged"] = not cell["flagged"]


def reveal_all_mines(board):
    size = len(board)

    for r in range(size):
        for c in range(size):
            if board[r][c]["mine"]:
                board[r][c]["revealed"] = True


def check_win(board):
    size = len(board)

    for r in range(size):
        for c in range(size):

            cell = board[r][c]

            if not cell["mine"] and not cell["revealed"]:
                return False

    return True


def get_visible_board(board):
    size = len(board)

    visible = []

    for r in range(size):
        row = []

        for c in range(size):
            cell = board[r][c]

            if cell["flagged"]:
                row.append("F")

            elif not cell["revealed"]:
                row.append("X")

            elif cell["mine"]:
                row.append("M")

            else:
                row.append(cell["count"])

        visible.append(row)

    return visible