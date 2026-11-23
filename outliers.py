import pandas as pd

mart = pd.read_parquet("dados/mart_internacoes_regiao_2025.parquet")

# 1. Quartis da coluna (o pandas calcula o que você fez no rascunho)
q1 = mart["DIAS_PERM"].quantile(0.25)
q3 = mart["DIAS_PERM"].quantile(0.75)

# 2. IQR, folga e limite de cima (as mesmas contas do rascunho)
iqr = q3 - q1
folga = 1.5 * iqr
limite_baixo = q1 - folga
limite_cima = q3 + folga
print(f"Q1={q1} Q3={q3} IQR={iqr} folga={folga} limite de baixo={limite_baixo} limite de cima={limite_cima}")

# 3. Filtrar as internações acima do limite (antes era o 11 escrito à mão)
internacoes_dias = mart[mart["DIAS_PERM"] > limite_cima]
print(len(internacoes_dias))
print(f"{len(internacoes_dias) / len(mart) * 100:.1f}% das internações")

print(internacoes_dias["CID_LETRA"].value_counts().head(10))

colunas = ["DIAS_PERM", "DIAG_PRINC", "IDADE", "MUNIC_RES", "MUNIC_MOV"]
print(internacoes_dias.sort_values("DIAS_PERM", ascending=False)[colunas].head(10))   

print(mart["VAL_TOT"].describe())

q1 = mart["VAL_TOT"].quantile(0.25)
q3 = mart["VAL_TOT"].quantile(0.75)


iqr = q3 - q1
folga = 1.5 * iqr
limite_baixo = q1 - folga
limite_cima = q3 + folga
print(f"Q1={q1} Q3={q3} IQR={iqr} folga={folga} limite de baixo={limite_baixo} limite de cima={limite_cima}")

internacao_maior = mart[mart["VAL_TOT"] > limite_cima]
print(f"{len(internacao_maior)} internações custaram mais de R$ {limite_cima:.2f}")
print(f"{len(internacao_maior) / len(mart) * 100:.1f}% das internações")

print(internacao_maior["CID_LETRA"].value_counts().head(10))

colunas = ["VAL_TOT", "DIAS_PERM", "DIAG_PRINC", "MUNIC_RES", "MUNIC_MOV"]
print(internacao_maior.sort_values("VAL_TOT", ascending=False)[colunas].head(10))


perfil = pd.crosstab(mart["MUNIC_RES"], mart["CID_LETRA"], normalize="index") * 100
print(perfil.round(1))
print(perfil.shape)

