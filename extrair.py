from urllib.request import urlretrieve
from pathlib import Path




adress = "ftp://ftp.datasus.gov.br/dissemin/publicos/SIHSUS/200801_/Dados/"
destination = Path("dados")

for mes in range(1, 13):
    name = f"RDMG25{mes:02d}.dbc"
    endereco = adress + name            
    destino = destination / name        

    if destino.exists():
        print(f"{name} já existe, pulando")
    else:
        print(f"Baixando {name}...")
        urlretrieve(endereco, destino)
        print(f"{name} pronto!")
