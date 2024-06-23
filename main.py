from bs4 import BeautifulSoup
import requests


def get_html(url):
    response = requests.get(url)
    return response.text

def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    # extract table
    table = soup.find_('table', class_='flexible table table-striped table-hover generaltable generalbox')
    # save as xlsx
    with open('data.xlsx', 'w') as f:
        f.write(str(table))
    
    

def main():
    url = 'https://elearning.uin-malang.ac.id/mod/assign/view.php?action=grading&id=92790&tsort=timesubmitted&tdir=4'
    html = get_html(url)
    data = get_data(html)
    print(data)

if __name__ == '__main__':
    main()