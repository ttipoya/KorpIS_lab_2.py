import pandas as pd
from pathlib import Path
from typing import List, Tuple

SUPPORTED = ['.csv', '.xls', '.xlsx']

class DataExtractor:
    def __init__(self, input_dir: str):
        self.input_dir = Path(input_dir)
        self.input_dir.mkdir(parents=True, exist_ok=True)

    def list_files(self) -> List[Path]:
        files = []
        for ext in SUPPORTED:
            files.extend(self.input_dir.glob(f'*{ext}'))
        return files

    def extract(self, file_path: Path) -> Tuple[pd.DataFrame, dict]:
        suffix = file_path.suffix.lower()
        meta = {'source': str(file_path.name)}
        if suffix == '.csv':
            df = pd.read_csv(file_path)
        else:
            xls = pd.read_excel(file_path, sheet_name=None)
            frames = []
            for sheet_name, sheet_df in xls.items():
                sheet_df['__sheet'] = sheet_name
                frames.append(sheet_df)
            df = pd.concat(frames, ignore_index=True)
            meta['sheets'] = list(xls.keys())
        df.columns = [str(c).strip() for c in df.columns]
        df = df.dropna(how='all')
        return df, meta
