# Power system data: CIM, CGMES, node-breaker and bus-branch

Transmission system data is often stored on the Common Grid Model Exchange Standard (CGMES)-format, which builds upon the Common Information Model (CIM) standards for transmission system data models.

CGMES consists of different *profiles*, which are data models that describe different part of the transmission system.
Each profile corresponds to a CIM standard maintained by the International Electrotechnical Commission (IEC) and some important profiles are:

 * The equipment profile (EQ): Quasi-static information. Which components are currently in the transmission system.
 * The steady state hypothesis profile (SSH): Dynamic information. How are components in the EQ-profile connected, how much power is produced by various generators and consumed by various loads, etc.
 * The topology profile (TP): Aggregated information obtained from SSH and EQ. A simplified bus-branch model which we can use to run power flow simulations.
 * The state variable profile (SV): The flow on specific branches, corrected node injections, etc. Typically the output of a simulation system.

In addition, CGMES also cover the following information models:

 * Boundary profiles (EQ_BD and TP_BD): E.g. used to describe transmission systems on the boundary of grid operators' juristictions
 * Geographical location profile: Geographical information that augments the equipment profile
 * Dynamics profile: Information required for computing transient (time-varying) information (like voltage stability, pendulum effects, etc.)
 * Diagram layout profile: Information needed to create model diagrams.

The standards cover a lot, but we'll start by considering the EQ-profile here.

> [!NOTE]
> We'll only cover the basics, but most of what we need to know can be found by reading the HTML documentation (linked in a zip file here): https://www.entsoe.eu/digital/common-information-model/#common-grid-model-exchange-specification-cgmes
> If you don't want to manually download it, then you can also run `uv run python -m sparql_tutorial.download_cgmes docs -o docs/` to download the CGMES documentation and extract it into the `docs/`-directory.
> Once you have downloaded it, you can view the documentation in your browser, e.g. by running `python -m http.server -d docs/HTML` and opening `http://localhost:8000/` in a web browser.


## The node-breaker and bus-branch representations of a power grid

To understand CGMES, it is useful to first consider the two fundamental descriptions of a power grid that the standard defines: the *node-breaker* model and the *bus-branch* model.
The node-breaker model contains very detailed information about the power grid.
Specifically it contains information about generators, loads, transformers and switches in a transmission system and how they are connected.
This means that even if a generator is disconnected from the grid, it can still be included in a node-breaker model, typically with an open switch (i.e. breaker).
You can therefore think of a node-breaker as a detailed digital representation of a single-line diagram.

### The node-breaker model

A node-breaker model describes a power grid with three different data types: *conducting equipment*, *terminals* and *connectivity nodes*.
Conducting equipment represent the physical parts in a power grid, the generators, loads, transformers, switches, etc.
However, the node-breaker model doesn't connect these together directly.
To understand why, consider the following simple electrical circuit (a generator that is directly connected to a load):

![Single line diagram representing the circuit 'Generator' ---- 'Load'](./figures/05_gen_load_sld.svg)

How should we store information about this connection? Should the load know its generator or should the generator know its load?
How about if we have multiple loads connected to one generator?

Instead, we connect components through connectivity nodes.
If two or more conducting components share a connectivity node, then there is direct electrical contact between them.
Also, to connect conducting components to connectivity nodes, we have terminals -- very simple "objects" that contain a single conducting equipment and a single connectivity node.

Let's now consider how to represent the above electrical curcuit with the node breaker model.
We need one connectivity node and two terminals, one to connect the load to the connectivity node and one to connect the generator to the connectivity node:

![Node-breaker representation representing the above circuit: 'Generator' <- 'Terminal' -> 'ConnectivityNode' <- 'Terminal' -> 'Load'](./figures/06_gen_load_eq.svg)

> [!NOTE]
> Generators actually consist of a `SyncronousMachine` (or similar) that is connected to a `GeneratingResource`.
> However, we'll look more at that later.

### Exercises

With pen and paper: Draw a diagram that shows how the following circuits will be represented when we use the node-breaker model

1. 
    * <details><summary>Single line diagram</summary><img alt="Single line diagram representing the circuit 'Generator' --- 'Switch' --- 'Load'" src="./figures/07_gen_switch_load_sld.svg" /></details>  
    * [*Solution*](./figures/08_gen_switch_load_eq.svg)

2. 
    * <details><summary>Single line diagram</summary><img alt="Single line diagram representing the circuit 'Load' --- 'Switch' --- 'Generator' --- 'Switch' --- 'Load'" src="./figures/09_gen_switch_2xload_sld.svg" /></details>  
    * [*Solution*](./figures/10_gen_switch_2xload_eq.svg)

### Reflection

We see that the while node-breaker formulation adds a lot of extra data structures.
However, most of these extra data structures are neccessary to obtain a good machine readable representation of single line diagrams.
Furthermore, while not a part of the simple CIM schemas, there are also constraints on the number of terminals of conducting equipment.
All loads and generators only have one terminal, switches ACLines, etc. have two terminals and transformers have one terminal for each winding.

### The bus-branch model

A downside with the node-breaker model is that it isn't suited for physical simulations.
Instead, we use a different aggregated data model for physical simulations: the bus-branch model.

The bus-branch model is a simplified model where all conducting equipment on the same voltage level that is connected with zero impedance and with zero impedance is grouped into one topological node, or "bus".
These buses are connected with transformers, powerlines, etc. that either have impedance or changes the voltage level.
The reason we group together conducting equipment into buses this way is that if two components are short circuited (i.e. connected with zero impedance), then there is no way to mathematically distinguish the behaviour of one component from that of another.

Consider, for example, the following power circuit

![Single line diagram representing a circuit with two generators connected with a switch, two AC-lines and two loads](./figures/11_2x_gen_switch_2xacline_2xload_sld.svg)

A Node breaker representation of this model would be
![A network diagram showing the node-breaker representation of a circuit with two generators connected with a switch, two AC-lines and two loads](./figures/12_2x_gen_switch_2xacline_2xload_eq.svg)

However, a bus-branch representation is much simpler.
It either has three topological nodes and two branches (if the switch is closed):
![A network diagram showing a bus-branch representation of a circuit with two generators connected with a switch, two AC-lines and two loads](./figures/13_2x_gen_switch_2xacline_2xload_tp_1.svg)
or four topological nodes and two branches (if the switch is open):
![A network diagram showing a bus-branch representation of a circuit with two generators connected with a switch, two AC-lines and two loads](./figures/14_2x_gen_switch_2xacline_2xload_tp_2.svg)

The number of nodes in a bus-branch model and their connectivity is, in other words, not defined by data solely stored in the EQ-profile.
We also need the status of switches, which is stored in the SSH-profile.

> [!NOTE]
> Our description of how topological nodes are formed is a bit imprecise.
> It is possible to have e.g. an ACLine with zero impedance, which leads to two topological nodes.
> However, that is not common, and the description fits the intuitive model you probably want for a bus-branch model.

### Exercises

What are the buses and branches of the following node-breaker models:

1. 
   * <details><summary>Single line diagram</summary> <img src="./figures/15_2x-gen-2x-switch-acline-load-closed-sld.svg" alt="Single line diagram representing a circuit with two generators connected to closed switches that are connected to an AC-line (the generators are in parallel) that is connected to a load" /></details>
   * <details><summary>Node-breaker representation</summary> <img src="./figures/16_2x-gen-2x-switch-acline-load-closed-eq.svg" alt="Node-breaker view of a circuit with two generators connected to closed switches that are connected to an AC-line (the generators are in parallel) that is connected to a load" />
   * [*solution*](./figures/17_2x-gen-2x-switch-acline-load-closed-tp.svg)
2. 
   * <details><summary>Single line diagram</summary> <img src="./figures/18_2x-gen-2x-switch-acline-load-open-sld.svg" alt="Single line diagram representing a circuit with two generators connected to switches (one closed, one open) that are connected to an AC-line (the generators are in parallel) that is connected to a load" /></details>
   * <details><summary>Node-breaker representation</summary> <img src="./figures/19_2x-gen-2x-switch-acline-load-open-eq.svg" alt="Node-breaker view of a circuit with two generators connected to switches (one closed, one open) that are connected to an AC-line (the generators are in parallel) that is connected to a load" /></details>
   * [*solution*](./figures/20_2x-gen-2x-switch-acline-load-open-tp.svg)

### Reflection

We see that while the node-breaker data model doesn't change fundamentally by modifying equipment state, the bus-branch model does.
However, the bus-branch model can change drastically by only closing a switch.
Still, by combining the information in the EQ-profile and the SSH-profile, we can compute all data fields we need for a bus-branch model as well.

## Next up
You are now ready for the final part of this tutorial -- the EQ-profile: [link](./05_the_eq_profile.md)
