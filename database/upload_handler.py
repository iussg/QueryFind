import os
import re
import pandas as pd
from sqlalchemy import create_engine, text

class UploadHandler:
    MAX_SIZE_MB = 50

    def validate_file(self, uploaded_file) -> tuple:
        if uploaded_file is None:
            return False, "No file provided."
        size_mb = uploaded_file.size / (1024 * 1024)
        if size_mb > self.MAX_SIZE_MB:
            return False, f"File too large ({size_mb:.1f}MB). Maximum is {self.MAX_SIZE_MB}MB."
        ext = uploaded_file.name.split('.')[-1].lower()
        if ext not in ['csv', 'db', 'sqlite']:
            return False, "Only .csv, .db, and .sqlite files are supported."
        return True, ""

    def process_csv(self, uploaded_file, session_id: str) -> tuple:
        try:
            db_path = f"database/upload_{session_id}.db"
            df = pd.read_csv(uploaded_file)

            # Clean column names
            df.columns = [re.sub(r'[^a-zA-Z0-9_]', '_', col.strip().lower())
                         for col in df.columns]

            # Clean table name from filename
            table_name = re.sub(r'[^a-zA-Z0-9_]', '_',
                               uploaded_file.name.replace('.csv', '').lower())
            table_name = table_name[:50]

            engine = create_engine(f'sqlite:///{db_path}')
            df.to_sql(table_name, engine, if_exists='replace', index=False)

            return db_path, table_name, df.shape[0], len(df.columns)
        except Exception as e:
            return None, None, 0, 0

    def process_sqlite(self, uploaded_file, session_id: str) -> tuple:
        try:
            db_path = f"database/upload_{session_id}.db"
            with open(db_path, 'wb') as f:
                f.write(uploaded_file.read())

            # Verify it's valid SQLite
            engine = create_engine(f'sqlite:///{db_path}')
            from sqlalchemy import inspect
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            if not tables:
                return None, 0
            return db_path, len(tables)
        except Exception as e:
            return None, 0

    def cleanup(self, session_id: str):
        path = f"database/upload_{session_id}.db"
        if os.path.exists(path):
            os.remove(path)