from pathlib import Path

import pandas as pd

DATASET = Path(
    'data/raw/nevworld_672389029456688961_20261005_182855.jsonl'
)

#Comprobando que la ruta existe
if not DATASET.exists():
    raise FileNotFoundError(
        f'No se encuentra: {DATASET.resolve()}'
    )

df = pd.read_json(DATASET, lines=True)


required = [
    'run_id', 'event_index', 'tick', 'type'
]

#Comprobando que la tabla no esta vacia
assert not df.empty, 'El dataset está vacío'

#Comprobando que las columnas principales
assert all(column in df.columns for column in required), \
    'Faltan columnas principales'

#Comprobando que no se repita la pareja
assert not df.duplicated(['run_id', 'event_index']).any(), \
    'Hay eventos duplicados'

#Comprobando que los ticks no retrocedan
ordered = df.sort_values('event_index')
assert ordered['tick'].is_monotonic_increasing, \
    'Los ticks retroceden'

print('\nVALIDACIÓN BÁSICA: OK')

#Mostrando las primeras filas
print('\n Primeros Eventos ')
print(df.head())

#Tomando filas y columnas
filas, columnas = df.shape

#Mostrando filas y columnas
print('Eventos:', filas)
print('Columnas:', columnas)

#Nombres de columnas 
print(df.columns.tolist())

#Tipo del primer evento 
print(df['type'].iloc[0])

#Tipo del evento mas frecuente 
print(df['type'].value_counts())


#Tipos de evento
tipos = set(df['type'].tolist())
print(tipos)

#Run ID
print('run_id:', df['run_id'].iloc[0])

#Semilla
print('semilla:', df['seed'].iloc[0])

#Esquema
print('esquema:', df['schema_version'].iloc[0])

#Tick Minimo
print('primer tick:', df['tick'].min())

#Tick Maximo
print('último tick:', df['tick'].max())