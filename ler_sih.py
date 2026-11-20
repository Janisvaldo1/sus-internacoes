import pandas as pd
from pyreaddbc import dbc2dbf
from dbfread import DBF

# 1. Descompactar: .dbc (formato do SUS) -> .dbf (tabela antiga, legível)
dbc2dbf("dados/RDMG2609.dbc", "dados/RDMG2609.dbf")

# 2. Ler o .dbf como tabela do pandas (o SUS usa acentuação latin-1)
df = pd.DataFrame(iter(DBF("dados/RDMG2609.dbf", encoding="iso-8859-1")))
print("Internações em MG em set/2026:", len(df))

# 3. Moradores de Aiuruoca (onde o paciente MORA)
aiu = df[df["MUNIC_RES"] == "310120"]
print("Moradores de Aiuruoca internados no mês:", len(aiu))

# Onde os moradores de Aiuruoca foram internados (qual estabelecimento)
print(aiu["CNES"].value_counts().head(15))

# 4. Internações feitas EM Aiuruoca (onde fica o HOSPITAL)
hosp = df[df["MUNIC_MOV"] == "310120"]
print("Internações feitas em Aiuruoca no mês:", len(hosp))

# Quantos hospitais internaram em Aiuruoca?
print(hosp["CNES"].value_counts())

# De onde vêm os pacientes atendidos em Aiuruoca?
print(hosp["MUNIC_RES"].value_counts().head(15))