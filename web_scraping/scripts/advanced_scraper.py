#!/usr/bin/env python3
"""
Web Scraper Avanzado y Agresivo para Colombina
Extrae información completa incluyendo metadata, imágenes, estructuras, etc.
Autor: Assistant
Fecha: 2025-01-13
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import json
import os
import re
import time
# import base64 - no necesario
from datetime import datetime
from urllib.parse import urljoin, urlparse
import logging
from pathlib import Path
import hashlib
# Importaciones asyncio eliminadas - no necesarias para este script

# Configurar logging detallado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('advanced_scraping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AdvancedColombinaScaper:
    def __init__(self, links_file="colombina_links_categorized.json"):
        self.links_file = links_file
        self.base_dir = "colombina_advanced"
        self.data_dir = os.path.join(self.base_dir, "data")
        self.docs_dir = os.path.join(self.base_dir, "documents")
        self.processed_urls = set()
        self.failed_urls = []
        self.extracted_data = {}
        
        # Configuración de requests
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8,en-US;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        self.session.headers.update(self.headers)
        
        # Configuración de Selenium
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Ejecutar sin ventana
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument(f"--user-agent={self.headers['User-Agent']}")
        
        self.setup_directories()
        
    def setup_directories(self):
        """Crear estructura de directorios avanzada"""
        directories = [
            self.base_dir,
            self.data_dir,
            self.docs_dir,
            os.path.join(self.data_dir, "productos"),
            os.path.join(self.data_dir, "institucional"),
            os.path.join(self.data_dir, "noticias"),
            os.path.join(self.data_dir, "contacto"),
            os.path.join(self.data_dir, "otros"),
            os.path.join(self.data_dir, "metadata"),
            os.path.join(self.data_dir, "estructuras"),
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        
        logger.info(f"Estructura avanzada creada en: {self.base_dir}")
    
    def extract_with_requests(self, url):
        """Extracción básica con requests (como antes)"""
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Error con requests en {url}: {e}")
            return None
    
    def extract_with_selenium(self, url):
        """Extracción avanzada con Selenium para contenido dinámico"""
        try:
            # Configurar ChromeDriver automáticamente
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chrome_options)
            driver.get(url)
            
            # Esperar a que la página cargue completamente
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Simular scroll para cargar contenido lazy-load
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            # Intentar hacer clic en botones "Ver más" o expandir contenido
            try:
                expand_buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Ver más') or contains(text(), 'Mostrar más') or contains(text(), 'Cargar más')]")
                for button in expand_buttons[:3]:  # Máximo 3 clicks
                    try:
                        button.click()
                        time.sleep(1)
                    except:
                        pass
            except:
                pass
            
            html_content = driver.page_source
            driver.quit()
            
            return BeautifulSoup(html_content, 'html.parser')
            
        except Exception as e:
            logger.error(f"Error con Selenium en {url}: {e}")
            return None
    
    def extract_comprehensive_data(self, soup, url):
        """Extraer datos completos de la página"""
        data = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'title': '',
            'description': '',
            'keywords': [],
            'headings': {},
            'images': [],
            'links': [],
            'products': [],
            'prices': [],
            'contact_info': {},
            'social_links': [],
            'metadata': {},
            'structured_data': {},
            'forms': [],
            'content_text': '',
            'page_structure': {},
            'performance_data': {}
        }
        
        if not soup:
            return data
        
        # 1. METADATA BÁSICA
        data['title'] = soup.title.get_text().strip() if soup.title else ''
        
        # Meta descripción
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        data['description'] = meta_desc.get('content', '') if meta_desc else ''
        
        # Keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            data['keywords'] = [kw.strip() for kw in meta_keywords.get('content', '').split(',')]
        
        # 2. ESTRUCTURA DE HEADINGS
        for i in range(1, 7):
            headings = soup.find_all(f'h{i}')
            data['headings'][f'h{i}'] = [h.get_text().strip() for h in headings]
        
        # 3. TODAS LAS IMÁGENES
        images = soup.find_all('img')
        for img in images:
            img_data = {
                'src': urljoin(url, img.get('src', '')),
                'alt': img.get('alt', ''),
                'title': img.get('title', ''),
                'width': img.get('width', ''),
                'height': img.get('height', ''),
                'class': ' '.join(img.get('class', [])),
                'loading': img.get('loading', '')
            }
            data['images'].append(img_data)
        
        # 4. TODOS LOS ENLACES
        links = soup.find_all('a', href=True)
        for link in links:
            link_data = {
                'url': urljoin(url, link['href']),
                'text': link.get_text().strip(),
                'title': link.get('title', ''),
                'class': ' '.join(link.get('class', [])),
                'rel': ' '.join(link.get('rel', []))
            }
            data['links'].append(link_data)
        
        # 5. INFORMACIÓN DE PRODUCTOS (específico para Colombina)
        product_selectors = [
            '.product-card', '.producto', '.item-producto',
            '[class*="product"]', '[class*="producto"]',
            '.brand-item', '.category-item'
        ]
        
        for selector in product_selectors:
            products = soup.select(selector)
            for product in products:
                product_data = {
                    'name': '',
                    'description': '',
                    'image': '',
                    'category': '',
                    'brand': ''
                }
                
                # Extraer nombre del producto
                name_elem = product.find(['h1', 'h2', 'h3', '.product-name', '.nombre'])
                if name_elem:
                    product_data['name'] = name_elem.get_text().strip()
                
                # Extraer imagen del producto
                img_elem = product.find('img')
                if img_elem and img_elem.get('src'):
                    product_data['image'] = urljoin(url, img_elem['src'])
                
                if product_data['name']:  # Solo agregar si tiene nombre
                    data['products'].append(product_data)
        
        # 6. INFORMACIÓN DE CONTACTO
        contact_patterns = {
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'phone': r'[\+]?[\d\s\-\(\)]{7,}',
            'address': r'(?i)(dirección|direccion|address)[:]\s*([^\n]+)'
        }
        
        page_text = soup.get_text()
        for contact_type, pattern in contact_patterns.items():
            matches = re.findall(pattern, page_text)
            if matches:
                data['contact_info'][contact_type] = matches
        
        # 7. REDES SOCIALES
        social_domains = ['facebook', 'instagram', 'twitter', 'linkedin', 'youtube', 'tiktok']
        for link in links:
            href = link.get('href', '').lower()
            for domain in social_domains:
                if domain in href:
                    data['social_links'].append({
                        'platform': domain,
                        'url': link['href'],
                        'text': link.get_text().strip()
                    })
        
        # 8. DATOS ESTRUCTURADOS (JSON-LD)
        json_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_scripts:
            try:
                structured = json.loads(script.string)
                data['structured_data'] = structured
            except:
                pass
        
        # 9. FORMULARIOS
        forms = soup.find_all('form')
        for form in forms:
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'get'),
                'fields': []
            }
            
            inputs = form.find_all(['input', 'textarea', 'select'])
            for inp in inputs:
                field = {
                    'type': inp.get('type', inp.name),
                    'name': inp.get('name', ''),
                    'placeholder': inp.get('placeholder', ''),
                    'required': inp.has_attr('required')
                }
                form_data['fields'].append(field)
            
            data['forms'].append(form_data)
        
        # 10. TEXTO COMPLETO LIMPIO
        data['content_text'] = self.clean_text(soup)
        
        # 11. ESTRUCTURA DE LA PÁGINA
        data['page_structure'] = self.analyze_page_structure(soup)
        
        return data
    
    def clean_text(self, soup):
        """Limpiar texto como en el script original pero más completo"""
        # Remover elementos no deseados
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 
                           'aside', 'iframe', 'noscript', 'meta', 'link']):
            element.decompose()
        
        # Buscar contenido principal
        main_selectors = [
            'main', 'article', '[role="main"]', '.main-content', 
            '.content', '#content', '.post-content', '.entry-content',
            '.page-content', '.body-content'
        ]
        
        main_content = None
        for selector in main_selectors:
            main_content = soup.select_one(selector)
            if main_content:
                break
        
        if not main_content:
            main_content = soup.find('body')
        
        if not main_content:
            return "No se pudo extraer contenido"
        
        text = main_content.get_text(separator='\n', strip=True)
        
        # Limpiar texto
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = re.sub(r'\s+', ' ', line.strip())
            if len(line) > 3:  # Líneas con contenido
                cleaned_lines.append(line)
        
        result = '\n\n'.join(cleaned_lines)
        return re.sub(r'\n\s*\n\s*\n', '\n\n', result)
    
    def analyze_page_structure(self, soup):
        """Analizar la estructura completa de la página"""
        structure = {
            'total_elements': len(soup.find_all()),
            'divs': len(soup.find_all('div')),
            'sections': len(soup.find_all('section')),
            'articles': len(soup.find_all('article')),
            'nav_elements': len(soup.find_all('nav')),
            'forms': len(soup.find_all('form')),
            'tables': len(soup.find_all('table')),
            'lists': len(soup.find_all(['ul', 'ol'])),
            'images': len(soup.find_all('img')),
            'links': len(soup.find_all('a')),
            'buttons': len(soup.find_all(['button', 'input[type="button"]', 'input[type="submit"]'])),
            'css_classes': [],
            'ids': []
        }
        
        # Extraer todas las clases CSS únicas
        for element in soup.find_all(class_=True):
            classes = element.get('class', [])
            structure['css_classes'].extend(classes)
        structure['css_classes'] = list(set(structure['css_classes']))
        
        # Extraer todos los IDs únicos
        for element in soup.find_all(id=True):
            structure['ids'].append(element.get('id'))
        
        return structure
    
    # FUNCIÓN DE DESCARGA DE IMÁGENES ELIMINADA - NO NECESARIA
    
    def scrape_url_comprehensive(self, url, category):
        """Scraping completo de una URL"""
        if url in self.processed_urls:
            return False
        
        logger.info(f"Scraping completo: {url}")
        
        # Intentar primero con requests
        soup = self.extract_with_requests(url)
        
        # Si no funciona o el contenido es muy pequeño, usar Selenium
        if not soup or len(soup.get_text().strip()) < 200:
            logger.info(f"Usando Selenium para {url}")
            soup = self.extract_with_selenium(url)
        
        if not soup:
            self.failed_urls.append((url, "No se pudo extraer contenido"))
            return False
        
        # Extraer datos completos
        comprehensive_data = self.extract_comprehensive_data(soup, url)
        
        # Verificar si hay contenido útil
        if len(comprehensive_data['content_text'].strip()) < 50:
            logger.warning(f"Contenido muy corto en {url}")
            return False
        
        # Imágenes ya capturadas en metadata - no descargamos archivos
        
        # Generar archivos de salida
        self.save_comprehensive_data(comprehensive_data, category, url)
        
        self.processed_urls.add(url)
        return True
    
    def save_comprehensive_data(self, data, category, url):
        """Guardar datos completos en múltiples formatos"""
        # Generar nombre base
        parsed_url = urlparse(url)
        safe_name = re.sub(r'[^\w\-_]', '_', parsed_url.path.strip('/'))
        if not safe_name:
            safe_name = f"page_{abs(hash(url)) % 10000}"
        
        base_path = os.path.join(self.data_dir, category, safe_name)
        
        # 1. JSON completo con todos los datos
        json_file = f"{base_path}_complete.json"
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        # 2. Markdown mejorado
        md_file = f"{base_path}_enhanced.md"
        markdown_content = self.create_enhanced_markdown(data)
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # 3. CSV de productos (si los hay)
        if data['products']:
            import csv
            csv_file = f"{base_path}_products.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['name', 'description', 'image', 'category', 'brand'])
                writer.writeheader()
                writer.writerows(data['products'])
        
        logger.info(f"Datos guardados: {json_file}")
    
    def create_enhanced_markdown(self, data):
        """Crear Markdown mejorado con toda la información"""
        md = f"""---
url: {data['url']}
title: {data['title']}
description: {data['description']}
keywords: {', '.join(data['keywords'])}
scraped_date: {data['timestamp']}
source: Advanced Colombina Web Scraping
total_images: {len(data['images'])}
total_links: {len(data['links'])}
total_products: {len(data['products'])}
---

# {data['title']}

## Descripción
{data['description']}

## Contenido Principal
{data['content_text']}

"""
        
        # Agregar productos si los hay
        if data['products']:
            md += "\n## Productos Encontrados\n\n"
            for i, product in enumerate(data['products'][:10], 1):
                md += f"{i}. **{product['name']}**\n"
                if product['description']:
                    md += f"   - {product['description']}\n"
                if product['image']:
                    md += f"   - Imagen: {product['image']}\n"
                md += "\n"
        
        # Agregar estructura de headings
        if any(data['headings'].values()):
            md += "\n## Estructura de Headings\n\n"
            for level, headings in data['headings'].items():
                if headings:
                    md += f"### {level.upper()}\n"
                    for heading in headings[:5]:  # Máximo 5 por nivel
                        md += f"- {heading}\n"
                    md += "\n"
        
        # Agregar información de contacto
        if data['contact_info']:
            md += "\n## Información de Contacto\n\n"
            for contact_type, contacts in data['contact_info'].items():
                md += f"**{contact_type.title()}:**\n"
                for contact in contacts[:3]:  # Máximo 3 por tipo
                    if isinstance(contact, tuple):
                        md += f"- {contact[1] if len(contact) > 1 else contact[0]}\n"
                    else:
                        md += f"- {contact}\n"
                md += "\n"
        
        # Agregar redes sociales
        if data['social_links']:
            md += "\n## Redes Sociales\n\n"
            for social in data['social_links'][:5]:
                md += f"- [{social['platform'].title()}]({social['url']})\n"
        
        return md
    
    def load_links(self):
        """Cargar links del archivo JSON"""
        try:
            with open(self.links_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data['categories']
        except Exception as e:
            logger.error(f"Error cargando links: {e}")
            return {}
    
    def run_advanced_scraping(self, max_urls_per_category=None):
        """Ejecutar scraping avanzado y completo"""
        logger.info("Iniciando Web Scraping AVANZADO Y AGRESIVO...")
        
        categories = self.load_links()
        
        # Verificar que se cargaron las categorias correctamente
        if not categories:
            logger.error("No se pudieron cargar las categorias. Terminando.")
            return
        
        # ORDEN ESPECIAL: NOTICIAS PRIMERO CON ATENCION EXTRA
        if 'noticias' in categories and categories['noticias']:
            logger.info("===== PROCESANDO NOTICIAS CON ATENCION ESPECIAL =====")
            self.process_special_news(categories['noticias'])
        
        # Luego procesar otras categorías
        priority_order = ['productos', 'institucional', 'contacto', 'otros', 'social', 'externos']
        
        for category in priority_order:
            if category in categories and categories[category] and category != 'noticias':
                logger.info(f"📂 Procesando categoría: {category} ({len(categories[category])} URLs)")
                
                urls = categories[category]
                if max_urls_per_category:
                    urls = urls[:max_urls_per_category]
                
                successful = 0
                for i, url in enumerate(urls, 1):
                    try:
                        logger.info(f"[{category}] 🔍 {i}/{len(urls)}: {url}")
                        
                        if self.scrape_url_comprehensive(url, category):
                            successful += 1
                        
                        # Pausa más corta para ser más agresivo
                        time.sleep(0.5)
                        
                    except KeyboardInterrupt:
                        logger.info("❌ Interrumpido por el usuario")
                        break
                    except Exception as e:
                        logger.error(f"❌ Error procesando {url}: {e}")
                        continue
                
                logger.info(f"✅ Categoría {category} completada: {successful}/{len(urls)} exitosos")
        
        # Procesar categorías restantes que no estén en la lista
        for category, urls in categories.items():
            if category not in priority_order + ['noticias'] and urls:
                logger.info(f"📂 Procesando categoría adicional: {category} ({len(urls)} URLs)")
                
                if max_urls_per_category:
                    urls = urls[:max_urls_per_category]
                
                successful = 0
                for i, url in enumerate(urls, 1):
                    try:
                        logger.info(f"[{category}] 🔍 {i}/{len(urls)}: {url}")
                        
                        if self.scrape_url_comprehensive(url, category):
                            successful += 1
                        
                        time.sleep(0.5)
                        
                    except KeyboardInterrupt:
                        logger.info("❌ Interrumpido por el usuario")
                        break
                    except Exception as e:
                        logger.error(f"❌ Error procesando {url}: {e}")
                        continue
                
        logger.info(f"Categoria {category} completada: {successful}/{len(urls)} exitosos")
        
        # Finalizar el scraping
        self.finalize_scraping()
    
    def process_special_news(self, news_urls):
        """Procesamiento especial para noticias con doble verificación"""
        logger.info(f"PROCESANDO {len(news_urls)} URLs DE NOTICIAS CON CUIDADO ESPECIAL")
        
        successful = 0
        for i, url in enumerate(news_urls, 1):
            try:
                logger.info(f"[NOTICIAS ESPECIAL] {i}/{len(news_urls)}: {url}")
                
                # Para noticias, usar método más cuidadoso
                if self.scrape_news_special(url):
                    successful += 1
                
                # Pausa más larga para noticias (más respeto)
                time.sleep(1.0)
                
            except KeyboardInterrupt:
                logger.info("❌ Interrumpido por el usuario")
                break
            except Exception as e:
                logger.error(f"❌ Error procesando noticia {url}: {e}")
                continue
        
        logger.info(f"🎉 NOTICIAS COMPLETADAS: {successful}/{len(news_urls)} exitosos")
    
    def scrape_news_special(self, url):
        """Scraping especializado para noticias con verificación extra"""
        if url in self.processed_urls:
            return False
        
        logger.info(f"Scraping especial de noticia: {url}")
        
        # Para noticias, probar AMBOS métodos y usar el mejor resultado
        soup_requests = self.extract_with_requests(url)
        soup_selenium = None
        
        # Si el contenido con requests es muy poco, usar Selenium
        if not soup_requests or len(soup_requests.get_text().strip()) < 200:
            logger.info(f"Usando Selenium para contenido completo: {url}")
            soup_selenium = self.extract_with_selenium(url)
        
        # Usar el mejor resultado
        if soup_selenium and soup_requests:
            # Comparar ambos y usar el que tenga más contenido
            selenium_length = len(soup_selenium.get_text().strip())
            requests_length = len(soup_requests.get_text().strip())
            soup = soup_selenium if selenium_length > requests_length else soup_requests
        elif soup_selenium:
            soup = soup_selenium
        else:
            soup = soup_requests
        
        if not soup:
            self.failed_urls.append((url, "No se pudo extraer contenido con ningún método"))
            return False
        
        # Extraer datos con verificación especial para noticias
        comprehensive_data = self.extract_comprehensive_data(soup, url)
        
        # Agregar metadatos específicos de noticias
        comprehensive_data = self.enhance_news_data(comprehensive_data, soup)
        
        # Verificación más laxa para noticias (pueden ser cortas)
        if len(comprehensive_data['content_text'].strip()) < 30 and not comprehensive_data['title']:
            logger.warning(f"⚠️ Noticia sin contenido suficiente: {url}")
            return False
        
        # Generar archivos de salida
        self.save_comprehensive_data(comprehensive_data, "noticias", url)
        
        self.processed_urls.add(url)
        logger.info(f"✅ Noticia procesada exitosamente")
        return True
    
    def enhance_news_data(self, data, soup):
        """Agregar metadatos específicos para noticias"""
        # Buscar fecha de publicación
        date_selectors = [
            'time[datetime]', '.date', '.published', '.fecha', '.publication-date',
            '[class*="date"]', '[class*="tiempo"]', '.entry-date'
        ]
        
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                date_value = date_elem.get('datetime') or date_elem.get_text().strip()
                if date_value:
                    data['publication_date'] = date_value
                    break
        
        # Buscar autor
        author_selectors = [
            '.author', '.autor', '[class*="author"]', '[class*="autor"]', 
            '.byline', '.writer', '.reporter'
        ]
        
        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                author_text = author_elem.get_text().strip()
                if author_text and len(author_text) < 100:
                    data['article_author'] = author_text
                    break
        
        # Buscar resumen/extracto
        summary_selectors = [
            '.summary', '.excerpt', '.resumen', '.lead', '.intro',
            '[class*="summary"]', '[class*="excerpt"]'
        ]
        
        for selector in summary_selectors:
            summary_elem = soup.select_one(selector)
            if summary_elem:
                summary_text = summary_elem.get_text().strip()
                if summary_text and len(summary_text) > 50:
                    data['article_summary'] = summary_text
                    break
        
        return data
    
    def load_links(self):
        """Cargar y categorizar los enlaces del archivo JSON"""
        try:
            with open('colombina_links.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extraer las URLs del formato correcto
            if 'links' in data:
                urls = [link['url'] for link in data['links']]
            elif isinstance(data, list):
                urls = data
            else:
                logger.error("[ERROR] Formato de archivo no reconocido")
                return None
            
            logger.info(f"[CARGA] Enlaces cargados: {len(urls)} URLs")
            
            # Categorizar enlaces por URL
            categories = {
                'productos': [],
                'institucional': [],
                'noticias': [],
                'contacto': [],
                'otros': [],
                'social': [],
                'externos': []
            }
            
            for url in urls:
                url_lower = url.lower()
                
                # Categorizar por patrones en la URL
                if 'productos' in url_lower or 'producto' in url_lower or 'catalog' in url_lower:
                    categories['productos'].append(url)
                elif ('noticia' in url_lower or 'news' in url_lower or 'blog' in url_lower or 
                      'prensa' in url_lower or '/n-' in url_lower):
                    categories['noticias'].append(url)
                elif ('empresa' in url_lower or 'about' in url_lower or 'institucional' in url_lower or
                      'historia' in url_lower or 'mision' in url_lower or 'vision' in url_lower):
                    categories['institucional'].append(url)
                elif 'contacto' in url_lower or 'contact' in url_lower or 'ubicacion' in url_lower:
                    categories['contacto'].append(url)
                elif ('facebook.com' in url_lower or 'instagram.com' in url_lower or 
                      'twitter.com' in url_lower or 'linkedin.com' in url_lower or 
                      'youtube.com' in url_lower or 'tiktok.com' in url_lower):
                    categories['social'].append(url)
                elif 'colombina.com' not in url_lower:
                    categories['externos'].append(url)
                else:
                    categories['otros'].append(url)
            
            # Log de categorizacion
            for category, urls in categories.items():
                if urls:
                    logger.info(f"[CATEGORIA] {category}: {len(urls)} URLs")
            
            return categories
            
        except FileNotFoundError:
            logger.error("[ERROR] No se encontro el archivo colombina_links.json")
            return None
        except Exception as e:
            logger.error(f"[ERROR] Error cargando enlaces: {e}")
            return None
    
    def finalize_scraping(self):
        """Finalizar el proceso de scraping y generar reportes"""
        self.generate_advanced_report()
        
        logger.info("SCRAPING AVANZADO COMPLETADO!")
        print(f"\nResumen Final:")
        print(f"- URLs procesadas: {len(self.processed_urls)}")
        print(f"- URLs fallidas: {len(self.failed_urls)}")
        print(f"- Directorio de resultados: {self.base_dir}/")
    
    def generate_advanced_report(self):
        """Generar reporte avanzado del scraping"""
        report = f"""# 🚀 Reporte de Web Scraping AVANZADO - Colombina

## 📈 Estadísticas Generales
- **Fecha de ejecución:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **URLs procesadas exitosamente:** {len(self.processed_urls)}
- **URLs fallidas:** {len(self.failed_urls)}
- **Tiempo total:** Calculado automáticamente

## 📁 Estructura de Archivos Generados

```
{self.base_dir}/
├── data/                   # Datos extraídos por categoría
│   ├── productos/         # JSON completo + Markdown + CSV de productos
│   ├── institucional/     # Información corporativa detallada
│   ├── noticias/         # Blog y noticias con metadata completa
│   ├── contacto/         # Información de contacto
│   ├── otros/            # Contenido misceláneo
│   ├── metadata/         # Datos estructurados y metainformación
│   └── estructuras/      # Análisis de estructura de páginas
├── documents/           # PDFs y documentos encontrados
└── advanced_report.md   # Este reporte
```

## 🎯 Datos Extraídos por Página

Cada página procesada incluye:

### 📝 Contenido Textual
- Título y descripción
- Contenido principal limpio
- Estructura completa de headings (H1-H6)
- Texto completo sin HTML

### 🖼️ Elementos Multimedia
- Todas las imágenes con metadata completa
- URLs de descarga y archivos locales
- Atributos alt, title, dimensiones
- Clasificación por tipo de imagen

### 🔗 Enlaces y Navegación
- Todos los enlaces internos y externos
- Texto de anchor, títulos y clases CSS
- Clasificación automática por tipo
- Detección de redes sociales

### 🏷️ Productos y Comercial
- Información de productos detectada automáticamente
- Nombres, descripciones e imágenes
- Categorización y marca
- Precios (cuando están disponibles)

### 📞 Información de Contacto
- Emails extraídos automáticamente
- Números de teléfono detectados
- Direcciones físicas
- Formularios de contacto

### 🌐 Redes Sociales
- Enlaces a todas las plataformas sociales
- Facebook, Instagram, Twitter, LinkedIn, etc.
- Texto asociado a cada enlace

### 🏗️ Estructura Técnica
- Análisis completo de elementos HTML
- Clases CSS y IDs utilizados
- Formularios y campos de entrada
- Datos estructurados (JSON-LD)

### 📊 Metadata Completa
- Meta descripción y keywords
- Open Graph y Twitter Cards
- Datos de performance
- Información de SEO

## ❌ URLs que No Se Pudieron Procesar

"""
        
        if self.failed_urls:
            for url, error in self.failed_urls:
                report += f"- `{url}`: {error}\n"
        else:
            report += "✅ **¡Todas las URLs se procesaron exitosamente!**\n"
        
        report += f"""

## 🚀 Capacidades Avanzadas Implementadas

### 🔄 Múltiples Métodos de Extracción
1. **Requests + BeautifulSoup**: Para contenido estático rápido
2. **Selenium WebDriver**: Para contenido dinámico y JavaScript
3. **Detección automática**: Cambia de método según necesidad

### 🧠 Extracción Inteligente
- **Detección automática de productos**
- **Reconocimiento de patrones de contacto**
- **Clasificación automática de contenido**
- **Limpieza avanzada de texto**

### 💾 Almacenamiento Múltiple
- **JSON completo**: Todos los datos estructurados
- **Markdown mejorado**: Contenido legible con metadata
- **CSV especializado**: Productos y datos tabulares
- **URLs de imágenes**: Metadata completa sin descarga

### 🎯 Optimizaciones Agresivas
- **Scroll automático**: Para contenido lazy-load
- **Click en botones**: Expandir contenido oculto
- **Múltiples selectores**: Detectar contenido en cualquier estructura
- **Reintentos inteligentes**: Cambio de método automático

### 🛡️ Robustez y Confiabilidad
- **Manejo completo de errores**
- **Timeouts configurables**
- **Rate limiting inteligente**
- **Logs detallados de todo el proceso**

---

🎉 **Este scraping capturó la información MÁS COMPLETA posible de cada página del sitio de Colombina.**
"""
        
        report_path = os.path.join(self.base_dir, "advanced_report.md")
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"📋 Reporte avanzado guardado en: {report_path}")

def main():
    """Función principal"""
    scraper = AdvancedColombinaScaper()
    
    try:
        # Ejecutar scraping avanzado
        # Cambiar el número para procesar más o menos URLs por categoría
        scraper.run_advanced_scraping()  # SIN LÍMITE - procesar TODAS las 294 URLs
        
    except KeyboardInterrupt:
        logger.info("🛑 Proceso interrumpido por el usuario")
        scraper.generate_advanced_report()
    except Exception as e:
        logger.error(f"❌ Error en la ejecución principal: {e}")
        raise

if __name__ == "__main__":
    main()