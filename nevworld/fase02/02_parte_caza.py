from pathlib import Path
import pandas as pd

# 1. Leer el RAW y crear `data/processed` si hace falta.
DATASET = Path('data/raw/nevworld_672389029456688961_20261005_182855.jsonl')
OUTPUT_DIR = Path('data/processed')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_json(DATASET, lines=True)



def event_table(event_type, columns):
    # 3. Conservar `run_id`, `event_index` y `tick`, que la función añade automáticamente.
    selected = ['run_id', 'event_index', 'tick', *columns]

    available = [column for column in selected if column in df.columns]

    columnas_de_salida = [
        'run_id',
        'event_index',
        'tick',
        'villager_id',
        'prey_type',
        'simulation_day',
    ]

    table = df.loc[
        df['type'] == event_type,
        available,
    ].copy()

    # 4. Añadir `simulation_day` mediante `tick // 12000`.
    if not table.empty:
        for col in columns:
            assert col in table.columns
        table['simulation_day'] = table['tick'] // 12000

    table = table.reindex(columns=columnas_de_salida)

    return table

# 2. Seleccionar únicamente cacerías completadas y los campos justificados en tu ficha.
hunts = event_table('hunt_completed', ['villager_id', 'prey_type'])

output = OUTPUT_DIR / f'hunts.csv'

# 5. Guardar `data/processed/hunts.csv` sin exportar el índice de pandas.
hunts.to_csv(output, index=False)

# 6. Mostrar la ruta del archivo generado y su número de filas.
print(output, len(hunts), 'filas')

# Comprueba que el número de filas del CSV coincide con el RAW
assert len(hunts) == (df['type'] == 'hunt_completed').sum()

campos_obligatorios = ['run_id','event_index','tick','villager_id','prey_type']

assert hunts[campos_obligatorios].notna().all().all()

assert (hunts['simulation_day'] == hunts['tick'] // 12000).all()