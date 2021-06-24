Pro správné spuštění je potřeba provést naásledující kroky:

1. Vytvořit virtuální prostředí pythonu:
   - ve složce se zdrojovými soubory spusť v příkazové řádce následující příkaz
   - "virtualenv venv"
   - vytvoří se složka venv s kopií prostředí pythonu
   - aktivuj prostředí příkazem
   - "venv\Scripts\activate"
2. Instalce knihoven:
   - příkaz "pip install ezdxf"
   - nutné aby bylo spuštěno virtuální prostředí, pozná se to tak, že je vedle cesty v
     příkazovém řádku v závorkách název prostředí např. "(venv) D:\Program\DXF_creator"
3. Spuštění programu:
   - příkaz "python main.py"
   - nutné aby bylo spuštěno virtuální prostředí
