import pandas as pd
import os
from pathlib import Path as p

os.stat

cur_dir = p.cwd()

output_dir = cur_dir / "output_files"

files_by_pattern = output_dir.glob('output_file_*')

newest_file = max(files_by_pattern, key=lambda f: f.stat().st_mtime)

print(newest_file)

df = pd.read_csv(newest_file, encoding='utf-8').convert_dtypes()

print(df.info())

df = df.explode('hourly').reset_index()
df['hourly_units'] = df['hourly_units'].iloc[0]  # Assuming 'hourly_units' is consistent across rows
df = df.pivot(columns='hourly_units', values='hourly').reset_index()

print(df.to_string())

# print(pd.DataFrame(df['hourly'].reset_index(drop=True)))

# print(df[''].to_string())

# for x in p.iterdir(output_dir):
#     if x.is_file():
#         if x.glob('output_file_'):
#             print(x)

# file_path = os.path.abspath('.')

# os.path.fi

# df = pd.read_csv(f"{file_path}\\output_files")