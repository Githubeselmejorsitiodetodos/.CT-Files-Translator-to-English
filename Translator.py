import xml.etree.ElementTree as ET
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory
import time
import os
import glob

# Avoid inconsistencies in language detection
DetectorFactory.seed = 0

# WINDOWS PATH FIX: Forces the script to use its own folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("==========================================================")
print("     AUTOMATIC INTELLIGENT CHEAT TABLE TRANSLATOR        ")
print("             (Any Language -> ENGLISH)                   ")
print("==========================================================\n")

print("[1/3] Searching for .ct files in the folder...")
archivos_ct = glob.glob("*.ct")

if not archivos_ct:
    print("\n[ERROR] No Cheat Table (.ct) file was found here.")
    print("INSTRUCTIONS: Place this script IN THE SAME FOLDER as")
    print("the .ct file you want to translate and open it again.")
    input("\nPress Enter to exit...")
    exit()

# Automatically selects the first table found
archivo_origen = archivos_ct[0]
archivo_destino = "cheat_table_english.ct"

print(f"[OK] Table detected: '{archivo_origen}'")
print(f"[OK] The translated file will be saved as: '{archivo_destino}'")
print("\n[2/3] Starting line-by-line translation...")
print("Please wait. This process may take a few minutes for thousands of lines...\n")

# LANGUAGE CONFIGURATION: Target set to 'en' (English)
traductor_vi = GoogleTranslator(source='vi', target='en')
traductor_es = GoogleTranslator(source='es', target='en')
truaductor_auto = GoogleTranslator(source='auto', target='en')

try:
    with open(archivo_origen, 'r', encoding='utf-8', errors='ignore') as f:
        xml_data = f.read()
    
    root = ET.fromstring(xml_data)
    total_lineas = 0
    traducidas = 0

    for elem in root.iter():
        if elem.tag in ['Description', 'Comments'] and elem.text:
            texto_original = elem.text.strip('"').strip()
            
            # Ignore numbers, hex codes, and empty strings
            if not texto_original or texto_original.isdigit() or texto_original.startswith(('0x', '[', '::')):
                continue
                
            total_lineas += 1
            texto_final = texto_original
            
            try:
                # Detect line language automatically
                idioma = detect(texto_original)
                if idioma == 'vi':
                    texto_final = traductor_vi.translate(texto_original)
                    traducidas += 1
                elif idioma == 'es':
                    texto_final = traductor_es.translate(texto_original)
                    traducidas += 1
                elif idioma == 'en':
                    # If it's already in English, skip translation entirely
                    texto_final = texto_original
                else:
                    texto_final = truaductor_auto.translate(texto_original)
                    traducidas += 1
            except Exception:
                try:
                    texto_final = truaductor_auto.translate(texto_original)
                    traducidas += 1
                except Exception:
                    pass

            if elem.text.startswith('"') and elem.text.endswith('"'):
                elem.text = f'"{texto_final}"'
            else:
                elem.text = texto_final

            # Security delay to prevent IP bans from the server
            if traducidas % 10 == 0:
                time.sleep(0.3)
                
            if total_lineas % 50 == 0:
                print(f" -> Processed {total_lineas} lines of text...")

    print("\n[3/3] Saving changes...")
    tree = ET.ElementTree(root)
    tree.write(archivo_destino, encoding='utf-8', xml_declaration=True)
    
    print("\n==========================================================")
    print(f" [SUCCESS] Process finished successfully.")
    print(f" Analyzed {total_lineas} text lines.")
    print("==========================================================")

except Exception as e:
    print(f"\n[ERROR] An issue occurred with the file format: {e}")

input("\nPress Enter to close the program...")
