from bs4 import BeautifulSoup

def html2txt(html_str):
    soup = BeautifulSoup(html_str, 'html.parser')    
    return soup.get_text()

