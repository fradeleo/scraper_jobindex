import requests
import lxml.html as lh
import pandas as pd
from helpers import printProgressBar
# Start your search on JobIndex and then copy the URL below

# Some examples:
#url = 'https://www.jobindex.dk/jobsoegning/kontor/oekonomi?q=%27financial+controller%27'
#url = 'https://www.jobindex.dk/jobsoegning/salg/salg?q=%27sales+manager%27'
#url = 'https://www.jobindex.dk/jobsoegning'
#url = 'https://www.jobindex.dk/jobsoegning?q=%27data+scientist%27' 

url = 'https://www.jobindex.dk/jobsoegning/kontor'

# Extracting the number of pages
url_n = url
url_list = []
next_page = True


while next_page:
        
    try:
        page = requests.get(url_n)
        doc = lh.fromstring(page.content)
        link = doc.xpath('//li[@class="page-item page-item-next"]//a/@href')
        url_n=str(link[0])
        url_list.append(url_n)
        next_page = True
        print('\rRetrieving number of pages: {} page(s) and counting...'.format(len(url_list)+1), end = '\r')
        
    except:
        next_page = False
        print("\nThere are {} pages listing results for your search".format(len(url_list)+1))
        
        
last = len(url_list)


# Extracting job titles and companies for each page

url = url+'?page={}' #adds the page element (with no page number) to the url
titles=[]
companies=[]
info=[]

    
for page_number in range(1, last+1):
    printProgressBar(page_number, last, prefix = 'Scraping...')
    #("Scraping page", page_number)
    #Make requests replacing 'page_number' in the curly brackets {} of the URL 
    url_page = url.format(page_number)
    #Create a handle, page, to handle the contents of the website
    page = requests.get(url_page)
    #Store the contents of the website under doc
    doc = lh.fromstring(page.content)
    #Parse data that are stored in the html elements with class "PaidJob"
    pj = doc.xpath('//div[@class="PaidJob"]')
    pj_titles = doc.xpath('//div[@class="PaidJob"]/a/b')
    pj_companies = doc.xpath('//div[@class="PaidJob"]/p[1]/a')
    pj_info = doc.xpath('//div[@class="PaidJob"]/p[1]/text()[2]')

    #Retrieve each title and append it to to the relative list
    for i in range(0,len(pj_titles)):
        #print(pj_titles[i].text_content())
        data = pj_titles[i].text_content()
        data = str(data)
        titles.append(data)
    
    #Retrieve each company name and append it to the relative list
    for i in range(0,len(pj_companies)):
        #print(pj_companies[i].text_content())
        data = pj_companies[i].text_content()
        data = str(data)
        companies.append(data)
    
    ##These lines are to extract the info on the side of the company name
    ##That information can either be a location or a string saying that the company is recruiting on behalf of somebody else
    #Retrieve each info and append it to the relative list
    for i in range(0,len(pj_info)):
        #print(pj_info[i])
        data = pj_info[i]
        data = str(data)
        data = str.lstrip((data.replace(",",""))) #lstrip removes leading whitespaces, newline and tab characters 
        info.append(data)
      
print("Scraping completed")
    

# Constructing the dataframe with the scraped data
data_tuples = list(zip(titles, companies, info))
df = pd.DataFrame(data_tuples, columns=['Titles','Companies','Info'])

# Exporting to csv
df.to_csv(r'job-results.csv', index = False, header=True)
