import rdflib
from pathlib import Path


data_dir = Path(__file__).with_name("data") / "dummy"

graph = rdflib.Graph()
graph.parse(data_dir / "first_intro.xml", publicID="EQ")

query = """
SELECT * WHERE {
    ?load cim:IdentifiedObject.name 'Load-1' .
    ?terminal cim:Terminal.ConductingEquipment ?load
}
"""

for row in graph.query(query):
    print({k: str(v) for k, v in row.asdict().items()})
