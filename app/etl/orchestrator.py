import logging
from pathlib import Path
from .extractors import DataExtractor
from .transformers import DataTransformer
from .loaders import DataLoader

logger = logging.getLogger('etl')

class ETLOrchestrator:
    def __init__(self, input_dir='data/input', output_dir='data/output', processed_dir='data/processed', errors_dir='data/errors', db_session=None):
        self.extractor = DataExtractor(input_dir)
        self.transformer = DataTransformer()
        self.loader = DataLoader(db_session=db_session, output_dir=output_dir, errors_dir=errors_dir)
        self.processed_dir = Path(processed_dir)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def run_players(self):
        files = self.extractor.list_files()
        if not files:
            logger.info('No input files found')
            return {'processed':0,'created':0,'errors':0}
        total_created = 0
        total_errors = 0
        for f in files:
            logger.info(f'Processing {f}')
            df, meta = self.extractor.extract(f)
            valid_df, invalid_df = self.transformer.transform_players(df)
            created = 0
            if not valid_df.empty:
                records = valid_df.to_dict(orient='records')
                created = self.loader.bulk_insert_players(records)
                total_created += created
            if not invalid_df.empty:
                self.loader.save_errors(invalid_df, f.stem)
                total_errors += len(invalid_df)
            try:
                dest = self.processed_dir / f.name
                f.rename(dest)
            except Exception:
                logger.exception('Failed to move processed file')
        return {'processed': len(files), 'created': total_created, 'errors': total_errors}
