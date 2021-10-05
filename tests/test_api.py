import json
import api


def test_01():
    with open('credentials.json') as fil:
        credentials = json.load(fil)
    # with open('template.xml') as fil:
    #     body = fil.read()
    mapi = api.MyDataAPI(credentials)
    # print(mapi.request_transmitted_docs(''))
