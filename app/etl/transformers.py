from typing import Tuple
import pandas as pd
from .validators import DataValidator

class DataTransformer:
    def __init__(self):
        self.validator = DataValidator()

    def normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        mapping = {
            'first_name': 'first_name', 'firstname': 'first_name', 'first name': 'first_name',
            'last_name': 'last_name', 'lastname':'last_name', 'last name':'last_name',
            'email':'email', 'e-mail':'email',
            'rating':'rating',
            'phone':'phone_number','phone_number':'phone_number','phone number':'phone_number',
            'dob':'date_of_birth','date_of_birth':'date_of_birth','date of birth':'date_of_birth'
        }
        new_cols = {}
        for c in df.columns:
            key = c.strip().lower()
            new_cols[c] = mapping.get(key, key)
        df = df.rename(columns=new_cols)
        return df

    def transform_players(self, df) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df = self.normalize_columns(df)
        required = ['first_name','last_name','email']
        valid_rows = []
        invalid_rows = []
        for _, row in df.iterrows():
            errors = []
            r = row.to_dict()
            if 'first_name' in r and isinstance(r['first_name'], str):
                r['first_name'] = r['first_name'].strip()
            if 'last_name' in r and isinstance(r['last_name'], str):
                r['last_name'] = r['last_name'].strip()
            for col in required:
                if not r.get(col):
                    errors.append(f'{col} is required')
            if 'email' in r and not self.validator.validate_email(r.get('email')):
                errors.append('invalid email')
            if 'phone_number' in r and r.get('phone_number') and not self.validator.validate_phone(r.get('phone_number')):
                errors.append('invalid phone')
            if 'date_of_birth' in r and r.get('date_of_birth') and not self.validator.validate_date(str(r.get('date_of_birth'))):
                errors.append('invalid date_of_birth')
            if 'rating' in r and r.get('rating') is not None:
                try:
                    r['rating'] = int(r['rating'])
                    if r['rating'] < 0:
                        errors.append('rating must be non-negative')
                except Exception:
                    errors.append('rating must be integer')
            if errors:
                r['_errors'] = '; '.join(errors)
                invalid_rows.append(r)
            else:
                valid_rows.append(r)
        valid_df = pd.DataFrame(valid_rows)
        invalid_df = pd.DataFrame(invalid_rows)
        return valid_df, invalid_df
