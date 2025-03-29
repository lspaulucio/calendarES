import os
from pathlib import Path
from datetime import datetime
from urllib.request import urlopen
from parser import parserContent, createCalendar

url = f"https://der.es.gov.br/feriados-e-pontos-facultativos-{datetime.now().year}"
page = urlopen(url)
html = page.read().decode("utf-8")

calendar = createCalendar("Feriados Espírito Santo",
                          "Calendário de Feriados do Espírito Santo")
holidays_list = parserContent(html)

for holiday in holidays_list:
    calendar.add_component(holiday)

# Write to disk
directory = Path.cwd() / 'CalendarES'
try:
    directory.mkdir(parents=True, exist_ok=False)
except FileExistsError:
    print("Folder already exists")
else:
    print("Folder was created")

with open(os.path.join(directory, 'calendarES.ics'), 'wb') as f:
    f.write(calendar.to_ical())
