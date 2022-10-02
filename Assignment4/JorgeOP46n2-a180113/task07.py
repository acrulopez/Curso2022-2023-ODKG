# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1796cOGWAgJErVW2pgiye7As8wDavp5J6

**Task 07: Querying RDF(s)**
"""

#pip install rdflib
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2021-2022/master/Assignment4/course_materials"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
#g.parse(github_storage+"/rdf/example6.rdf", format="xml")
g.parse("../course_materials/rdf/example6.rdf", format="xml")

ns = Namespace("http://somewhere#")

"""# Nueva sección

**TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL**
"""

print("RDFLib")
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s)


print("SPARQL")
q1 = prepareQuery("""
    SELECT ?subclase WHERE{
    ?subclase rdfs:subClassOf ns:Person.
    }""", initNs={"ns":ns})

for r in g.query(q1):
  print(r.subclase)

"""**TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)**

"""


print("RDFLib")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  print(s)
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s1, p, o in g.triples((None, RDF.type, s)):
    print(s1)


print("SPARQL")
q1 = prepareQuery("""
    SELECT ?persona WHERE{
      {?persona rdf:type ns:Person.}
       UNION
       {?subclase rdfs:subClassOf ns:Person.
        ?persona rdf:type ?subclase.}

    }""", initNs={"ns":ns})

for r in g.query(q1):
  print(r.persona)


"""**TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL**

"""


print("RDFLib")
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  for s1, p1, o1, in g.triples((s, None, None)):
    print("person: ", s, "property: ", p1)
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s1, p1, o1 in g.triples((None, RDF.type, s)):
    for s2, p2, o2 in g.triples((s1, None, None)):
      print("person: ", s1, "property: ", p1)


print("SPARQL")
q1 = prepareQuery("""
    SELECT DISTINCT ?persona ?propiedad WHERE{
    {?persona rdf:type ns:Person.}

    UNION{
      ?subclase rdfs:subclassOf* ns:Person.
      ?persona rdf:type ?subclase
    }
    ?persona ?propiedad ?Value
    }""", initNs={"ns":ns})

for r in g.query(q1):
  print("person: ",r.persona, "property: ", r.propiedad)
