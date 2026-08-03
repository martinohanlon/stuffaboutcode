---
title: 'RAG vs GraphRAG — Two Retrievers, One Question'
date: 2026-07-22 01:00:30 +01:00
tags: [graphrag, neo4j, ai]
canonical_url: https://graphacademy.neo4j.com/blog/rag-vs-graphrag-demo
---

Ask for “a highly rated action movie about travelling to other planets” and two systems can hand you two very different answers. One reads the plot of every film and returns whatever sounds closest. The other knows which films share a genre, who acted in them, and how thousands of people actually rated them.

Same question, same data, different retrieval. I built a small demo to make that difference impossible to miss, and it runs on exactly the concepts and dataset you work through in [Neo4j & GenAI Fundamentals](https://graphacademy.neo4j.com/courses/genai-fundamentals).

![](/assets/img/2026/07/rag-vs-graphrag-two-retrievers-one-question-1.png)

## What RAG and GraphRAG actually do

Retrieval-augmented generation (RAG) gives a large language model the context it needs to answer a question. Instead of relying on what the model memorised during training, you retrieve relevant data and pass it in alongside the question.

The most common form is vector RAG. You embed your text as vectors, store them, and at query time find the chunks that are semantically closest to the question. It is good at “find me something that reads like this”.

![](/assets/img/2026/07/rag-vs-graphrag-two-retrievers-one-question-2.png)

GraphRAG adds the missing dimension: relationships. A vector search can tell you a film’s plot is similar to your query, but it cannot tell you the film’s genre, its cast, or its average rating unless that text happens to sit in the same chunk. A graph can. GraphRAG takes the results of a vector search and traverses the graph to pull in connected facts, so the model answers with structure, not just similarity.

![](/assets/img/2026/07/rag-vs-graphrag-two-retrievers-one-question-3.png)

## The recommendations dataset

The demo runs on Neo4j’s public dataset, the same one used throughout the course. It models movies, people connected to them, and a lot of ratings.

![](/assets/img/2026/07/rag-vs-graphrag-two-retrievers-one-question-4.png)

A `Movie` is `IN_GENRE` of one or more genres, a `Person` `ACTED_IN` or `DIRECTED` it, and a `USER` `RATED` it. Each movie also carries a plot summary, which is embedded as a 1536-dimension vector and stored in a vector index called `moviePlots`.

That single graph holds everything both retrievers need. Vector RAG uses only the plot embeddings. GraphRAG uses the embeddings and the relationships around them.

## Seeing the difference

The [RAG vs GraphRAG demo](https://github.com/martinohanlon/rag-x-graphrag) is a terminal application that sends your question to two agents at once and shows their answers side by side.

- The **RAG** agent uses a `VectorRetriever`. It finds the movies whose plot embeddings are nearest to your query and passes those plots to the LLM.
- The **GraphRAG** agent uses a `VectorCypherRetriever`. It starts from the same vector hits, then runs a Cypher query to enrich them with genres, cast, directors, and user ratings before the LLM ever sees them.

{% include youtube.html id="izlF3hulft8" %}

Both retrievers are built with the [neo4j-graphrag](https://neo4j.com/docs/neo4j-graphrag-python/current/) Python package, so the only meaningful difference between them is how much of the graph they retrieve. Ask for the highest-rated action film about other planets, and plain vector RAG returns something plot-similar. GraphRAG returns something plot-similar that is also an action film with a genuinely high average rating, because it retrieved the ratings and genres to reason over.

## Run it yourself

The [installation instructions are on GitHub](https://github.com/martinohanlon/rag-x-graphrag#readme). The demo connects to the public dataset out of the box, so all you need is Python and an OpenAI API key to try it on your own questions.

## Learn to build it yourself

The concepts underneath the demo — embeddings, vector indexes, retrievers, and graph-enhanced retrieval, are what make it work, and they are exactly what [Neo4j & GenAI Fundamentals](https://graphacademy.neo4j.com/courses/genai-fundamentals/) teaches. You will build the same `VectorRetriever` and `VectorCypherRetriever` against this dataset, write the retrieval Cypher yourself, and see the context change as you do.

> **[Neo4j & GenerativeAI Fundamentals](https://graphacademy.neo4j.com/courses/genai-fundamentals/)** — Learn how Neo4j and GraphRAG can support your Generative AI projects

If the side-by-side answers made you curious about why the graph wins, the course is where you find out how to build it.

---

*Originally published on [Neo4j GraphAcademy](https://graphacademy.neo4j.com/blog/rag-vs-graphrag-demo) on 22 July 2026.*
