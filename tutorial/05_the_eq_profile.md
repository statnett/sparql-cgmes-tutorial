# The EQ profile

Let us consider the EQ profile a bit more thoroughly.
The EQ profile contains information about all equipment in a power system, whether its disconnected or not doesn't matter, pretty much everything is there.
This also makes it largest data profile by a large margin, and a single CIM-XML file can be gigabytes!
It is therefore common for the EQ profiles to change seldomly, while the SSH, TP and SV profiles, which contain more frequently changing data to change often.

As already described, the CIM model describes the network as a collection of conducting equipment, terminals and connectivity nodes.
There are a couple of extra data types that provide metadata for conducting equipment, but these are the main data types.

Consider, for example, a connectivity node.
Sometimes, we want to store metadata about collections connectivity nodes as well, which is included in a `ConnectivityNodeContainer` object that `ConnectivityNode`s point to.
All these definitions and relationships are specified in the documentation for the EQ profile, and navigating this documentation is key for getting data out of CGMES exports.

## Exercises

1. Download the CGMES documentation by running `uv run python -m sparql_tutorial.download_cgmes docs -o docs/`. Open it in your browser, e.g. by running `python -m http.server -d docs/HTML` and opening `http://localhost:8000` in a web browser.
2. Read the documentation entry for `SynchronousMachine` and `GeneratingUnit` and answer the following questions:

   * What is the relationship between the `SynchronousMachine` and `GeneratingUnit`?
   * What do you think the `0..1` and `1..1` in the second column of the members tables mean?
    
3. Open the [`exercises/05_eq_lookups.py`](../exercises/05_eq_lookups.py`) and modify its query so it contains a `?sync_unit_name` variable with the `cim:IdentifiedObject.name` attribute of the `cim:SynchronousMachine` connected to the `cim:GeneratingUnit`.
4. Expand the query so it now displays the `cim:IdentifiedObject.name` attribute of the `cim:ConnectivityNode` of the SynchronousMachine you obtained in the last exercise.

## Reflection

As you may have realised in exercise 1 and two, the EQ profile is quite extensive, and you may need to follow links to get the information you want.
For example, to find the connectivity node(s) for a `GeneratingUnit`, you need to traverse an inverse `cim:SynchronousMachine.GeneratingUnit`-predicate, an inverse `cim:Terminal.ConductingEquipment`-predicate, and finally a `cim:Terminal.ConnectivityNode`-predicate.
The documentation is a good starting point for crafting these more intricate queries.
However, sometimes it also helps to interactively craft SPARQL queries, using the documentation as a reference to understand what different prefixes mean.

## Exercises

1. Update the [`exercises/05_eq_lookups.py`](../exercises/05_eq_lookups.py`) file so it instead queries the [`load_and_gen_transformer.xml`](../exercises/data/dummy/load_and_gen_transformer.xml) file with query below. What do you think it does?

```SPARQL
SELECT * WHERE {
    ?cn cim:IdentifiedObject.name 'CN-2' ;
        ^cim:Terminal.ConnectivityNode / cim:Terminal.ConductingEquipment ?equip
}
```

2. Update the query again so it is the query below. What do you think it does?

```SPARQL
SELECT * WHERE {
    ?start_term cim:IdentifiedObject.name 'Terminal-G1' ;
                cim:Terminal.ConnectivityNode / ^cim:Terminal.ConductingEquipment ?connected_term
}
```

## Reflection

We have now seen two useful queries.
The first is pretty straightforward: It finds all conducting equipment connected to a connectivity node.
The second however, might seem odd.
First, we traverse edges with a given prefix forwards and then, edges with the same prefix backwards again.
If there was only one terminal connected to each connectivity node, then this wouldn't do anything interesting.
However, since multiple terminals point at the same connectivity node, we first find one connectivity node.
Then, when we traverse edges with the `cim:Terminal.ConductingEquipment` prefix backwards, we find *all* terminals connected to that connectivity node.
Thus, we end up with a query that finds all terminals that share connectivity node with the terminal we specified.

Below, we have a simple diagram that shows how the final query works.

## Exercises

1. Update the [`exercises/05_eq_lookups.py`](../exercises/05_eq_lookups.py`) file so it finds the MRID of the load with name 'Load-1'
2. Update the query so it finds the MRID of the connectivity node that 'Load-1' is connected to.
3. Update the query so it finds the `cim:TransformerEnd.endNumber` that 'Load-1' is connected to (via the connectivity node).
