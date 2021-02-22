### Wufoo v3 REST API playground
A simple playground of Wufoo v3 APIs. https://wufoo.github.io/docs/#

#### Supported functionalities:
* Fetch forms
* Fetch single form
* Fetch form fields
* Fetch form comments
* Fetch form comments count
* Fetch entries (with filter and sorting)
* Fetch entries count
* Submit entry

#### Project structure:
```
wufoo-playground
    │──── README.md
    │──── requirements.txt
    │──── playground.py                   # main method for show case
    └──── wufoo_rest
              │──── api_caller.py         # An api gateway
              │──── utils.py              # util functions
              └──── api
                     │──── comment.py     # Comments requests and responses
                     │──── entry.py       # Entry requests and responses
                     │──── field.py       # Field requests and responses
                     └──── form.py        # Form requests and responses
```
