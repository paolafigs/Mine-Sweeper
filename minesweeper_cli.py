import random

class Minesweeper:
    def __init__(self, rows=8, cols=8, mines=10):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[' ' for _ in range(cols)] for _ in range(rows)]
        self.visible = [[False for _ in range(cols)] for _ in range(rows)]
        self.mine_locations = set()
        self._place_mines()
        self._calculate_numbers()
        self.game_over = False
        self.win = False

    def _place_mines(self):
        while len(self.mine_locations) < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            self.mine_locations.add((r, c))

    def _calculate_numbers(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.mine_locations:
                    self.board[r][c] = 'M'
                else:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                                if (nr, nc) in self.mine_locations:
                                    count += 1
                    self.board[r][c] = str(count) if count > 0 else ' '

    def print_board(self, reveal=False):
        print('   ' + ' '.join(str(i) for i in range(self.cols)))
        print('  +' + '--' * self.cols + '+')
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                if reveal or self.visible[r][c]:
                    row.append(self.board[r][c])
                else:
                    row.append('.')
            print(f'{r} |' + ' '.join(row) + '|')
        print('  +' + '--' * self.cols + '+')

    def reveal(self, r, c):
        if self.visible[r][c]:
            return
        self.visible[r][c] = True
        if (r, c) in self.mine_locations:
            self.game_over = True
            return
        if self.board[r][c] == ' ':
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if not self.visible[nr][nc]:
                            self.reveal(nr, nc)

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.mine_locations and not self.visible[r][c]:
                    return False
        self.win = True
        return True

def play():
    game = Minesweeper()
    while not game.game_over and not game.win:
        game.print_board()
        try:
            move = input('Enter row and column (e.g., 3 4): ')
            r, c = map(int, move.strip().split())
            if not (0 <= r < game.rows and 0 <= c < game.cols):
                print('Invalid coordinates.')
                continue
            game.reveal(r, c)
            if game.check_win():
                break
        except Exception as e:
            print('Invalid input. Please enter two numbers separated by a space.')
    if game.win:
        print('Congratulations! You win!')
    else:
        print('Game over! You hit a mine!')
        game.print_board(reveal=True)

if __name__ == '__main__':
    play()
