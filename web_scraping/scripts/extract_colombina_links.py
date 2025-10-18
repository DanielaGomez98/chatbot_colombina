#!/usr/bin/env python3
"""
Script para extraer todos los links de la página principal de Colombina
Autor: Assistant
Fecha: 2025-01-13
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import csv
import time
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('colombina_links.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ColombinaLinkExtractor:
    def __init__(self, base_url="https://colombina.com/co-es"):
        self.base_url = base_url
        self.session = requests.Session()
        self.links = set()  # Usar set para evitar duplicados
        
        # Headers para simular un navegador real
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session.headers.update(self.headers)
    
    def is_valid_url(self, url):
        """Valida si una URL es válida y pertenece al dominio de Colombina"""
        try:
            parsed = urlparse(url)
            # Verificar que tenga esquema (http/https)
            if not parsed.scheme:
                return False
            # Verificar que sea del dominio de Colombina o un subdominio
            if 'colombina.com' not in parsed.netloc and parsed.netloc != '':
                return False
            return True
        except:
            return False
    
    def extract_links_from_page(self, url):
        """Extrae todos los links de una página específica"""
        try:
            logger.info(f"Extrayendo links de: {url}")
            
            # Realizar petición con timeout
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parsear HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Encontrar todos los elementos con enlaces
            link_elements = soup.find_all(['a', 'link'], href=True)
            
            page_links = set()
            
            for element in link_elements:
                href = element.get('href')
                if href:
                    # Convertir enlaces relativos a absolutos
                    absolute_url = urljoin(url, href)
                    
                    # Limpiar fragmentos (#) y parámetros de tracking innecesarios
                    clean_url = absolute_url.split('#')[0]
                    
                    if self.is_valid_url(clean_url):
                        page_links.add(clean_url)
                        
                        # Obtener información adicional del link
                        link_info = {
                            'url': clean_url,
                            'text': element.get_text(strip=True) if element.name == 'a' else '',
                            'title': element.get('title', ''),
                            'class': ' '.join(element.get('class', [])),
                            'rel': ' '.join(element.get('rel', [])),
                            'found_on': url,
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        self.links.add((clean_url, json.dumps(link_info)))
            
            logger.info(f"Encontrados {len(page_links)} links únicos en {url}")
            return page_links
            
        except requests.RequestException as e:
            logger.error(f"Error al acceder a {url}: {e}")
            return set()
        except Exception as e:
            logger.error(f"Error inesperado al procesar {url}: {e}")
            return set()
    
    def categorize_links(self, links):
        """Categoriza los links por tipo"""
        categories = {
            'productos': [],
            'categorias': [],
            'institucional': [],
            'noticias': [],
            'contacto': [],
            'social': [],
            'externos': [],
            'otros': []
        }
        
        for link in links:
            url = link.lower()
            
            if any(keyword in url for keyword in ['producto', 'product']):
                categories['productos'].append(link)
            elif any(keyword in url for keyword in ['categoria', 'category', 'dulces', 'galletas', 'chocolates']):
                categories['categorias'].append(link)
            elif any(keyword in url for keyword in ['nosotros', 'about', 'quienes-somos', 'historia']):
                categories['institucional'].append(link)
            elif any(keyword in url for keyword in ['noticia', 'news', 'blog', 'prensa']):
                categories['noticias'].append(link)
            elif any(keyword in url for keyword in ['contacto', 'contact']):
                categories['contacto'].append(link)
            elif any(keyword in url for keyword in ['facebook', 'instagram', 'twitter', 'linkedin', 'youtube']):
                categories['social'].append(link)
            elif 'colombina.com' not in url:
                categories['externos'].append(link)
            else:
                categories['otros'].append(link)
        
        return categories
    
    def save_to_json(self, filename="colombina_links.json"):
        """Guarda los links en formato JSON"""
        links_data = []
        for link_tuple in self.links:
            url, info_json = link_tuple
            link_info = json.loads(info_json)
            links_data.append(link_info)
        
        data = {
            'extraction_date': datetime.now().isoformat(),
            'base_url': self.base_url,
            'total_links': len(links_data),
            'links': links_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Links guardados en {filename}")
    
    def save_to_csv(self, filename="colombina_links.csv"):
        """Guarda los links en formato CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['URL', 'Texto', 'Título', 'Clases CSS', 'Rel', 'Encontrado en', 'Timestamp'])
            
            for link_tuple in self.links:
                url, info_json = link_tuple
                link_info = json.loads(info_json)
                writer.writerow([
                    link_info['url'],
                    link_info['text'],
                    link_info['title'],
                    link_info['class'],
                    link_info['rel'],
                    link_info['found_on'],
                    link_info['timestamp']
                ])
        
        logger.info(f"Links guardados en {filename}")
    
    def save_categorized_links(self, filename="colombina_links_categorized.json"):
        """Guarda los links categorizados"""
        urls_only = [json.loads(link_tuple[1])['url'] for link_tuple in self.links]
        categorized = self.categorize_links(urls_only)
        
        data = {
            'extraction_date': datetime.now().isoformat(),
            'base_url': self.base_url,
            'total_links': len(urls_only),
            'categories': categorized,
            'category_counts': {category: len(links) for category, links in categorized.items()}
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Links categorizados guardados en {filename}")
    
    def extract_all_links(self):
        """Método principal para extraer todos los links"""
        logger.info("Iniciando extracción de links de Colombina...")
        
        # Extraer links de la página principal
        main_links = self.extract_links_from_page(self.base_url)
        
        # Pausa para ser respetuosos con el servidor
        time.sleep(1)
        
        logger.info(f"Extracción completada. Total de links únicos encontrados: {len(self.links)}")
        
        return self.links
    
    def print_summary(self):
        """Imprime un resumen de los links encontrados"""
        urls_only = [json.loads(link_tuple[1])['url'] for link_tuple in self.links]
        categorized = self.categorize_links(urls_only)
        
        print("\n" + "="*50)
        print("RESUMEN DE EXTRACCIÓN DE LINKS - COLOMBINA")
        print("="*50)
        print(f"Página base: {self.base_url}")
        print(f"Total de links únicos: {len(urls_only)}")
        print(f"Fecha de extracción: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\nCATEGORÍAS DE LINKS:")
        for category, links in categorized.items():
            print(f"  {category.capitalize()}: {len(links)} links")
        
        print("\nPRIMEROS 10 LINKS ENCONTRADOS:")
        for i, url in enumerate(urls_only[:10], 1):
            print(f"  {i}. {url}")
        
        if len(urls_only) > 10:
            print(f"  ... y {len(urls_only) - 10} más")
        
        print("="*50)

def main():
    """Función principal"""
    extractor = ColombinaLinkExtractor()
    
    try:
        # Extraer links
        links = extractor.extract_all_links()
        
        # Mostrar resumen
        extractor.print_summary()
        
        # Guardar en diferentes formatos
        extractor.save_to_json()
        extractor.save_to_csv()
        extractor.save_categorized_links()
        
        print(f"\nArchivos generados:")
        print("- colombina_links.json (todos los links con metadata)")
        print("- colombina_links.csv (formato tabular)")
        print("- colombina_links_categorized.json (links por categorías)")
        print("- colombina_links.log (log de la ejecución)")
        
    except Exception as e:
        logger.error(f"Error en la ejecución principal: {e}")
        raise

if __name__ == "__main__":
    main()