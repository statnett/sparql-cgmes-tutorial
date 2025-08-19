import rdflib
from pathlib import Path


data_dir = Path(__file__).with_name("data") / "dummy"

graph = rdflib.Graph()
graph.parse(data_dir / "single_gen.xml", publicID="EQ")

query = """
SELECT * WHERE {
    ?gen cim:IdentifiedObject.name 'Gen-1'
}
"""

for row in graph.query(query):
    print({k: str(v) for k, v in row.asdict().items()})
