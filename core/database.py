from flask_sqlalchemy import SQLAlchemy

class Database(SQLAlchemy):
    _seeds = set()

    def register_seed(self, seed):
        assert callable(seed), "seed parameter must be callable"
        self._seeds.add(seed)
    
    def seed(self):
        for seed in self._seeds:
            seed(self)


db = Database()
