# SPARQL joins as graph traversal

Recall that the RDF-database represents a directed graph.
Each triple is a labelled edge, where the subject is the start vertex, the predicate is the edge label and the object is the end vertex.
Furthermore, SPARQL is a way to extract data from this graph.

Therefore, we don't think of SPARQL queries the same way as we think of SQL queries.
We often don't want to select data, we want to traverse the graph.

Consider, for example, the following graph
![Network diagram displaying the graph Terminal-L1 <-- cim:IdentifiedObject.name -- _bce40a7a-3ab9-40df-8a25-bbd944a7d794 -- cim:Terminal.ConductingEquipment -- > _334e4a67-6496-47a1-b623-d306f83f3bbf -- cim:IdentifiedObject.name --> Load-1; _bce40a7a-3ab9-40df-8a25-bbd944a7d794 -- cim:Terminal.ConnectivityNode -- > _196965ea-27ad-4566-a7ee-429856557aef --> cim:IdentifiedObject.name --> CN-1.](./figures/03_simple_graph_with_names.svg)
A natural question here is: What is the ID of the conducting equipment connected to the terminal with name "Terminal-L1".

Looking at the graph, we see that we first need to find the ID of the terminal, which we can use the following SPARQL-query to do

```sparql
SELECT * WHERE {
    ?terminal cim:IdentifiedObject.name 'Terminal-L1'
}
```

then, once we know the ID of the terminal, we can find the ID of its conducting equipment by following the `cim:Terminal.ConductingEquipment` edge.

```sparql
SELECT * WHERE {
    ?terminal cim:IdentifiedObject.name 'Terminal-L1' .
    ?terminal cim:Terminal.ConductingEquipment ?cond_equip
}
```

## Exercises
1. Run the [exercises/03_graph_traversal.py](../exercises/03_graph_traversal.py) file. Did you get the correct conducting equipment?
2. Update the code so it says 
```sparql
SELECT * WHERE {
    ?terminal cim:IdentifiedObject.name 'Terminal-L1' ;
              cim:Terminal.ConductingEquipment ?cond_equip
}
```
instead. Run the code, did anything change?

3. Update the query so you find the ID of the connectivity node instead.
4. Update the query so you also find the name of the connectivity node.

## Reflection

By not only considering the edges, but how you traverse them to obtain some information, we can find a lot of useful knowledge.
First, we had a literal, and we want to find the objects that have this literal as a subject and find some information about these objects.
This is a very common pattern, so common in fact that it has it's own syntax: `;`.
By using a semicolon to join two queries, we say that they should use the same subject.
However, while it can be nice to shorten the query, you should consider if it makes the query easier or harder to understand.
In this case, we had a lot of whitespace to help us make it clear what happened.

Also, while it's sometimes enough to traverse just two edges we also saw that to find the name of the connetivity node, we needed to traverse three edges:

```sparql
SELECT * WHERE {
    ?terminal cim:IdentifiedObject.name 'Terminal-L1' ;
              cim:Terminal.ConnectivityNode ?cn .
    ?cn cim:IdentifiedObject.name ?cn_name
}
```

## Exercises
1. Replace the select statement you have in [exercises/03_graph_traversal.py](../exercises/03_graph_traversal.py) with the one above and run the code. Did you get the correct name of the connectivity node?
2. Update the select statement so it says `SELECT ?cn_name WHERE` instead of `SELECT * WHERE`. What do you think this does? Run the code again to see if you were right.

## Reflection
A downside with the more complicated queries is that we create a lot of "intermediate" variables that we aren't interested in.
For example, when we want to find the name of the connectivity node that is connected to `'Terminal-L1'`, we have to create the `?terminal`-variable and the `?cn`-variable.
In this case, we only have two intermediate variables, however, for more complex queries, we quickly get way too many intermediate variables that can make the query a bit difficult to parse.

Luckily, since SPARQL is a query language for graphs, it has specific syntax for graph traversal, such as the `^`-operator and `/`-operator, which we'll look a bit at next.


## Exercises
1. Update the select statement in [exercises/03_graph_traversal.py](../exercises/03_graph_traversal.py) so it says
```sparql
SELECT * WHERE {
    'Terminal-L1' ^cim:IdentifiedObject.name ?terminal .
    ?terminal cim:Terminal.ConnectivityNode ?cn .
    ?cn cim:IdentifiedObject.name ?cn_name
}
```
Run the script, did anything change? What do you think the `^`-operator does?

2. Update the coda again, so it says
```sparql
SELECT * WHERE {
    'Terminal-L1' ^cim:IdentifiedObject.name ?terminal .
    ?terminal cim:Terminal.ConnectivityNode/cim:IdentifiedObject.name ?cn_name
}
```
Run the script. Did anything change? What do you think the `/`-operator does?

3. Update the script so the query is a one-liner.

## Reflection

The first thing we did now was to use the `^`-operator.
This *InversePath* operator "flips" an edge, so the subject becomes the object and the object becomes the subject.
At first glance, this might not be too useful, but it can be very useful (which will be apparent very soon).

Then, we used the `/` *SequencePath*-operator. 
This operator essentially takes two predicates and says that we want to follow both edges.
So the `?terminal cim:Terminal.ConnectivityNode/cim:IdentifiedObject.name ?cn_name`-line means: start at the `?terminal`-nodes, follow any `cim:Terminal.ConnectivityNode` edge and wherever you end up, follow the `cim:IdentifiedObject.name` edge and store the end subject in the `?cn_name`-variable.

When we combine the `/`-operator and the `^`-operator, we can get the full query down to a oneliner:
```
SELECT * WHERE {
    'Terminal-L1' ^cim:IdentifiedObject.name / cim:Terminal.ConnectivityNode / cim:IdentifiedObject.name ?cn_name
}
```

Below, we see a figure that illustrates how this graph traversal is conducted.
We start in the `'Terminal-L1'`-vertex and follow the path in green to end up at the `'CN-1'`-vertex, which is stored in the `?cn_name`-variable.

![Network diagram displaying the graph Terminal-L1 <-- cim:IdentifiedObject.name -- _bce40a7a-3ab9-40df-8a25-bbd944a7d794 -- cim:Terminal.ConductingEquipment -- > _334e4a67-6496-47a1-b623-d306f83f3bbf -- cim:IdentifiedObject.name --> Load-1; _bce40a7a-3ab9-40df-8a25-bbd944a7d794 -- cim:Terminal.ConnectivityNode -- > _196965ea-27ad-4566-a7ee-429856557aef --> cim:IdentifiedObject.name --> CN-1. The path Terminal-L1 -- ^cim:IdentifiedObject.name --> _bce40a7a-3ab9-40df-8a25-bbd944a7d794 -- cim:Terminal.ConnectivityNode -> _196965ea-27ad-4566-a7ee-429856557aef --> cim:IdentifiedObject.name --> CN-1 is highlighted.](./figures/04_simple_graph_with_names_and_path.svg)


## Next up
Now that you are familiar SPARQL, we can move on to looking at CIM and CGMES: [link](./04_cim_cgmes.md)
