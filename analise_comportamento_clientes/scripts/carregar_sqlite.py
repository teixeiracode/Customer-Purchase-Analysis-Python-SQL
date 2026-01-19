import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "dados" / "clientes.csv"
DB_PATH = BASE_DIR / "banco" / "clientes.db"

print("📂 Iniciando carga de dados...")

# Verificações
if not CSV_PATH.exists():
    raise FileNotFoundError("❌ clientes.csv não encontrado")

try:
    df = pd.read_csv(CSV_PATH, encoding='utf-8-sig', sep=',', engine='python')
except pd.errors.EmptyDataError:
    raise ValueError("❌ O arquivo clientes.csv está vazio ou não tem colunas válidas")

if df.empty:
    raise ValueError("❌ O arquivo clientes.csv está vazio")

print(f"📊 {len(df)} registros carregados")

# Tratamento
df["data_compra"] = pd.to_datetime(df["data_compra"], errors="coerce")
df["valor_compra"] = pd.to_numeric(df["valor_compra"], errors="coerce")

df = df.dropna()

print("🧹 Dados tratados com sucesso")

# Salvar no SQLite
conn = sqlite3.connect(DB_PATH)
df.to_sql("compras_clientes", conn, if_exists="replace", index=False)
conn.close()

print("✅ Banco SQLite criado com sucesso")
print(f"📁 Caminho: {DB_PATH}")
