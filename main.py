from PlateScanner import PlateScanner
from AcpTrafego import AcpTrafego
import time

plateScanner = PlateScanner(1, "Aninha", False)
# acpTrafego = AcpTrafego(2, "Anao")

# plateScannerThread = threading.Thread()
# acpTrafegoThread = threading.Thread()

plateScanner.start()
# acpTrafego.run()

for i in range(15):
    print("To rodando")
    time.sleep(10)