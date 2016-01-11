#!/usr/bin/env python3
import database
import agent_module
import matplotlib
matplotlib.use('Agg')
import base64
import datetime
import matplotlib.pyplot as plt
import io

def create_graph(ip, item):
    """Bak een grafiek van een item en data."""
    plt.clf() # Plot leegmaken, zodat we fris kunnen beginnen. Nodig als de functie al een keer eerder is aangeroepen, maar kan geen kwaad.
    # TODO RAM Graph fixen
    ding = agent_module.agent(ip) # Agent module aanroepen.
    history = database.get_history(ding.ip, item) # Geschiedenis opvragen.
    history_time = []
    history_value = []
    for history_item in history:
        history_time.append(datetime.datetime.fromtimestamp(history_item[0]).strftime("%d-%m %H:%M")) # Tijd mooi maken.
        history_value.append(history_item[1])

    if len(history_value) == 0:
        # Als er geen geschiedenis is, hoeven we ook geen grafiek te maken.
        return ''

    plt.gcf().subplots_adjust(bottom=0.15) # Beetje meer ruimte aan de onderkant maken.
    plt.plot(history_value, linewidth=2.0) # Tekenen.
    plt.xticks(range(len(history_time)), history_time, rotation=45) # Dingetjes op de x-as zetten.
    plt.title(item)
    plt.ylim(0, plt.ylim()[0] + 5) # Y-as limieten instellen.
    # Aangezien sommige waardes speciale dingen nodig hebben in de grafiek, hier een lelijke zooi if-jes.
    if item == 'cpu_load':
        plt.ylim(0, 100)
    elif item == 'no_processes':
        plt.ylim(0, max(history_value) + 10)
    elif item == 'ram_free':
        plt.ylim(0, max(history_value) + 100)
    buf = io.BytesIO() # Met BytesIO kunnen we een variabele misbr... gebruiken als file.
    plt.savefig(buf, format="png", dpi=48, transparent=True) # Opslaan naar file.
    buf.seek(0)
    base64_img = base64.b64encode(buf.getvalue())
    #buf.seek(0)
    #data = buf.read()
    buf.close()
    #f = open('copy.png', 'wb')
    #f.write(data)
    #f.close()
    return '<img class="graph" id="%s" src="data:image/png;base64, %s"/>' % (item, base64_img.decode('ASCII'))
#print(base64_img)

#plt.savefig('myfig')
