import rdflib
from pathlib import Path


data_dir = Path(__file__).parent.with_name("data") / "dummy"

graph = rdflib.Graph()
graph.parse(data_dir / "first_intro.xml", publicID="EQ")


query = """
SELECT * WHERE {
    ?subject ?predicate ?object
}
"""

for row in graph.query(query):
    print({k: str(v) for k, v in row.asdict().items()})
