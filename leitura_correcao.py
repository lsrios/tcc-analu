# ==========================================================
import cv2  # "Biblioteca" OpenCV
import pytesseract  # Módulo para a utilização da tecnologia OCR

import time  # "Biblioteca" nativa de Python para calcularmos quantos frames por segundo
from PIL import Image  # Importando o módulo Pillow para abrir a imagem no script
from _thread import start_new_thread  # Thread
import re


# ==========================================================
novaThread = True  # Variável utilizada para evitar várias threads rodando ao mesmo tempo


def runOCR(frame_gray):
    global novaThread

    # Definição do dicionário para correção da leitura
    let_num = {'O': '0', '0': '0', 'I': '1', '1': '1', 'Z': '2', '2': '2', '3': '3', 'A': '4', '4': '4', 'S': '5',
               '5': '5', '6': '6', '7': '7', 'B': '8', '8': '8', '9': '9', 'C': 'C', 'D': 'D',
               'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N',
               'P': 'P', 'Q': 'Q', 'R': 'R', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X',
               'Y': 'Y'}
    num_let = {'0': 'O', '1': 'I', '2': 'Z', '4': 'A', '5': 'S', '8': 'B', 'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D',
               'E': 'E', 'F': 'F', 'G': 'G', 'H': 'H', 'I': 'I', 'J': 'J', 'K': 'K', 'L': 'L', 'M': 'M', 'N': 'N',
               'O': 'O', 'P': 'P', 'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'X',
               'Y': 'Y', 'Z': 'Z', '3': '3', '6': '6', '7': '7', '9': '9'}

    ind_num = [3, 5, 6] #índices de caracteres numericos
    ind_let = [0, 1, 2, 4] #índices de caracteres alfabéticos

    novaThread = False

    leitura = pytesseract.image_to_string(Image.fromarray(frame_gray), config='-psm 11')  # realiza a leitura e a transformação da imagem em string


    if len(leitura) > 1:

        pattern = re.compile(r'[A-Z0-9]{7}') #Define padrão a ser encontrado na string
        matches = pattern.finditer(leitura) #busca o padrão na variável leitura

        for match in matches:
            a = match.group(0) #variável que recebe o padrão identificado
            print("===========================================\n" "A placa lida é: ", a)

            # Correção da leitura:
            placaCorreg = list(a)

            aux_let = [num_let[a[i]] for i in ind_let]
            aux_num = [let_num[a[i]] for i in ind_num]

            for i, j in enumerate(ind_num):
                placaCorreg[j] = aux_num[i]

            for i, j in enumerate(ind_let):
                placaCorreg[j] = aux_let[i]

            # Resultado:
            a1 = ''.join(placaCorreg)
            print("A placa corrigida é: ", a1)

    novaThread = True


# ==========================================================
cap = cv2.VideoCapture(0)  # 0 - Primeira camera, 1 - segunda camera, ou 'C:/path/para/arquivo/de/video.avi'
start = time.time()

while (True):  # Loop Infinito

    # Leitura:
    ret, frame = cap.read()  # Lendo frame atual
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertendo o frame (RGB) para tons de cinza
    cv2.imshow('Tons de Cinza', frame_gray)  # Mostrando imagem na janela com título "Tons de Cinza"


    # Calcundo quantos frames por segundo (a cada 2 segundos):
    if time.time() - start > 1:  # Se já se passaram os "x" segundos:
        start = time.time()  # Reseta o tempo inicial

        if novaThread == True:  # Se pudermos fazer uma nova leitura OCR:
            start_new_thread(runOCR, (frame_gray,))  # Executa o OCR em uma nova Thread, para não travarmos a aplicação


    # Final:
    if cv2.waitKey(1) & 0xFF == ord(
            'q'):  # Se o usuário estiver com a janela aberta e pressionar "q", iremos encerrar o programa
        break



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