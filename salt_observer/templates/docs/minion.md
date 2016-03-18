# Generelle Informationen

- Die installierte Version von **Salt** auf diesem Minion ist `{{ minion.grains.saltversion }}`

- Der installierte Kernel hat die Version `{{ minion.grains.kernelrelease }}`

- Das Betriebssystem ist ein `{{ minion.grains.os }} {{ minion.grains.osrelease }} {{ minion.grains.oscodename }}` und
hat ein aktuelles Bios vom {{ minion.grains.biosreleasedate }}.

- Dieser Minion hat **{{ minion.grains.num_cpus }} CPU's** und zugesicherten Arbeitsspeicher von **{{ minion.grains.mem_total }} Mb**

- Das CPU Modell ist `{{ minion.grains.osarch }} - {{ minion.grains.cpuarch }} - {{ minion.grains.cpu_model }}`


# Netzwerk Interfaces

{% block network-description %}{% endblock %}

{% if minion.networkinterface_set.all %}
| Interface | MAC address | IPv4 | Netmask |
|-----------|-------------|------|---------|
{% for network in minion.networkinterface_set.all %}| {{ network.name }} | {{ network.mac_address }} | {{ network.network.ipv4 }} | [{{ network.network.mask }}]({% url 'network-detail' network.network.ipv4 %}) |
{% endfor %}
{% else %}
Leider konnten wir keine Informationen über die Netzwerke dieses Minions abgreifen
{% endif %}

{% block else-description %}{% endblock %}
