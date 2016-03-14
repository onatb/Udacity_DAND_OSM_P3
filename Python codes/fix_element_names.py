#This code fixes element names containing abbreviated street types
import xml.etree.ElementTree as ET
import pprint
from collections import defaultdict
import re

OSMFILE = "C:/ankara.osm"

#1. Build a regular expression that searches the end of the string to find street types
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

#2. Investigate street types and create an expected list of street types that do not need to be cleaned
expected=[u"Cadde",u"Caddesi","uSokak",u"Bulvarı",u"Yolu",u"Kampüsü"]

#3. Create a Python dictionary that addresses expected values of abbreviations
mapping = { #Boulevard abbreviations
            u"Blv.": u"Bulvarı",
            u"Bul": u"Bulvarı",
            #Avenue abbreviations
            u"CADDESİ": u"Caddesi",
            u"caddesi": u"Caddesi",
            u"Cad": u"Caddesi",
            u"Cad.": u"Caddesi",
            u"Cd": u"Caddesi",
            u"Cd.": u"Caddesi",
            u"cd": u"Caddesi",
            #Street abbreviations
            u"SOKAK": u"Sokak",
            u"sokak": u"Sokak",
            u"Sk": u"Sokak",
            u"Sk.":u"Sokak",
            u"Sok": u"Sokak",
            u"Sok.": u"Sokak",
            u"Soak": u"Sokak",
            u"sk": u"Sokak",
            u"sK": u"Sokak"
            }

def audit_street_type(street_types, street_name):
    #This function searches for street type of a given street name
    #and adds that street type to dictionary if it is not in expected list
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_name(elem):
    return (elem.attrib['k'] == "name")

def audit(osmfile):
    #This function iterates 'tag' elements inside node' and 'way' elements in XML file using iterparse function
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

def update_name(name, mapping):
    #This function fixes abbreviations, replaces them with expected values
    for key in mapping:
        if name.find(key)>-1:
            if u" " not in name[:name.find(key)]:
                #If there isn't any space between street name and street type, add a space
                #and replace abbreviation with expected value
                name=name[:name.find(key)]+u" "+mapping[key]
            else:
                #replace abbreviation with expected value
                name=name[:name.find(key)]+mapping[key]
            if u"Caddesi" in name and name[0].isdigit():
                #In Turkish, avenues starting with a digit are called 'Cadde',
                #where other type of avenues are called 'Caddesi'
                #For instance: '2785. Cadde', 'Akay Caddesi'
                name=name.replace(u"Caddesi",u"Cadde")
            break
    return name

#4. Parse through XML file looking for street names and replace the abbreviations with expected values
st_types = audit(OSMFILE)

for st_type, ways in st_types.iteritems():
    for name in ways:
        better_name = update_name(name, mapping)
        print name, "=>", better_name
        
