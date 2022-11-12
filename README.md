# Loqinkee

An extremely simplistic python templating engine built to parse and render untrusted arbitrary templates from users.
Currently only supports rendering variables, but once blocks are added will feature a maximum number of allowed loops and a timeout to guarantee templating does not run forever.
Only supports `int`, `str`, `dict`, and `list` as types in data, will not allow rendering of other types or of built-in attribtues.

Usage:

```python
>>> import loqinkee
>>> 
>>> template = """
... Hello {{ name }},
... 
... This is a more complex value: {{ arg.0.foo }}
... """
>>> 
>>> loqinkee.render(template, {"name": "Andrew", "arg": [{"foo": "a more complex value"}]} )
'\nHello Andrew,\n\nThis is a more complex value: a more complex value\n'
```
