import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

mart = pd.read_parquet("dados/mart_internacoes_regiao_2025.parquet")
perfil = pd.crosstab(mart["MUNIC_RES"], mart["CID_LETRA"], normalize="index") * 100

# lista para guardar o SSE de cada K
sse = []

# para cada K de 1 a 8, o K-means agrupa as 21 cidades e guarda o SSE
for k in range(1, 9):
    modelo = KMeans(n_clusters=k, n_init=10, random_state=42)
    modelo.fit(perfil)
    sse.append(modelo.inertia_)
    print(f"K={k}: SSE={modelo.inertia_:.1f}")

# gráfico para achar o joelho
plt.plot(range(1, 9), sse, marker="o")
plt.xlabel("K (número de grupos)")
plt.ylabel("SSE")
plt.title("Método do joelho")
# plt.show()

nomes = {
    "310120": "Aiuruoca", "311480": "Carvalhos", "313850": "Liberdade",
    "316640": "Seritinga", "316700": "Serranos", "310720": "Bocaina de Minas",
    "310130": "Alagoa", "310360": "Arantina", "310750": "Bom Jardim de Minas",
    "313590": "Jesuânia", "313300": "Itamonte", "314780": "Passa-Vinte",
    "315930": "Santa Rita do Jacutinga", "311550": "Caxambu",
    "316530": "São Vicente de Minas", "310280": "Andrelândia",
    "314190": "Minduri", "312080": "Cruzília", "310490": "Baependi",
    "313780": "Lambari", "314760": "Passa Quatro",
}

def testar(k):
    modelo = KMeans(n_clusters=k, n_init=10, random_state=42)
    grupos = modelo.fit_predict(perfil)
    print(f"\n===== K = {k} =====")
    for g in range(k):
        cidades = perfil.index[grupos == g]
        media = perfil.loc[cidades].mean().sort_values(ascending=False).head(3)
        print(f"\nGrupo {g}: {', '.join(nomes.get(c, c) for c in cidades)}")
        print("  Mais comuns:", ", ".join(f"{letra} {valor:.1f}%" for letra, valor in media.items()))

testar(4)
testar(5)

