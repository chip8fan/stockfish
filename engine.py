import chess.engine
import sys
import random
class Stockfish():
    def convert(self, score: chess.engine.Cp):
        if "#" not in str(score):
            return int(str(score))
        else:
            mate_count = int(str(score).replace("#", ""))
            if mate_count < 0:
                return -100000
            elif mate_count > 0:
                return 100000
    def play(self, board: chess.Board, time_limit: float, cp_loss: int):
        engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
        high_score = engine.analyse(board, chess.engine.Limit(time=time_limit))["score"]
        scores = []
        max_score = -sys.maxsize
        if high_score.is_mate() == False:
            for move in board.legal_moves:
                board.push(move)
                score = self.convert(-engine.analyse(board, chess.engine.Limit(time=time_limit))["score"].relative)
                if score is not None:
                    if score > max_score:
                        max_score = score
                    scores.append([move, score])
                board.pop()
            engine.quit()
            best_moves = []
            for move in scores:
                if move[1] > max_score-cp_loss:
                    best_moves.append(move[0])
            return random.choice(best_moves)
        else:
            best_moves = []
            for move in board.legal_moves:
                board.push(move)
                evaluation = self.convert(-engine.analyse(board, chess.engine.Limit(time=time_limit))["score"].relative)
                if evaluation == 100000:
                    best_moves.append(move)
                board.pop()
            engine.quit()
            if len(best_moves) == 0:
                return random.choice(list(board.legal_moves))
            return random.choice(best_moves)