from whyis import autonomic
from rdflib import URIRef
from slugify import slugify
from whyis import nanopub

from whyis.namespace import sioc_types, sioc, sio, dc, prov, whyis

class SurfaceEnergyGen(autonomic.UpdateChangeService):
    activity_class = whyis.SurfaceEnergyGen

    def getInputClass(self):
        return sioc.Post

    def getOutputClass(self):
        # http://purl.org/dc/dcmitype/Dataset
        return URIRef("http://purl.org/dc/dcmitype/Text")

    def get_query(self):
        return QUERY

    def process(self, i, o):
        content = i.value(sioc.content)
        # soup = BeautifulSoup(content, 'html.parser')
        # text = soup.get_text("\n")
        # o.add(URIRef("http://schema.org/text"), Literal(text))

QUERY = '''
PREFIX nm: <http://materialsmine.org/ns/>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?VolFrac (LCASE(?SurfaceTreatmentType) AS ?PST) (LCASE(?MatrixType) AS ?matrix) ?sample ?doi WHERE {
  ?sample a nm:PolymerNanocomposite;
          sio:hasComponentPart ?FillerPart ,
                               ?MatrixPart .
  
  ?doi sio:hasPart ?sample .

  ?FillerPart sio:hasRole [ a nm:Filler ] ;
              a [ rdfs:label "Silicon dioxide" ] .
  
  ?MatrixPart sio:hasRole [ a nm:Matrix ] ;
              a [ rdfs:label ?MatrixType ] .
  
  OPTIONAL {
    ?FillerPart sio:isSurroundedBy [ sio:hasRole [ a nm:SurfaceTreatment ] ;
                                     a [ rdfs:label ?SurfaceTreatmentType ] ] .
  }                   
}
'''