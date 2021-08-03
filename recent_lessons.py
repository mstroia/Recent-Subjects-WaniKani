import requests
import xlsxwriter
from fpdf import FPDF
from datetime import datetime
import sys


def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('fireflysung', '', 'fireflysung.ttf', uni=True)
    pdf.set_font('fireflysung', '', 14)

    pdf.cell(0, 10, 'WaniKani Recently Started Items', 0, 1, 'C')
    pdf.cell(35, 10, 'Type', 1, 0, 'C')
    pdf.cell(35, 10, 'Word', 1, 0, 'C')
    pdf.cell(45, 10, 'Reading', 1, 0, 'C')
    pdf.cell(0, 10, 'Meaning', 1, 1, 'C')
    for subject_type, word, reading, meaning in data:
        pdf.cell(35, 10, subject_type, 1, 0, 'C')
        pdf.cell(35, 10, word, 1, 0, 'C')
        pdf.cell(45, 10, reading, 1, 0, 'C')
        pdf.cell(0, 10, meaning, 1, 1, 'C')
    pdf.output('subjects.pdf', 'F')


def create_spreadsheet(data):
    workbook = xlsxwriter.Workbook("subjects.xlsx")
    worksheet = workbook.add_worksheet()
    row = 0
    worksheet.write(row, 0, "Type")
    worksheet.write(row, 1, "Word")
    worksheet.write(row, 2, "Reading")
    worksheet.write(row, 3, "Meaning")

    for subject_type, word, reading, meaning in data:
        row += 1
        worksheet.write(row, 0, subject_type)
        worksheet.write(row, 1, word)
        worksheet.write(row, 2, reading)
        worksheet.write(row, 3, meaning)

    workbook.close()


# Run the script by running recent_lessons <API Bearer Token>
headers = {"Authorization": "Bearer " + sys.argv[1]}

reviews = requests.get(url='https://api.wanikani.com/v2/review_statistics', headers=headers)
rev_list = list()
while reviews.json()['pages']['next_url']:
    next_url = reviews.json()['pages']['next_url']
    for x in reviews.json()['data']:
        rev_list.append(x)
    reviews = requests.get(url=next_url, headers=headers)
for x in reviews.json()['data']:
    rev_list.append(x)
rev_list = list(
    filter(lambda x: (
            (datetime.now() - datetime.strptime(x['data']['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')).days < 7
            and x['data']['subject_type'] != 'radical'
        ),
        rev_list
    )
)

subjects = list()
for x in rev_list:
    subject = requests.get(
        url='https://api.wanikani.com/v2/subjects/' + str(x['data']['subject_id']), headers=headers
    ).json()
    subjects.append([
        subject['object'],
        subject['data']['characters'],
        subject['data']['readings'][0]['reading'],
        subject['data']['meanings'][0]['meaning']
    ])

if sys.argv[2] == 'spreadsheet':
    create_spreadsheet(subjects)
else:
    # to generate PDFs, you need to have the fireflysung font ttf file in the same directory
    create_pdf(subjects)
