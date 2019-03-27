import cv2
import pytesseract
import time
from PIL import Image
from _thread import start_new_thread


novaThread = True


def runOCR(frame_gray):
    global novaThread

    novaThread = False

    leitura = pytesseract.image_to_string(Image.fromarray(frame_gray), config='-psm 11')  # realiza a leitura com o pytesseract da imagem em escala de cinza"
    if len(leitura) > 1:
        print("------------------------\n", "Resultado: |", leitura, "|")

    novaThread = True



cap = cv2.VideoCapture(0)  # 0 - Primeira camera, 1 - segunda camera, ou 'C:/path/para/arquivo/de/video.avi'
start = time.time()

while (True):  # Loop Infinito
    # ---------------------------------------
    # Leitura:
    ret, frame = cap.read()  # Lendo frame atual
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertendo o frame (RGB) para tons de cinza
    cv2.imshow('Tons de Cinza', frame_gray)  # Mostrando imagem na janela com título "Tons de Cinza"

    # ---------------------------------------
    # Calcundo quantos frames por segundo (a cada 2 segundos):
    if time.time() - start > 1:  # Se já se passaram os "x" segundos:
        start = time.time()  # Reseta o tempo inicial

        if novaThread == True:  # Se pudermos fazer uma nova leitura OCR:
            start_new_thread(runOCR, (frame_gray,))  # Executa o OCR em uma nova Thread, para não travarmos a aplicação

    # ---------------------------------------
    # Final:
    if cv2.waitKey(1) & 0xFF == ord(
            'q'):  # Se o usuário estiver com a janela aberta e pressionar "q", encerraa o programa
        break

    # ---------------------------------------

# ==========================================================
cap.release()  # Liberando Webcam para o Sistema Operacional
cv2.destroyAllWindows()  # Fechando todas as janelas do OpenCV

import os

os._exit(0)

# ==========================================================

"""
Usage:
  tesseract --help | --help-extra | --help-psm | --help-oem | --version
  tesseract --list-langs [--tessdata-dir PATH]
  tesseract --print-parameters [options...] [configfile...]
  tesseract imagename|imagelist|stdin outputbase|stdout [options...] [configfile...]

OCR options:
  --tessdata-dir PATH   Specify the location of tessdata path.
  --user-words PATH     Specify the location of user words file.
  --user-patterns PATH  Specify the location of user patterns file.
  -l LANG[+LANG]        Specify language(s) used for OCR.
  -c VAR=VALUE          Set value for config variables.
                        Multiple -c arguments are allowed.
  --psm NUM             Specify page segmentation mode.
  --oem NUM             Specify OCR Engine mode.
NOTE: These options must occur before any configfile.

Page segmentation modes:
  0    Orientation and script detection (OSD) only.
  1    Automatic page segmentation with OSD.
  2    Automatic page segmentation, but no OSD, or OCR.
  3    Fully automatic page segmentation, but no OSD. (Default)
  4    Assume a single column of text of variable sizes.
  5    Assume a single uniform block of vertically aligned text.
  6    Assume a single uniform block of text.
  7    Treat the image as a single text line.
  8    Treat the image as a single word.
  9    Treat the image as a single word in a circle.
 10    Treat the image as a single character.
 11    Sparse text. Find as much text as possible in no particular order.
 12    Sparse text with OSD.
 13    Raw line. Treat the image as a single text line,
       bypassing hacks that are Tesseract-specific.

OCR Engine modes:
  0    Legacy engine only.
  1    Neural nets LSTM engine only.
  2    Legacy + LSTM engines.
  3    Default, based on what is available.

Single options:
  -h, --help            Show minimal help message.
  --help-extra          Show extra help for advanced users.
  --help-psm            Show page segmentation modes.
  --help-oem            Show OCR Engine modes.
  -v, --version         Show version information.
  --list-langs          List available languages for tesseract engine.
  --print-parameters    Print tesseract parameters.
"""