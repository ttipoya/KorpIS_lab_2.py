from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal
from pathlib import Path

BATCH = 200

class DataLoader:
    def __init__(self, db_session: Optional[Session]=None, output_dir: str='data/output', errors_dir: str='data/errors'):
        self.db_session = db_session
        self.output_dir = Path(output_dir)
        self.errors_dir = Path(errors_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.errors_dir.mkdir(parents=True, exist_ok=True)

    def bulk_insert_players(self, records: List[Dict[str, Any]]):
        db = self.db_session or SessionLocal()
        created = 0
        try:
            for i in range(0, len(records), BATCH):
                chunk = records[i:i+BATCH]
                objs = []
                for r in chunk:
                    obj = models.Player(
                        first_name=r.get('first_name'),
                        last_name=r.get('last_name'),
                        email=r.get('email'),
                        rating=r.get('rating') if r.get('rating') is not None else None
                    )
                    objs.append(obj)
                db.add_all(objs)
                db.commit()
                created += len(objs)
            return created
        except Exception:
            db.rollback()
            raise
        finally:
            if self.db_session is None:
                db.close()

    def save_errors(self, invalid_df, source_name: str):
        if invalid_df is None or invalid_df.empty:
            return None
        csv_path = self.errors_dir / f"errors_{source_name}.csv"
        json_path = self.errors_dir / f"errors_{source_name}.json"
        invalid_df.to_csv(csv_path, index=False)
        invalid_df.to_json(json_path, orient='records', force_ascii=False)
        return csv_path, json_path
