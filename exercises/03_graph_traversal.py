import rdflib
from pathlib import Path


data_dir = Path(__file__).with_name("data") / "dummy"

graph = rdflib.Graph()
graph.parse(data_dir / "first_intro.xml", publicID="EQ")

query = """
SELECT * WHERE {
    ?terminal cim:IdentifiedObject.name 'Terminal-L1' .
    ?terminal cim:Terminal.ConductingEquipment ?cond_equip
}
"""

for row in graph.query(query):
    print({k: str(v) for k, v in row.asdict().items()})
