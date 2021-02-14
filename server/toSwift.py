from caps import capsList

collection = ''

for cap in capsList:
    name = cap['cap_id'].partition('(')[0].rstrip()
    description = cap['cap_id'].partition('(')[-1].rpartition(')')[0]
    if description == '':
        description = 'nil'
    else:
        description = '"' + description + '"'
    capsLine = 'Cap(name: "'+name+'", description: '+description+', color: RGBPoint(r:'+str(cap["color"][0])+', g:'+str(cap["color"][1])+', b:'+str(cap["color"][2])+'), image: nil),'
    #print capsLine

    description = cap['cap_id'].partition('(')[-1].rpartition(')')[0]
    _description = cap['cap_id'].partition('(')[-1].rpartition(')')[0]
    if _description != '':
        _description = '-' + _description
    collectionLine = '"'+name+_description+'": ["quantity": '+str(cap["amount"])+', "cap": ["name": "'+name+'", "description": "'+description+'", "color": ["r": '+str(cap["color"][0])+', "g": '+str(cap["color"][1])+', "b": '+str(cap["color"][2])+'], "image": ""]],'
    collection = collection + collectionLine
print collection