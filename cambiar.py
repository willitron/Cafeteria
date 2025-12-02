
import os
import re
from pathlib import Path

def cambiar_moneda_en_archivo(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        contenido_original = contenido
        
        contenido = contenido.replace('>${{', '>Bs {{')
        contenido = contenido.replace('${{', 'Bs {{')
        contenido = contenido.replace('"$', '"Bs ')
        contenido = contenido.replace("'$", "'Bs ")
        contenido = contenido.replace('$0.00', 'Bs 0.00')
        contenido = contenido.replace('>$<', '>Bs<')
        contenido = contenido.replace('Total: $', 'Total: Bs ')
        contenido = contenido.replace('TOTAL: $', 'TOTAL: Bs ')
        contenido = contenido.replace('-${{', '-Bs {{')
        
        contenido = contenido.replace('textContent = "$"', 'textContent = "Bs "')
        contenido = contenido.replace("textContent = '$'", "textContent = 'Bs '")
        contenido = contenido.replace('innerHTML = "$"', 'innerHTML = "Bs "')
        contenido = contenido.replace("innerHTML = '$'", "innerHTML = 'Bs '")
        contenido = contenido.replace('+ "$"', '+ "Bs "')
        contenido = contenido.replace("+ '$'", "+ 'Bs '")
        contenido = contenido.replace('"$" +', '"Bs " +')
        contenido = contenido.replace("'$' +", "'Bs ' +")
        
        contenido = re.sub(r'(\s+)\$\$\{', r'\1Bs \${', contenido)  # Para template strings JS
        contenido = re.sub(r'>\$\$\{', r'>Bs \${', contenido)
        
        if contenido != contenido_original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(contenido)
            return True
        return False
    
    except Exception as e:
        print(f"Error al procesar {filepath}: {e}")
        return False


def main():
    print("=" * 60)
    print("  CAMBIO DE MONEDA: $ → Bs")
    print("=" * 60)
    print()
    
    if not os.path.exists('templates'):
        print("Error: No se encontró la carpeta 'templates'")
        print("   Asegúrate de ejecutar este script desde la raíz del proyecto")
        return
    
    archivos_procesados = 0
    archivos_modificados = 0
    
    templates_dir = Path('templates')
    
    for html_file in templates_dir.rglob('*.html'):
        archivos_procesados += 1
        print(f"Procesando: {html_file}", end=" ... ")
        
        if cambiar_moneda_en_archivo(html_file):
            archivos_modificados += 1
            print("✓ MODIFICADO")
        else:
            print("○ Sin cambios")
    
    print()
    print("=" * 60)
    print(f"  RESUMEN")
    print("=" * 60)
    print(f"  Archivos procesados: {archivos_procesados}")
    print(f"  Archivos modificados: {archivos_modificados}")
    print("=" * 60)
    print()
    
    if archivos_modificados > 0:
        print(" Cambio completado exitosamente!")
        print("   Todos los símbolos $ han sido reemplazados por Bs")
        print()
        print(" Próximos pasos:")
        print("   1. Revisa los cambios en tus archivos")
        print("   2. Ejecuta: python app.py")
        print("   3. Verifica que los precios se muestren correctamente")
    else:
        print(" No se encontraron símbolos $ para reemplazar")
        print("   Puede que ya hayas ejecutado este script anteriormente")
    
    print()


if __name__ == '__main__':
    main()