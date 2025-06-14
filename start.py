import uvicorn # type: ignore
import sys
import os

# Adiciona o diretório "backend" ao path de importação
#sys.path.append(os.path.abspath("./backend"))
if __name__ == "__main__":
    uvicorn.run("backend.main:app", reload=True)
