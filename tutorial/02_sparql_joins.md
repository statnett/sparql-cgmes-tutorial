# Joining SPARQL queries

At this point, we have crafted simple queries where we essentially just filter the triples.
However, we can take it one step further and "join" multiple queries.

## Exercises

1. Open the [exercises/02_sparql_joins.py](../exercises/02_sparql_joins.py) and read the contents. Run it and compare the output with the [`exercises/data/dummy/first_intro.xml`](../exercises/data/dummy/first_intro.xml) file. What do you think the query did?
2. Modify the Python file, so it queries [`exercises/data/dummy/second_intro.xml`](../exercises/data/dummy/second_intro.xml) instead of [`exercises/data/dummy/first_intro.xml`](../exercises/data/dummy/first_intro.xml). What's the difference. Look at the XML-file, why do you think you got two output lines?
3. Undo so you query the [`exercises/data/dummy/first_intro.xml`](../exercises/data/dummy/first_intro.xml) file again and modify the query so it finds the ID of the connectivity node and its connected terminal instead of the ID of the load.

## Reflection

The "dot"-operator might be the closest thing we have to a join operator for SPARQL, so the query 

```sparql
SELECT * WHERE {
    ?load cim:IdentifiedObject.name 'Load-1' .
    ?terminal cim:Terminal.ConductingEquipment ?load
}
```

works by first finding the triple with a predicate `cim:IdentifiedObject.name` and subject `'Load-1'`..
Still, the object from all triples are stored with with the `?load`-name.
Importantly, multiple subjects might have the same `cim:IdentifiedObject.name`, so the `?load` "variable" may represent multiple values.
Then, we find all triples with a predicate equal to `cim:Terminal.ConductingEquipment` and a subject that matches one of the values that `?load` "covers".

An important thing to note is that with joins in SPARQL, we match all possible sets of triples that match the query.
Consider therefore the query

```sparql
SELECT * WHERE {
    ?s1 ?p1 ?o1 .
    ?s2 ?p2 ?o2
}
```

This will return all possible combinations of triples and for each triple, it will find all possible combinations of triples again.
Such queries form "cartesian products", and it can be easy to accidentally create one (for example, if we have a typo).
