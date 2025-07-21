#rl_agent.py
import pickle

from sqlalchemy.orm import Session


class BanditAgent:
    def __init__(self):
        self.Q = {}  # lesson_id -> Q-value

    def recommend(self):
        # Recommend lesson with lowest mastery
        return min(self.Q, key=self.Q.get)

    def update(self, lesson_id, reward, alpha=0.1):
        if lesson_id not in self.Q:
            self.Q[lesson_id] = 0
        self.Q[lesson_id] += alpha * (reward - self.Q[lesson_id])

    def save(self, path="qtable.pkl"):
        with open(path, "wb") as f:
            pickle.dump(self.Q, f)

    def load(self, path="qtable.pkl"):
        with open(path, "rb") as f:
            self.Q = pickle.load(f)


# Hàm helper
def load_model(version: str, db: Session, agent: BanditAgent):
    from models import RLModel  # Đảm bảo import RLModel
    model = db.query(RLModel).filter(RLModel.Version == version).first()
    if not model:
        raise ValueError(f"Model version {version} not found")
    agent.load(model.FilePath)