

import fiona #https://gis.stackexchange.com/questions/113799/how-to-read-a-shapefile-in-python

"""
[('OIDN', 170273), 
('UIDN', 170273), 
('RECID', 3704935), 
('CAPAKEY', '12038A0016/00C002'), 
('TYPE', 'PR'), 
('LBLTYPE', 'Privaat domein'), 
('CASEKEY', '12038A'), 
('FISCSITID', 1), 
('FISCSIT', '2016-01-01'), 
('UPDDATE', '2016-11-30'), 
('LENGTE', 231.36), 
('OPPERVL', 1096.17)]), 
'geometry': {'type': 'Polygon', 'coordinates': [[(138982.002700001, 200520.74399999902), (138991.27170000225,...

"""


"""
{'properties': 
OrderedDict(
    [('OIDN', 'int:15'), 
    ('UIDN', 'int:15'), 
    ('RECID', 'int:10'), 
    ('CAPAKEY', 'str:17'), 
    ('TYPE', 'str:2'), 
    ('LBLTYPE', 'str:50'), 
    ('CASEKEY', 'str:6'), 
    ('FISCSITID', 'int:5'), 
    ('FISCSIT', 'date'), 
    ('UPDDATE', 'date'), 
    ('LENGTE', 'float:16.2'), 
    ('OPPERVL', 'float:16.2')
    ]), 
    'geometry': 'Polygon'}  """


shape = fiona.open("/Users/jari/DATA/Projects/GIS/CadGIS_fiscaal_20210101_GewVLA_Shapefile/Shapefile/bpncapa.shp")
print(shape.schema)
"""print("="*100)
print("properties", shape.schema['properties'])
print("="*100)
print("shape[1]", shape[1])"""

print(len(shape))
for i in shape:
    if shape['UIDN'] == '12906467':
        print("LÖYTYI!!!!!!!!")
        print(i)


shape.close
"""print("Schema:", shape.schema)
print("CRS ",shape.crs)
print("driver ",shape.driver)
print("name ",shape.name)

print("mode ",shape.mode)
print("meta ",shape.meta)
#print("srs ",shape.srs)
print("bounds ",shape.bounds)
print("closed ",shape.closed)"""



