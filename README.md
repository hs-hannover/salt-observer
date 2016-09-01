# salt-observer [![python version](https://img.shields.io/badge/python-3.x-blue.svg)]() [![build status](https://lab.it.hs-hannover.de/django/salt-observer/badges/master/build.svg)](https://lab.it.hs-hannover.de/django/salt-observer/commits/master)

Web interface to visualize most of the data *your* installed [SaltStack](https://docs.saltstack.com/en/latest/) installation provides.

Written in [python](https://www.python.org/), with the help of [django](https://www.djangoproject.com/).

## Primary source and issue tracking

The source of this project is hosted on [lab.it.hs-hannover.de](https://lab.it.hs-hannover.de/django/salt-observer).  
Issues and further documentation can be found there.

## Development

A complete list of the `Minion.data` json structure can be found [here](https://lab.it.hs-hannover.de/django/salt-observer/wikis/minion-data-structure) in the wiki.


```python
# get output of 'w' command of all 'tgt' minions
request('token', {'tgt': '*', 'fun': 'cmd.run', 'arg': 'w'})

# get all grains of 'tgt' minions
request('token', {'tgt': '*', 'fun': 'grains.items'})

# execute some state and apply custom pillars to it
request('token', {'tgt': '*', 'fun': 'state.sls', 'kwarg': {
    'mods': 'name_of_state', 'pillar': {'some': 'pillar_data'}
}})
```
