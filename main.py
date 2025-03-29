
from datetime import datetime
from urllib.request import urlopen
from parser import parser_content, create_calendar, save_calendar

year = datetime.now().year
url = f"https://der.es.gov.br/feriados-e-pontos-facultativos-{year}"
page = urlopen(url)
html = page.read().decode("utf-8")

calendar = create_calendar("Feriados Espírito Santo",
                           "Calendário de Feriados do Espírito Santo")

holidays_list = parser_content(html)

for holiday in holidays_list:
    calendar.add_component(holiday)

save_calendar(calendar)
