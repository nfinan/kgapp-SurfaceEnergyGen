from whyis import autonomic
from rdflib import URIRef
from slugify import slugify
from whyis import nanopub
from .surface_energy_terms import surface_energy_terms, pprint

from whyis.namespace import sioc_types, sioc, sio, dc, prov, whyis

class SurfaceEnergyGen(autonomic.UpdateChangeService):
    activity_class = whyis.SurfaceEnergyGen

    def getInputClass(self):
        return URIRef("http://materialsmine.org/ns/PolymerNanocomposite")

    def getOutputClass(self):
        return URIRef("http://materialsmine.org/ns/PolymerNanocomposite")

    def get_query(self):
        return QUERY

    def process(self, i, o):
        for vf, pst, matrix, FillerPart, MatrixPart in i.graph.query(filler_query, initNs={sample:i.identifier}):
            # Do the thing!!
            # Returns nested dict with 4 "Raw Terms" and 3 "Work Terms"
            d = surface_energy_terms(matrix, pst)
            units = {
                "WorkOfAdhesion": "http://www.ontology-of-units-of-measure.org/resource/om-2/joulePerSquareMetre",
                "WorkOfSpreading": "http://www.ontology-of-units-of-measure.org/resource/om-2/joulePerSquareMetre",
                "DegreeOfWetting": ""
            }

            # Add Work Terms
            for key, value in d["Work Terms"].items():
                uri_property = "http://materialsmine.org/ns/" + key
                uri_unit = units[key]
                property = o.graph.resource(BNode())
                property.add(RDF.type, URIRef(uri_property))
                property.add(sio.hasValue, Literal(value)) # Whatever the actual value is)
                property.add(sio.hasUnit, URIRef(uri_unit))
                o.add(sio.hasAttribute, property)
            
            # Add Raw Terms
            # Add Filler Energies
            filler_resource = o.graph.resource(FillerPart)

            # Dispersive
            FDSE = d["Raw Terms"]["filler dispersive surface energy"]
            property = o.graph.resource(BNode())
            property.add(RDF.type, URIRef("http://materialsmine.org/ns/DispersiveSurfaceEnergy"))
            property.add(sio.hasValue, Literal(FDSE)) # Whatever the actual value is)
            property.add(sio.hasUnit, URIRef("http://www.ontology-of-units-of-measure.org/resource/om-2/joulePerSquareMetre"))
            filler_resource.add(sio.hasAttribute, property)

            # Polar
            FPSE = d["Raw Terms"]["filler polar surface energy"]
            property = o.graph.resource(BNode())
            property.add(RDF.type, URIRef("http://materialsmine.org/ns/PolarSurfaceEnergy"))
            property.add(sio.hasValue, Literal(FPSE)) # Whatever the actual value is)
            property.add(sio.hasUnit, URIRef("http://www.ontology-of-units-of-measure.org/resource/om-2/joulePerSquareMetre"))
            filler_resource.add(sio.hasAttribute, property)

            # Add Matrix Energies
            matrix_resource = o.graph.resource(MatrixPart)

            # Dispersive
            MDSE = d["Raw Terms"]["matrix dispersive surface energy"]
            property = o.graph.resource(BNode())
            property.add(RDF.type, URIRef("http://materialsmine.org/ns/DispersiveSurfaceEnergy"))
            property.add(sio.hasValue, Literal(MDSE)) # Whatever the actual value is)
            property.add(sio.hasUnit, URIRef("http://www.ontology-of-units-of-measure.org/resource/om-2/joulePerSquareMetre"))
            matrix_resource.add(sio.hasAttribute, property)

            # Polar
            MPSE = d["Raw Terms"]["matrix polar surface energy"]
            property = o.graph.resource(BNode())
            property.add(RDF.type, URIRef("http://materialsmine.org/ns/PolarSurfaceEnergy"))
            property.add(sio.hasValue, Literal(MPSE)) # Whatever the actual value is)
            property.add(sio.hasUnit, URIRef("http://www.ontology-of-units-of-measure.org/resource/om-2/joulePerSquareMetre"))
            matrix_resource.add(sio.hasAttribute, property)


            # for key, value in d["Raw Terms"].items():
            #     property = o.graph.resource(BNode())
            #     property.add(RDF.type, URIRef("URI_OF_THE_PROPERTY_CLASS")
            #     property.add(sio.hasValue, Literal(value)) # Whatever the actual value is)
            #     property.add(sio.hasUnit, URIRef("URI_OF_THE_UOM")
            #     o.add(sio.hasAttribute, property)


filler_query = '''
PREFIX nm: <http://materialsmine.org/ns/>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?VolFrac (LCASE(?SurfaceTreatmentType) AS ?PST) (LCASE(?MatrixType) AS ?matrix) ?FillerPart ?MatrixPart WHERE {
  ?sample a nm:PolymerNanocomposite;
          sio:hasComponentPart ?FillerPart ,
                               ?MatrixPart .
  ?FillerPart sio:hasRole [ a nm:Filler ] ;
              a [ rdfs:label "Silicon dioxide" ];
              sio:hasAttribute [a nm:VolumeFraction; sio:hasValue ?volFrac] .
  
  ?MatrixPart sio:hasRole [ a nm:Matrix ] ;
              a [ rdfs:label ?MatrixType ] .
  
  OPTIONAL {
    ?FillerPart sio:isSurroundedBy [ sio:hasRole [ a nm:SurfaceTreatment ] ;
                                     a [ rdfs:label ?SurfaceTreatmentType ] ] .
  }                   
}
'''

QUERY = '''
PREFIX nm: <http://materialsmine.org/ns/>
PREFIX sio: <http://semanticscience.org/resource/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?sample WHERE {
  ?sample a nm:PolymerNanocomposite;
          sio:hasComponentPart ?FillerPart ,
                               ?MatrixPart .
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