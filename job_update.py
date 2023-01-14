from bs4 import BeautifulSoup
import requests
from tkinter import *
from tkinter import ttk
import webbrowser

# Stepstone elements and classes for BS
stepstone =	{
  "job_anzeige_element": "article",
  "job_anzeige_class": "resultlist-1jx3vjx",
  "job_titel_element": "a",
  "job_titel_class": "resultlist-1uvdp0v",
  "job_standort_element":"span",
  "job_standort_class":"resultlist-suri3e",
  "job_description_element": "div",
  "job_description_class": "resultlist-1fp8oay",
  "job_link_element":"a",
  "job_link_class":"resultlist-1uvdp0v",
  "url_de": "de/jobs/",
  "url_nl": "nl/work/",
  "url_be": "be/emplois/"
}

# Function to obtain job title and job link, and key word filtering using BS
def get_jobs(url, page_number, key_word):
    url_page = url + str(page_number)
    html_text = requests.get(url_page).text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all(stepstone["job_anzeige_element"],class_=stepstone["job_anzeige_class"])
    job_titles = []
    job_links = []
    for job in jobs:
        job_title = job.find(stepstone["job_titel_element"], class_=stepstone["job_titel_class"]).text
        job_description = job.find(stepstone["job_description_element"], class_=stepstone["job_description_class"]).text
        job_link = job.find(stepstone["job_link_element"], class_=stepstone["job_link_class"])['href']
        if key_word in job_title or key_word in job_description:
            job_titles.append(job_title)
            job_links.append(job_link)
    return job_titles, job_links

# Function to determine URL from Tkinter user input, BS output is shown in separate widget "finds"
def printValues(page_number):
    finds = Canvas(master, height = 900, width = 800)
    finds.place(x=0, y=100)
    finds['bg'] = '#ffbf00'
    description = job_description.get()
    country = job_country.get().lower()
    if country == "netherlands":
        country_url = stepstone["url_nl"]
    elif country == "belgium":
        country_url = stepstone["url_be"]
    else:
        country_url = stepstone["url_de"]
    location = job_location.get()
    description = job_company.get()
    key = key_word.get()
    recent = cb.get()
    only_recent = f"&action=facet_selected%3bage%3bage_7&ag=age_7" if recent == 1 else ""
    url = 'https://www.stepstone.' + country_url + description + '/in-' + location + '?radius=30&page=' + only_recent
    job_titles, job_links = get_jobs(url, page_number, key)
    
    # Add search output to finds widget
    key_string = f'with the key word {key_word.get()} ' if key != "" else ""
    location_string = f'around {location} ' if location != "" else ""
    page_offers = len(job_titles)
    Label(finds, text=f'{page_offers} {description} jobs {location_string}{key_string}found!', bg='#ffbf00').place(x=250, y=5)
    for i in range(page_offers):
        btn = ttk.Button(finds, text = job_titles[i], command=lambda: webbrowser.open_new("https://www.stepstone.de" + job_links[i]))
        btn.place(x=0, y= 50 + i*25)
    more_button = ttk.Button(finds,text="Search more jobs", command=lambda: printValues(page_number + 1))
    more_button.place(x=0, y= 0)
    if page_number > 1:
        previous_button = ttk.Button(finds,text="Previous page", command=lambda: printValues(page_number - 1))
        previous_button.place(x=100, y= 0)

# Initiate TK object
master = Tk()
master.title("StepStone Job Finder")
master.geometry('650x800')
master['bg'] = '#ffbf00'

# Labels
label_description = Label(master, text='Job description')
label_country = Label(master, text='Country')
label_region = Label(master, text='Region')
label_company = Label(master, text='Company')
label_key = Label(master, text='Key word')
label_recent = Label(master, text='Less than a week ago')

# Label positions
label_description.place(x=0,y=0)
label_country.place(x=0,y=25)
label_region.place(x=0,y=50)
label_company.place(x=0,y=75)
label_key.place(x=0,y=100)
label_recent.place(x=250,y=0)

# Input
job_description = Entry(master)
job_country = Entry(master)
job_location = Entry(master)
job_company = Entry(master)
key_word = Entry(master)
cb = IntVar()
only_latest = Checkbutton(master, variable=cb)

# Input positions
job_description.place(x=100,y=0)
job_country.place(x=100,y=25)
job_location.place(x=100,y=50)
job_company.place(x=100,y=75)
key_word.place(x=100,y=100)
only_latest.place(x=375,y=0)

# Submit button
page_number = 1
submit_button = ttk.Button(master,text="Submit", command=lambda: printValues(page_number))
submit_button.grid()
submit_button.place(x=250, y=70)

# Create finds widget
finds = Canvas(master, height = 900, width = 800)
finds.place(x=0, y=125)
finds['bg'] = '#ffbf00'

mainloop()
 