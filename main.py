import requests
from bs4 import BeautifulSoup
import pandas as pd
from pw import username, password

def login(session, login_url):    
    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.text, 'html.parser')
       
    logintoken = soup.find('input', {'name': 'logintoken'})['value']
        
    anchor = soup.find('input', {'name': 'anchor'})['value']
    
    payload = {
        'username': username,
        'password': password,
        'logintoken': logintoken,
        'anchor': anchor
    }
        
    response = session.post(login_url, data=payload)
    return response

def get_html(session, url):
    response = session.get(url)
    response.encoding = 'utf-8'
    return response.text

def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='flexible table table-striped table-hover generaltable generalbox')
    
    if not table:
        print("No table found on the page.")
        return [], []
    
    data = []
    headers = [header.text for header in table.find_all('th')]
    rows = table.find_all('tr')[1:] 
    for row in rows:
        cells = row.find_all('td')
        data.append([cell.text.strip() for cell in cells])
    
    return headers, data

def save_to_excel(headers, data, filename):
    df = pd.DataFrame(data, columns=headers)
    df.to_excel(filename, index=False)

def main():
    login_url = 'https://elearning.uin-malang.ac.id/login/index.php'  
    url = 'https://elearning.uin-malang.ac.id/mod/assign/view.php?id=92790&action=grading'
    page2= url + "&page=1"
    
    
    with requests.Session() as session:        
        login_response = login(session, login_url)
        if login_response.url != login_url: 
            html = get_html(session, url)
            html2 = get_html(session, page2)        
            headers, data = get_data(html)
            headers, data2 = get_data(html2)
            data.extend(data2)
            if headers and data:
                save_to_excel(headers, data)
            else:
                print("No data to save.")
        else:
            print("Login failed. Please check your credentials.")

if __name__ == '__main__':
    main()
