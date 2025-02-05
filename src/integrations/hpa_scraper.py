import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def table_to_markdown(table):
    """
    Convert HTML table to markdown format using pandas.
    """
    # Extract headers
    headers = []
    header_row = table.find('tr')
    if header_row:
        headers = [th.get_text().strip() for th in header_row.find_all(['th', 'td'])]
    
    # Extract rows
    rows = []
    for row in table.find_all('tr')[1:]:  # Skip header row
        cells = row.find_all(['td', 'th'])
        row_data = [cell.get_text().strip() for cell in cells]
        if row_data and len(row_data) == len(headers):
            rows.append(row_data)
    
    if headers and rows:
        try:
            df = pd.DataFrame(rows, columns=headers)
            return df.to_markdown(index=False) + '\n\n'
        except Exception as e:
            print(f"Error converting table: {e}")
            return "\n".join([" | ".join(row) for row in [headers] + rows]) + "\n\n"
    return ""

def html_to_markdown(element):
    """
    Convert HTML elements to markdown format.
    """
    if element.name is None:
        return element.string.strip() if element.string else ''
    
    text = ''
    
    if element.name == 'h1':
        text = f'\n# {element.get_text().strip()}\n\n'
    elif element.name == 'h2':
        text = f'\n## {element.get_text().strip()}\n\n'
    elif element.name == 'h3':
        text = f'\n### {element.get_text().strip()}\n\n'
    elif element.name == 'h4':
        text = f'\n#### {element.get_text().strip()}\n\n'
    elif element.name == 'p':
        # Preserve links within paragraphs
        content = ''
        for child in element.children:
            if child.name == 'a':
                href = child.get('href', '')
                if href:
                    content += f"[{child.get_text().strip()}]({href})"
                else:
                    content += child.get_text().strip()
            else:
                content += str(child.string) if child.string else ''
        text = f'{content.strip()}\n\n'
    elif element.name == 'table':
        text = table_to_markdown(element)
    elif element.name == 'ul':
        for li in element.find_all('li', recursive=False):
            text += f"* {li.get_text().strip()}\n"
        text += '\n'
    elif element.name == 'ol':
        for i, li in enumerate(element.find_all('li', recursive=False), 1):
            text += f"{i}. {li.get_text().strip()}\n"
        text += '\n'
    elif element.name == 'pre':
        code = element.find('code')
        language = code.get('class', [''])[0] if code and code.get('class') else ''
        content = code.get_text().strip() if code else element.get_text().strip()
        text = f"```{language}\n{content}\n```\n\n"
    elif element.name == 'code' and element.parent.name != 'pre':
        text = f'`{element.get_text().strip()}`'
    elif element.name == 'strong' or element.name == 'b':
        text = f"**{element.get_text().strip()}**"
    elif element.name == 'em' or element.name == 'i':
        text = f"*{element.get_text().strip()}*"
    
    return text

def scrape_to_markdown(url):
    """
    Scrapes a webpage and converts it to markdown format.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print("Fetching URL...")
    response = requests.get(url, headers=headers)
    print(f"Response status code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Remove unwanted elements
    for element in soup.find_all(['script', 'style', 'nav', 'footer', 'img']):
        element.decompose()
    
    # Find the main content area
    main_content = soup.find('div', class_='content-main')
    if not main_content:
        print("Couldn't find content-main, trying content...")
        main_content = soup.find('div', {'id': 'content'})
    if not main_content:
        print("Couldn't find specific content div, using entire body...")
        main_content = soup.find('body')
    if not main_content:
        print("Couldn't find body, using entire document...")
        main_content = soup
    
    print(f"Main content found: {bool(main_content)}")
    
    markdown_content = ''
    
    # Get all relevant elements
    elements = main_content.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'table', 'ul', 'ol', 'pre', 'code'], recursive=True)
    print(f"Found {len(elements)} elements to process")
    
    # Process each element
    for element in elements:
        print(f"Processing {element.name} element...")
        content = html_to_markdown(element)
        markdown_content += content
    
    print(f"Final markdown length: {len(markdown_content)}")
    return markdown_content

def main():
    url = "https://www.proteinatlas.org/about/download"
    markdown_content = scrape_to_markdown(url)
    
    # Save to markdown file
    with open('hpa_docs.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print("Content has been converted to markdown and saved to hpa_content.md")

if __name__ == "__main__":
    main()