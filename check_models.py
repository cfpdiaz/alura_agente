import google.generativeai as genai
import os

print('Conectando con Google AI Studio...')
genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

print('Modelos de embedding disponibles para tu API Key:')
try:
    encontrado = False
    for m in genai.list_models():
        if 'embedContent' in m.supported_generation_methods:
            print(f' - {m.name}')
            encontrado = True
            
    if not encontrado:
        print(' ⚠️ No se encontraron modelos de embedding permitidos para esta llave.')
except Exception as e:
    print(f'Error al conectar: {e}')
