---
title: 'Constructing Knowledge Graphs With Neo4j GraphRAG for Python'
date: 2025-12-03 15:34:59 +00:00
tags: [graphrag, neo4j, python]
canonical_url: https://neo4j.com/blog/developer/knowledge-graphs-neo4j-graphrag-for-python/
---

A knowledge graph is an organized representation of real-world entities and their relationships. [Knowledge graphs](https://neo4j.com/blog/knowledge-graph/what-is-knowledge-graph/) provide a structured way to represent entities, their attributes, and their relationships, allowing for a comprehensive and interconnected understanding of the information.

Creating knowledge graphs from unstructured data can be complex, involving multiple steps of data query, cleansing, and transforms. You can use the text analysis capabilities of LLMs to help automate knowledge graph creation.

The [Neo4j GraphRAG for Python (neo4j_graphrag) package](https://neo4j.com/docs/neo4j-graphrag-python/current/) includes a Knowledge Graph Builder to help you convert your unstructured and structured data.

## Knowledge Graph Builder

The [`SimpleKGPipeline`](https://neo4j.com/docs/neo4j-graphrag-python/current/user_guide_kg_builder.html) class provides a pipeline that implements a series of steps to create a knowledge graph from unstructured data:

1. Load the text
2. Split the text into chunks
3. Create embeddings for each chunk
4. Extract entities from the chunks using an LLM
5. Write the data to a Neo4j database

![The SimpleKGPipeline steps, left to right: a document into a data loader, then a text splitter, chunk embedder, and entity and relation extractor, which draws on a schema builder and a lexical graph builder, then a graph pruner, KG writer and entity resolver, both reading and writing a Neo4j database](/assets/img/2025/12/constructing-knowledge-graphs-with-neo4j-graphrag-for-python-1.png)

For example, you could turn the Neo4j Wikipedia page into a graph representing Neo4j the organization and the database.

![The Neo4j Wikipedia article on the left, an arrow labelled SimpleKGBuilder, and on the right a small graph: a Neo4j GraphDatabase node DEVELOPED_BY a Neo4j Inc Company node and IMPLEMENTED_IN a Java ProgLanguage node](/assets/img/2025/12/constructing-knowledge-graphs-with-neo4j-graphrag-for-python-2.png)

The `SimpleKGPipeline` only requires a Neo4j connection, an embedding model, and an LLM to turn your documents into a knowledge graph.

```python
import os
from dotenv import load_dotenv
load_dotenv()

import asyncio

from neo4j import GraphDatabase
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.embeddings import OpenAIEmbeddings
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline

neo4j_driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
)
neo4j_driver.verify_connectivity()

llm = OpenAILLM(
    model_name="gpt-4o",
    model_params={
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
)

embedder = OpenAIEmbeddings(
    model="text-embedding-ada-002"
)

kg_builder = SimpleKGPipeline(
    llm=llm,
    driver=neo4j_driver,
    neo4j_database=os.getenv("NEO4J_DATABASE"),
    embedder=embedder,
    from_pdf=True,
)

pdf_file = ".my_document.pdf"
result = asyncio.run(kg_builder.run_async(file_path=pdf_file))
print(result.result)
```

You can learn how to use and customize the `SimpleKGPipeline` in a new [GraphAcademy](https://graphacademy.neo4j.com) course: [Constructing Knowledge Graphs with Neo4j GraphRAG for Python](https://graphacademy.neo4j.com/courses/genai-graphrag-python/).

![Course banner: Neo4j GraphAcademy, Constructing Knowledge Graphs with Neo4j GraphRAG for Python — learn how to use Generative AI and LLMs to convert unstructured data into knowledge graphs](/assets/img/2025/12/constructing-knowledge-graphs-with-neo4j-graphrag-for-python-3.png)

You’ll also learn how to:

- Create text splitters and define chunks
- Implement custom data loaders
- Define a schema for your lexical (unstructured) graph to ensure that you’re extracting the data you need
- Add structured data alongside your unstructured data
- Create [GraphRAG](https://neo4j.com/essential-graphrag/) pipelines and retrievers to access your knowledge graph

## Summary

Knowledge graphs help you organize and make sense of your data. Learn how to create them in the GraphAcademy [Constructing Knowledge Graphs with Neo4j GraphRAG for Python](https://graphacademy.neo4j.com/courses/genai-graphrag-python/) course.

---

*Originally published on [Neo4j Developer Blog](https://neo4j.com/blog/developer/knowledge-graphs-neo4j-graphrag-for-python/) on 3 December 2025.*
