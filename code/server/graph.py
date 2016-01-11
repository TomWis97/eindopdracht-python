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
    plt.clf()
    #plt = matplotlib.pyplot
    # TODO RAM Graph fixen
    ding = agent_module.agent(ip)
    history = database.get_history(ding.ip, item)
    history_time = []
    history_value = []
    for history_item in history:
        history_time.append(datetime.datetime.fromtimestamp(history_item[0]).strftime("%d-%m %H:%M"))
        history_value.append(history_item[1])
    #print("History_time", history_time)
    #print("History_value", history_value)

    # print("Debug:", item)
    # print("History_time:", history_time)
    # print("History_value:", history_value)

    if len(history_value) == 0:
        return ''

    plt.gcf().subplots_adjust(bottom=0.15)
    plt.plot(history_value, linewidth=2.0)
    plt.xticks(range(len(history_time)), history_time, rotation=45)
    plt.title(item)
    plt.ylim(0, plt.ylim()[0] + 5)
    # Aangezien sommige waardes speciale dingen nodig hebben in de grafiek, hier een lelijke zooi if-jes.
    if item == 'cpu_load':
        plt.ylim(0, 100)
    elif item == 'no_processes':
        plt.ylim(0, max(history_value) + 10)
    elif item == 'ram_free':
        plt.ylim(0, max(history_value) + 100)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=48, transparent=True)
    buf.seek(0)
    base64_img = base64.b64encode(buf.getvalue())
    buf.seek(0)
    data = buf.read()
    buf.close()
    f = open('copy.png', 'wb')
    f.write(data)
    f.close()
    return '<img class="graph" id="%s" src="data:image/png;base64, %s"/>' % (item, base64_img.decode('ASCII'))
#print(base64_img)

#plt.savefig('myfig')
