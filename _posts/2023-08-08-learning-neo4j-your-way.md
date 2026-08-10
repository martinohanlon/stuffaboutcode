---
title: 'Learning Neo4j Your Way'
date: 2023-08-08 02:10:15 +01:00
tags: [neo4j, graph-database, learning]
canonical_url: https://neo4j.com/blog/developer/learning-neo4j-your-way/
---

Hi, I recently joined the Neo4j developer relations team as the Technical Curriculum Developer.

My role is centered around developing Neo4j educational resources to support developers. I have a strong background in computer science education. My previous role was creating online learning experiences for the Raspberry Pi Foundation, and although I worked in software development and architecture for many years, my knowledge of Neo4j was limited.

Therefore, one of my first priorities was to educate myself in Neo4j.

> Learning something new is hard! Multiple factors affect how hard it is, such as the resources available to you, your experience, knowledge and skills, and your own motivation. Applying a structure to your learning can help you achieve your objective.

Come with me on an exploration of how I structured my learning using Neo4j’s developer relations output and educational content.

## Make Your Learning Effective

Most people have an understanding of how they like to obtain knowledge and learn new skills. You may not be able to articulate how you like to learn, but you will be aware of the ways of learning that excite you or bore you!

> Do you relish the opportunity to sit down with a text book or fear and loath it?

I personally thrive when given a variety of learning opportunities and particularly when it's accessible in short pieces with time to practice and get hands-on.

Neo4j’s investment in developer support and education resources is impressive, and there are plenty of resources and opportunities to learn and acquire new skills.

## Create a Goal

To structure and support my learning, I set myself these initial learning objectives:

1. Understand the benefits and use cases of graphs and graph databases
2. Be able to design a graph data model to fulfill a typical use case
3. Understand the options for loading data into a Neo4j database
4. Use Cypher to load, query, and manipulate data in a graph database
5. Use simple Graph Data Science tools and techniques to answer questions
6. Interact with a Neo4j database using Python

To make my learning effective, I also wanted to create my own project. A project excites me, it allows me to structure my learning so I get the opportunity to get hands-on, and it motivates me to continue.

From my initial understanding of graphs and Neo4j, I had an idea about mapping the physical world, understanding the relationship between places and how you move between them.

I have snowboarded for over 30 years, and I love nothing more than exploring the mountains. Large ski resorts are a complex system of interconnected trails and lifts.

![A section of the Grand Massif ski area in France](/assets/img/2023/08/learning-neo4j-your-way-1.png)

I planned to use a Neo4j graph database to allow me to answer the following questions:

- What lifts and trails are there?
- What trails have a specified difficulty?
- What trails are accessible from a specific lift?
- Is there an accessible route between 2 points?
- What is the shortest path between 2 points?

## A Learning Pathway

To help me achieve my goals, I created a learning pathway:

1. Fundamentals — Understanding Neo4j and graphs
2. Data modeling — How to structure data in a graph
3. Importing data — The options and processes for moving data into Neo4j
4. Query and analysis — Answering questions and running queries
5. Programming and integration — Integrating a graph database into an application

The [Beginners collection of courses](https://graphacademy.neo4j.com/categories/beginners/) on Neo4j’s GraphAcademy is an example of a learning pathway that supports you in obtaining the skills and knowledge required to complete the [Neo4j Certified Professional](https://graphacademy.neo4j.com/courses/neo4j-certification/) certification.

![The beginner pathway of courses on Graph Academy](/assets/img/2023/08/learning-neo4j-your-way-2.png)

The beginner courses were my starting point for obtaining fundamental knowledge and skills.

### Fundamentals

I started my learning with the [Neo4j Fundamentals](https://graphacademy.neo4j.com/courses/neo4j-fundamentals/) and [Cypher Fundamentals](https://graphacademy.neo4j.com/courses/cypher-fundamentals/) courses on [GraphAcademy](https://graphacademy.neo4j.com/). These courses introduce graph theory, the Neo4j graph database, and the Cypher query language. These courses gave me the initial knowledge and skills needed to interact with Neo4j and understand the key use cases.

![The seven bridges of Königsberg, a rite of passage for anyone learning about graphs](/assets/img/2023/08/learning-neo4j-your-way-3.png)

I wanted to increase my knowledge of the graph database sector, so I also started reading the complementary ebook [Graph Databases by Ian Robinson, Jim Webber, and Emil Eifrem](https://neo4j.com/graph-databases-book/).

![The cover of the O'Reilly book Graph Databases, second edition, by Ian Robinson, Jim Webber and Emil Eifrem](/assets/img/2023/08/learning-neo4j-your-way-4.png)

Once I had secured my fundamental knowledge of Neo4j, I looked for sources of ski resort data for my project. I discovered that trails and lifts were included in [OpenStreetMap](https://www.openstreetmap.org/) (OSM).

I wrote an [Overpass Turbo](http://overpass-turbo.eu/) query to export the lift (aerialway) and trail (piste) data in JSON.

```text
[out:json][timeout:25];
area[name="Val Thorens"]->.a;
(  
  way["piste:type"](area.a);  
  way["aerialway"](area.a);  
);
out body;
>;
out skel qt;
```

My plan was to use Overpass Turbo to export the data from OSM, create a Python program to convert it to CSV, and load it into Neo4j. I envisaged a graph of trail, lift, and position nodes using relationships to store how you would progress from one place to the next.

![A pipeline diagram: a ski piste map labelled overpass turbo, an arrow marked JSON to the Python logo, an arrow marked CSV to the Neo4j logo](/assets/img/2023/08/learning-neo4j-your-way-5.png)

### Data Modeling

To understand graph data modeling and the potential for graph databases, I completed the [Graph Data Modeling Fundamentals](https://graphacademy.neo4j.com/courses/modeling-fundamentals/) course, which explores how to design a Neo4j graph and best practices.

I learned about storing geospatial data in Neo4j from the [Geospatial Data in your Graph](https://www.youtube.com/watch?v=djMsdSxvd2E) livestream on [Neo4j’s Twitch channel](https://www.twitch.tv/neo4j).

Neo4j Developer Advocate William Lyon has created a useful [Spatial Cypher Cheat Sheet](https://lyonwj.com/blog/spatial-cypher-cheat-sheet) about managing geospatial data using Cypher.

The Twitch channel often has presenters from the Neo4j community and has helped me to expand my knowledge of the use of Neo4j and graph databases. The stream on [GraphTFT — a team builder app for Teamfight tactics](https://www.youtube.com/watch?v=n5mo4bqBEPY) is a great example of how Neo4j can be used to understand relationships.

I developed a data model for my project, which incorporated what I have learned about graph databases, Neo4j, and the ski resort data I exported from OpenStreetMap.

![A data model: Lift and Trail nodes, each carrying name and type properties, both joined by IS_ROUTE to a Route node, which joins to a Position node by START, END and ON_ROUTE, with Position nodes chained to each other by NEXT](/assets/img/2023/08/learning-neo4j-your-way-6.png)

### Importing Data

I completed the [Graph Academy](https://graphacademy.neo4j.com/) course [Importing CSV Data into Neo4j](https://graphacademy.neo4j.com/courses/importing-data/) as my starting point for learning about importing data. The course gave me an understanding of the options available, how to use [Neo4j’s Data Importer](https://data-importer.neo4j.io/), and an overview of the [`LOAD CSV`](https://neo4j.com/docs/cypher-manual/current/clauses/load-csv/) statement in Cypher.

I created a [Python program to generate CSV files](https://github.com/martinohanlon/trail_and_run/blob/main/data/parse_data.py) from the OSM data, which I could import into Neo4j and generate the data model I had created.

I signed up for [Neo4j’s AuraDB](https://neo4j.com/cloud/platform/aura-graph-database/) and set up a free Neo4j database in the cloud in a couple of minutes.

Using the [data importer](https://data-importer.neo4j.io/connection/connect) allowed me to quickly create a data model and get started on exploring the data, but as I looked to expand the data model, I found I needed to modify the source CSV files to support more complex relationships.

At this point, I had a learning opportunity. I could either:

1. Modify my Python program to get the data into the right shape and continue to use Data Importer.
2. Use `LOAD CSV` and Cypher to manipulate the existing CSV data at import.

While changing my Python program would have been quicker and easier I chose to use Cypher. My knowledge of Cypher is limited, and it gave me an opportunity to practice what I had learned and develop my knowledge.

> Choosing a path which exposes gaps in your learning will help you stretch yourself and expand your knowledge and skills.

Neo4j’s documentation includes useful information on data importing, such as the [Import your data into Neo4j](https://neo4j.com/docs/getting-started/data-import/) guide, the [Cypher manual](https://neo4j.com/docs/cypher-manual/current/introduction/), and the [LOAD CSV reference](https://neo4j.com/docs/cypher-manual/current/functions/load-csv/).

I generated a [data load process in Cypher](https://github.com/martinohanlon/trail_and_run/blob/main/load/load_data.cypher) which took the CSV data and built the data model.

This code snippet loads lift data from a [CSV file](https://github.com/martinohanlon/trail_and_run/blob/main/data/flaine_lift_data.csv) and adds the data to the graph.

```cypher
// lifts
LOAD CSV WITH HEADERS
FROM 'file:///test_lift_data.csv'
AS row
MATCH (r:Route {id: toInteger(row.id)})
SET r:Lift,
r.name = row.name,
r.type = row.type,
r.capacity = toInteger(row.capacity),
r.occupancy = toInteger(row.occupancy),
r.oneway = CASE row.oneway WHEN "yes" THEN true WHEN "no" THEN false ELSE null END;
```

Loading the data in Cypher allowed me to practice what I had learned and develop my skills.

### Queries and Analytics

I explored the data graph I had created, writing queries to answer the questions I had created, testing against known scenarios, and extending the data range.

I refactored the data model removing duplication and using multiple labels to determine whether a Route node was a Trail or a Lift.

![The refactored data model: a single node carrying the Route, Lift and Trail labels together with id, name, type and difficulty properties, joined to a Position node by START, END and ON_ROUTE, with Position nodes chained by NEXT](/assets/img/2023/08/learning-neo4j-your-way-7.png)

The [Intermediate Cypher Queries course](https://graphacademy.neo4j.com/courses/cypher-intermediate-queries/) on [GraphAcademy](https://graphacademy.neo4j.com) taught me more advanced Cypher queries and complex patterns.

I paired with my colleagues to learn about how to use shortest path algorithms and add properties such as distance and difficulty to relationships so I could use weighting to find alternative paths.

> It is easy to forget that pairing is an opportunity for both people to learn new skills but also to find new ways of working.

The Graph database and Cypher queries I developed allowed me to determine how to navigate ski resorts.

For example, if I was at the top of the “Lapiaz” lift, how could I get to the bottom of the “Lutin” trail?

![A piste map of the Grandes Platieres area, with a Start marker at the top of the Lapiaz lift and an End marker at the bottom of the Lutin trail](/assets/img/2023/08/learning-neo4j-your-way-8.png)

I created a Cypher query to find the start and end positions and used the `shortestPath` function to find a route between the 2 points.

```cypher
MATCH (l:Lift{name: "Lapiaz"})-[:END]->(startPos:Position)
MATCH (endPos:Position)<-[:END]-(t:Trail{name: "Lutin"})
MATCH path = shortestPath(
    (startPos)-[:NEXT*..100]->(endPos)
)
RETURN l, path, t
```

![The query result in Neo4j Browser: a long chain of Position nodes linked by NEXT, running from the red Lapiaz node round to the green Lutin node](/assets/img/2023/08/learning-neo4j-your-way-9.png)

### Programming and Integration

I wanted to use Neo4j within an application to help me learn about the end-to-end use of Neo4j.

I am an experienced Python programmer, and while I would have gained other skills from using a different language, my goal was to understand Neo4j integration options and the drivers, not learn a new language.

The [Using Neo4j from Python](https://neo4j.com/docs/getting-started/languages-guides/neo4j-python/) developer guide got me started installing the Python Driver and getting an example application running.

The GraphAcademy course [Building Neo4j Applications with Python](https://graphacademy.neo4j.com/courses/app-python) taught me about the driver in more detail, including executing read and write queries, managing transactions, and processing returned data.

I developed a [Python application](https://github.com/martinohanlon/trail_and_run/blob/main/app/where_can_I_go.py) to access the ski resort data and show the route options from specific positions.

![A small desktop application called Route options: drop-downs to pick a position, set to the END of the Aujon Lift, and below them two suggestions, take trail 'Cornaline' or trail 'Calcedoine', both easy downhills](/assets/img/2023/08/learning-neo4j-your-way-10.png)

This helped me identify several new areas for my own learning, such as indexing and query optimization.

You can view the complete project code, including the data extract, data model, load process, and Python application, at [github.com/martinohanlon/trail_and_run](https://github.com/martinohanlon/trail_and_run).

## Certifications and Next Steps

I now feel ready to complete my [Neo4j Certified Professional](https://graphacademy.neo4j.com/courses/neo4j-certification/) certification.

Gaining certification is an important step and demonstrates that you have the skills and knowledge required to develop solutions and support others.

On top of the recognition that comes with certification, assessment is an important part of any learning journey. Assessment allows you to recognize the progression you have made and identify gaps in your skills and knowledge; you can use this information to set your next goal and continuously adapt your learning journey.

## Learning With Neo4j

If you are starting on a learning journey, I would recommend:

- Creating a goal
- Setting some easy-to-understand learning objectives
- Structuring your learning so it appeals to and motivates you

The [Neo4j Developers](https://neo4j.com/developer/) page is the place to take your first steps with Neo4j. You will find guides, documentation, and events and be able to access the community of Neo4j developers.

[Neo4j GraphAcademy](http://graphacademy.neo4j.com/) offers a wide range of courses completely free of charge, teaching everything from [Neo4j Fundamentals](https://graphacademy.neo4j.com/courses/neo4j-fundamentals/) to [how to develop software that connects to Neo4j](https://graphacademy.neo4j.com/categories/developer/).

I hope you have as much fun learning Neo4j as I have. I would love to hear about your experience learning Neo4j, our educational content, and particularly [Neo4j GraphAcademy](http://graphacademy.neo4j.com/).

---

*Originally published on [Neo4j](https://neo4j.com/blog/developer/learning-neo4j-your-way/) on 8 August 2023.*
