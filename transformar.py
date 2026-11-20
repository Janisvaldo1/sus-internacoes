from pathlib import Path

import pandas as pd
from dbfread import DBF
from pyreaddbc import dbc2dbf

destination = Path("dados")

# =========================================================
# T (pré-processamento): converter os 12 .dbc em .dbf
# =========================================================
for mes in range(1, 13):
    entrada = destination / f"RDMG25{mes:02d}.dbc"
    saida = entrada.with_suffix(".dbf")

    if saida.exists():
        print(f"{saida} já existe, pulando")
    else:
        print(f"Transformando {saida}...")
        dbc2dbf(entrada, saida)
        print(f"{saida} pronto!")


def ler_mes(mes):
    """Lê o .dbf de um mês de 2025 como DataFrame."""
    caminho = destination / f"RDMG25{mes:02d}.dbf"
    return pd.DataFrame(iter(DBF(caminho, encoding="iso-8859-1")))


# =========================================================
# SELEÇÃO 1: de onde vêm os pacientes do hospital de Aiuruoca
# =========================================================
partes = []
for mes in range(1, 13):
    df = ler_mes(mes)
    inter_aiu = df[df["MUNIC_MOV"] == "310120"]
    partes.append(inter_aiu["MUNIC_RES"])
    print(f"Mês {mes:02d}: {len(inter_aiu)} internações no hospital de Aiuruoca")

todas = pd.concat(partes)
contagem = todas.value_counts()
print(f"\nTotal no hospital de Aiuruoca em 2025: {len(todas)}")

# A região: cidades com 5 ou mais internações no hospital no ano
MINIMO = 5
regiao = contagem[contagem >= MINIMO].index
print(f"Cidades na região (mínimo {MINIMO}): {len(regiao)}")
print(f"Internações dessas cidades no hospital: {contagem[regiao].sum()}")

# =========================================================
# SELEÇÃO 2 + INTEGRAÇÃO: internações dos moradores da região,
# em qualquer hospital de MG, juntando os 12 meses
# =========================================================
partes_mart = []
for mes in range(1, 13):
    df = ler_mes(mes)
    moradores = df[df["MUNIC_RES"].isin(regiao)]
    partes_mart.append(moradores)          # a linha inteira, todas as colunas
    print(f"Mês {mes:02d}: {len(moradores)} internações de moradores da região")

mart = pd.concat(partes_mart, ignore_index=True)

# =========================================================
# TRANSFORMAÇÃO: grupo do CID pela primeira letra
# =========================================================
mart["CID_LETRA"] = mart["DIAG_PRINC"].str[0]

# =========================================================
# CARGA: salvar o data mart
# =========================================================
arquivo_mart = destination / "mart_internacoes_regiao_2025.parquet"
mart.to_parquet(arquivo_mart, index=False)

# =========================================================
# CONFERÊNCIA
# =========================================================
no_hospital = mart[mart["MUNIC_MOV"] == "310120"]
print(f"\nData mart salvo em {arquivo_mart}")
print(f"Linhas: {len(mart)} | Colunas: {mart.shape[1]}")
print(f"Destas, no hospital de Aiuruoca: {len(no_hospital)}")