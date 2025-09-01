# Introduction

We'll start with some exercises to get familiar with the most basic SPARQL-queries.
To do so, we'll use the Python library [RDFLib](https://rdflib.readthedocs.io/en/stable/index.html), which allows us to load RDF/XML-files and query them in memory directly. 

## Exercises
1. Open the [exercises/01_simple_select](../exercises/01_simple_select.py)-script. Which XML-file do you think it parses?
2. Can you find the SPARQL-query in the Python script?
3. Run the script and look at the output. Do you see any pattern?
4. Try to modify the `?subject ?predicate ?object`-line in the Python file so it says `?sub ?pred ?obj`. Rerun the script, what changed?
5. One of the lines in the output says `{'subject': 'EQ#_196965ea-27ad-4566-a7ee-429856557aef', 'predicate': 'http://iec.ch/TC57/2013/CIM-schema-cim16#ConnectivityNode.ConnectivityNodeContainer', 'object': 'EQ#_705e0aca-674d-47e6-b550-d9f6afecdb25'}`. Can you find the XML-tag in `data/dummy/first_intro.xml` that matches this subject? (Hint: skip the `EQ#`-part when you're searching).
6. Inside the tag that matches the subject `_196965ea-27ad-4566-a7ee-429856557aef`, can you find the `ConnectivityNode.ConnectivityNodeContainer` tag? What do you think the object ID in the `{'subject': 'EQ#_196965ea-27ad-4566-a7ee-429856557aef', 'predicate': 'http://iec.ch/TC57/2013/CIM-schema-cim16#ConnectivityNode.ConnectivityNodeContainer', 'object': 'EQ#_705e0aca-674d-47e6-b550-d9f6afecdb25'}`-triple means?

## Reflection
You have now run your first SPARQL-query, and you may have noticed that SPARQL can be used to get the outputs of an XML-file that follows a very specific schema.
However, SPARQL doesn't really work on XML, it works on *Resource Description Framework (RDF)*-data, which we can represent with XML.
RDF-data is a way to specify a graph, and we'll look at that later, but for now, just think of RDF-data as a list of three-tuples:

```raw
[
    (subject1, predicate1, object1),
    (subject2, predicate2, object2),
    (subject3, predicate3, object3),
    [...]
    (subjectN, predicateN, objectN),
]
```

So when RDFLib reads an the [`exercises/data/dummy/first_intro.xml`](../exercises/data/dummy/first_intro.xml)-file, it converts it into a list like the one above.
In particular the file

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:cim="http://iec.ch/TC57/2013/CIM-schema-cim16#" xmlns:entsoe="http://entsoe.eu/CIM/SchemaExtension/3/1#" xmlns:md="http://iec.ch/TC57/61970-552/ModelDescription/1#" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <cim:ConnectivityNode rdf:ID="_196965ea-27ad-4566-a7ee-429856557aef">
        <cim:IdentifiedObject.name>CN-1</cim:IdentifiedObject.name>
        <cim:ConnectivityNode.ConnectivityNodeContainer rdf:resource="#_705e0aca-674d-47e6-b550-d9f6afecdb25"/>
    </cim:ConnectivityNode>
    
    <cim:Terminal rdf:ID="_bce40a7a-3ab9-40df-8a25-bbd944a7d794">
        <cim:IdentifiedObject.name>Terminal-L1</cim:IdentifiedObject.name>
        <cim:Terminal.ConductingEquipment rdf:resource="#_334e4a67-6496-47a1-b623-d306f83f3bbf"/>
        <cim:Terminal.ConnectivityNode rdf:resource="#_196965ea-27ad-4566-a7ee-429856557aef"/>
    </cim:Terminal>
    
    <cim:EnergyConsumer rdf:ID="_334e4a67-6496-47a1-b623-d306f83f3bbf">
        <cim:IdentifiedObject.name>Load-1</cim:IdentifiedObject.name>
    </cim:EnergyConsumer>
</rdf:RDF>
```

is converted into the following triples

```raw
[
    ({rdfID}#_196965ea-27ad-4566-a7ee-429856557aef, cim:IdentifiedObject.name, CN-1),
    ({rdfID}#_196965ea-27ad-4566-a7ee-429856557aef, cim:ConnectivityNode.ConnectivityNodeContainer, {rdfID}#_705e0aca-674d-47e6-b550-d9f6afecdb25),
    ({rdfID}#_bce40a7a-3ab9-40df-8a25-bbd944a7d794, cim:IdentifiedObject.name, Terminal-L1),
    ({rdfID}#_bce40a7a-3ab9-40df-8a25-bbd944a7d794, cim:Terminal.ConductingEquipment, {rdfID}#_334e4a67-6496-47a1-b623-d306f83f3bbf),
    ({rdfID}#_bce40a7a-3ab9-40df-8a25-bbd944a7d794, cim:Terminal.ConnectivityNode, {rdfID}#_196965ea-27ad-4566-a7ee-429856557aef),
    ({rdfID}#_334e4a67-6496-47a1-b623-d306f83f3bbf, cim:IdentifiedObject.name, Load-1),
]
```

(we get some extra triples too, but we'll ignore those)

Also, you may have realised that one of the powers of SPARQL is it's ability to filter triples. When we use the query
```
SELECT * WHERE {
    ?subject ?predicate 'Terminal-L1'
}
```
we get all the triples that share the object 'Terminal-L1'.

## Exercises

1. Do you see a pattern in how the XML-file above is converted into RDF-triples?
2. Can update `01_simple_select.py` so it prints out all triples with the `cim:IdentifiedObject.name`-predicate?

## Reflection

We'll start with exercise 2: when we write `?subject ?predicate ?object`, then we select all triples.
However, we can filter each of these fields arbitrarily, e.g. if we want all triples with the `cim:IdentifiedObject.name`-predicate, then we need to write `?subject cim:IdentifiedObject.name ?object`.

Now, regarding how XML is converted into RDF-triples. Consider the XML-file

```xml
<cim:Terminal rdf:ID="_bce40a7a-3ab9-40df-8a25-bbd944a7d794">
    <cim:IdentifiedObject.name>Terminal-L1</cim:IdentifiedObject.name>
    <cim:Terminal.ConductingEquipment rdf:resource="#_334e4a67-6496-47a1-b623-d306f83f3bbf"/>
    <cim:Terminal.ConnectivityNode rdf:resource="#_196965ea-27ad-4566-a7ee-429856557aef"/>
</cim:Terminal>
```

If we read this as XML, we would read the document as a `cim:Terminal`-object with ID `_bce40a7a-3ab9-40df-8a25-bbd944a7d794` with three children, a `cim:IdentifiedObject.name`-object a `cim:Terminal.ConductingEquipment`-object and a `cim:Terminal.ConnectivityNode`-object.
For RDF, we see it kind of similar.
However, instead of children, we talk about triples (or as we'll see shortly "sentences").
The XML above becomes three triples:

```raw
[
    ({rdfID}#_bce40a7a-3ab9-40df-8a25-bbd944a7d794, cim:IdentifiedObject.name, Terminal-L1),
    ({rdfID}#_bce40a7a-3ab9-40df-8a25-bbd944a7d794, cim:Terminal.ConductingEquipment, {rdfID}#_334e4a67-6496-47a1-b623-d306f83f3bbf),
    ({rdfID}#_bce40a7a-3ab9-40df-8a25-bbd944a7d794, cim:Terminal.ConnectivityNode, {rdfID}#_196965ea-27ad-4566-a7ee-429856557aef),
]
```

These three triples specify edges in a graph.
Specifically, we say that the `cim:Terminal`-vertex with ID `_bce40a7a-3ab9-40df-8a25-bbd944a7d794` has three edges: a `cim:IdentifiedObject.name`-edge that points to the `Terminal-L1`-literal, a `cim:Terminal.ConductingEquipment`-edge that points to another vertex with ID `_334e4a67-6496-47a1-b623-d306f83f3bbf` and a `cim:Terminal.ConnectivityNode`-edge that points to a third vertex with ID `_196965ea-27ad-4566-a7ee-429856557aef`.
The figure below shows a small drawing of this graph.

![Network diagram displaying the graph parametrised by the above XML-file](./figures/01_simple_graph.svg)

Each triple is represented with one arrow, the subject is the "starting vertex", the object is the "end vertex" and the predicate is the label of each array (or edge).

> [!Note]
> We have introduced some weird words here: `subject`, `predicate` and `object`.
> You may remember from your language classes in school that a sentence is built up from subjects, predicates and objects, and RDF data tries to mimic the same structure.
> Therefore, you can often read a triple as a sentence on the form "{subject} has/is a/the {predicate} {object}", so the triple `({rdfID}#_bce40a7a-3ab9-40df-8a25-bbd944a7d794, cim:IdentifiedObject.name, Terminal-L1)` can be read as "`{rdfID}#_bce40a7a-3ab9-40df-8a25-bbd944a7d794` has the `cim:IdentifiedObject.name` `Terminal-L1`".

## Exercises

1. What are the triples in this graph?
![Network diagram displaying the graph 'CN-1' <-- cim:IdentifiedObject.name -- '#_196965ea-27ad-4566-a7ee-429856557aef' -- cim:ConnectivityNode.ConnectivityNodeContainer --> '#_705e0aca-674d-47e6-b550-d9f6afecdb25'](./figures/02_exercise.svg)
2. Create an XML document that represents the graph.

## Reflection

Hopefully, you realised that there were two triples in the graph, one for each edge:

```raw
[
    ({rdfID}#_196965ea-27ad-4566-a7ee-429856557aef, cim:IdentifiedObject.name, 'CN-1'),
    ({rdfID}#_196965ea-27ad-4566-a7ee-429856557aef, cim:ConnectivityNode.ConnectivityNodeContainer, {rdfID}#_705e0aca-674d-47e6-b550-d9f6afecdb25),
]
```
Moreover, you may also have realised that literals are stored as the content of XML tags while references to other vertices are stored in the `rdf:resource`-attribute of the XML tags. Putting all of that together, we get the following XML document
```raw
<cim:ConnectivityNode rdf:ID="_196965ea-27ad-4566-a7ee-429856557aef">
    <cim:IdentifiedObject.name>CN-1</cim:IdentifiedObject.name>
    <cim:ConnectivityNode.ConnectivityNodeContainer rdf:resource="#_705e0aca-674d-47e6-b550-d9f6afecdb25"/>
</cim:ConnectivityNode>
```

> [!NOTE]
> The SPARQL specs use the word "node" where we use "vertex". These are interchangeable in the graph theory litterature, but since "node" already has a different meaning in the CGMES standard, we use the word "vertex" when we talk about SPARQL.

## Next up
You should now understand that RDF-data is structured in triples, and that these triples commonly are represented using XML.
Next up, we'll look at how SPARQL can be used to do other things than just filter the triples: [link](./02_sparql_joins.md)
