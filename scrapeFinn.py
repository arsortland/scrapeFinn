from openpyxl.reader import excel
import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import pandas
from datetime import date
import os

sokeord = input("skriv inn ønsket søkeord for stillinger i Kristiansand: ")

URL = 'https://www.finn.no/job/fulltime/search.html?abTestKey=rerank&location=2.20001.22042.20179&q=frontend&sort=RELEVANCE'
NEWURL = URL.replace("frontend", sokeord)

page = requests.get(NEWURL)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find(id="page-results")
job_elements = results.find_all("article", class_="ads__unit")

jobbtittel = []
arbeidsgiver = []
beskrivelse = []
lenke = []

for job_element in job_elements:
    jobtitle = job_element.find("a", class_="ads__unit__link")
    jobgiver = job_element.find("div", class_="ads__unit__content__list")
    jobdescription = job_element.find("div", class_="ads__unit__content__keys")
    joblink = job_element.find("a", href=True)
    jobbtittel.append(jobtitle.text)
    arbeidsgiver.append(jobgiver.text)
    lenke.append(joblink['href'])
    if jobdescription == None:  #behov for denne for med None verdier får jeg traceback.
        beskrivelse.append("Ingen beskrivelse funnet")
    else:
        beskrivelse.append(jobdescription.text)

df = pandas.DataFrame({'Dato' : date.today(),'Tittel' : jobbtittel, 'Arbeidsgiver' : arbeidsgiver, 'Arbeidsbeskrivelse' : beskrivelse, 'Søkelink' : lenke})
filename = '%s.xlsx'% sokeord
if os.path.exists(filename) == True:
    try:
        with pandas.ExcelWriter(filename, mode='a', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=str(date.today()))
    except ValueError:
        print("Søk allerede gjort i dag på dette sokeordet. Vent til i morgen og prøv igjen.")
else:
    df.to_excel(filename, sheet_name=str(date.today()))