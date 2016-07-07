# Generelle Informationen

- Die installierte Version von **Salt** auf diesem Minion ist `{{ minion.data.grains.saltversion }}`

- Der installierte Kernel hat die Version `{{ minion.data.grains.kernelrelease }}`

- Das Betriebssystem ist ein `{{ minion.data.grains.os }} {{ minion.data.grains.osrelease }} {{ minion.data.grains.oscodename }}` und
hat ein aktuelles Bios vom {{ minion.data.grains.biosreleasedate }}.

- Dieser Minion hat **{{ minion.data.grains.num_cpus }} CPU's** und zugesicherten Arbeitsspeicher von **{{ minion.data.grains.mem_total }} Mb**

- Das CPU Modell ist `{{ minion.data.grains.osarch }} - {{ minion.data.grains.cpuarch }} - {{ minion.data.grains.cpu_model }}`


# Network Interfaces

{% block network-description %}{% endblock %}

{% if minion.networkinterface_set.all %}
| Interface | MAC address | IPv4 | Netmask |
|-----------|-------------|------|---------|
{% for network in minion.networkinterface_set.all %}| {{ network.name }} | {{ network.mac_address }} | {{ network.network.ipv4 }} | [{{ network.network.mask }}]({% url 'network-detail' network.network.ipv4 %}) |
{% endfor %}
{% else %}
Leider konnten wir keine Informationen über die Netzwerke dieses Minions abgreifen
{% endif %}

# Installed Packages

{% block package-description %}{% endblock %}

| Package | Version |
|---------|---------|
{% for package, version in minion.data.packages.items %}| {{ package }} | {{ version }} |
{% endfor %}

{% block else-description %}{% endblock %}
