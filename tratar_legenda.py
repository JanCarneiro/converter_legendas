from odf.opendocument import OpenDocumentText
from odf.text import P
import os
import shutil
import xml.etree.ElementTree as ET
import re


PATH_BASE = '<<SEU PATH>>'
PATH_DESTINO = '<<SEU PATH>>'

def extrair_legendas(xml_path):
    namespaces = {
        'tt': 'http://www.w3.org/ns/ttml',
    }

    tree = ET.parse(PATH_BASE+xml_path)
    root = tree.getroot()

    legendas = []
    for p in root.findall('.//tt:body/tt:div/tt:p', namespaces):
        
        texto = ''.join(p.itertext()).strip()
        legendas.append((texto))
        
    return legendas

def salvar_em_txt(legendas, caminho_saida):
    caminho_saida = PATH_BASE.replace('files_brutos', 'Legendas') + caminho_saida
    doc = OpenDocumentText()
    for texto in legendas:
        texto = re.sub(r'(?<!^)(?<!\n)(-)(?=[^\s])', r'\n\1', texto)

        if not texto.startswith('-'):
            texto = '- ' + texto
        else:
            texto = texto.replace('-', '- ')
        
    
        p = P(text=texto)
        doc.text.addElement(p)
    doc.save(f'{caminho_saida}')

file_xml = os.listdir(f'{PATH_BASE}')
legendas_files = [arquivo.replace("xml", "odt") for arquivo in file_xml]

for arquivo_xml,saida_odt in zip(file_xml,legendas_files):
  legendas = extrair_legendas(arquivo_xml)
  salvar_em_txt(legendas, saida_odt)

  shutil.move(PATH_BASE+arquivo_xml,PATH_DESTINO)
  print(f"Removido arquivo {arquivo_xml}")
  print(f"Arquivo '{saida_odt}' salvo em 'Legendas' com sucesso!")