# Generelle Informationen

Netzwerk: `{{ network.ipv4 }}`

Subnet-Mask: `{{ network.mask }}`


# Minions

{% block minion-description %}{% endblock %}

{% if network.minion_set.all %}
| Minion ID | Network interface | MAC addresse |
|-----------|-------------------|--------------|
{% for minion in network.minion_set.all %}| [{{ minion.fqdn }}]({% url 'minion-detail' minion.fqdn %}) | {% for ni in minion.networkinterface_set.all %}{% if ni.network.ipv4 == network.ipv4 %}{{ ni.name }} | {{ ni.mac_address }} |{% endif %}{% endfor %}
{% endfor %}
{% else %}
Leider konnten wir keine Informationen über die Minions in diesem netzwerk abgreifen.
{% endif %}

{% block else-description %}{% endblock %}
