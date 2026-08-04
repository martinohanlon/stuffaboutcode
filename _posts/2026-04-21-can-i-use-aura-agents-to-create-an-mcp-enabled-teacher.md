---
title: 'Can I use Aura Agents to create an MCP enabled teacher?'
date: 2026-04-21 14:04:57 +01:00
tags: [neo4j, agents, mcp]
canonical_url: https://neo4j.com/blog/graph-database/can-i-use-aura-agents-to-create-an-mcp-enabled-teacher-2/
---

If you have used an agent to code you will know they are great at providing solutions to problems. Unfortunately they are not as good at teaching you to do it yourself.

Fine tuned to deliver solutions, they lack good context relating to how to teach complex subjects, often missing key points, providing inconsistent results, and don’t build confidence.

```text
[Human]
Create a function which connects to my Neo4j databases and runs a 
Cypher statement.

[AI] 
Sure, here is a new function, run_cypher(driver, database, cypher).

[Human]
How does this work?

[AI]
It runs a cypher statement using the neo4j.GraphDatabase driver 
instance and database name and returns a list of Record objects.

[Human]
But how does it actually work? What are the concepts I need to know? 
How do I do this myself?
```

I wanted to change this and provide coding agents (VS Code, Cursor, etc) with access to Neo4j’s [GraphAcademy](https://graphacademy.neo4j.com?ref=martin-aura-agents) content and teaching approaches.

GraphAcademy is Neo4j’s free online training platform and provides learners with knowledge and skills to use Neo4j to solve real world problems, including a new course on [Building Agents on Neo4j Aura](https://graphacademy.neo4j.com/courses/aura-agents/?ref=martin-aura-agents).

## The plan

1. Create a [Neo4j graph database](https://neo4j.com/product/neo4j-graph-database) on [Aura](https://neo4j.com/product/auradb/) of [GraphAcademy](https://graphacademy.neo4j.com?ref=martin-aura-agents) lessons.
2. Build an [Aura agent](https://neo4j.com/product/aura-agent/) with tools to search, retrieve, and format lessons.
3. Expose the agent as an MCP server that can connect to an agent.

![GraphAcademy MCP POC architecture](/assets/img/2026/04/can-i-use-aura-agents-to-create-an-mcp-enabled-teacher-1.png)

## The graph database

[GraphAcademy’s lesson content is open source](http://github.com/neo4j-graphacademy/courses) and written in Asciidoc.

![GraphAcademy lessons](/assets/img/2026/04/can-i-use-aura-agents-to-create-an-mcp-enabled-teacher-2.png)

I used [asciidoctor-reducer](https://github.com/asciidoctor/asciidoctor-reducer) to turn the lessons into single files containing all the text, code, examples, and questions by injecting attributes and resolving any includes.

Each lesson was chunked into sections, embeddings were created using [OpenAI’s text-embedding-3-small model](https://developers.openai.com/api/docs/models/text-embedding-3-small), and stored in Neo4j Aura with associated meta data about the lesson (course structure, slugs, names, urls, etc).

![Graph model](/assets/img/2026/04/can-i-use-aura-agents-to-create-an-mcp-enabled-teacher-3.png)

With the data in Neo4j I could search to find complete lessons based on something I want to learn (a `$subject`) e.g. *Teach me about filtering with Cypher WHERE clauses*.

```cypher
WITH ai.text.embed(
  $subject, 
  'OpenAI', 
  { token: $token, model: 'text-embedding-3-small' }
) AS userEmbedding

MATCH (c:Chunk)
SEARCH c IN (
  VECTOR INDEX chunkText
  FOR userEmbedding
  LIMIT $k
) SCORE AS score
WHERE score > 0.7

MATCH (c)<-[:HAS_CHUNK]-(l:Lesson)

RETURN 
  l.slug as slug, 
  l.title as title, 
  l.url as url, 
  l.text as lesson, 
  avg(score) as score

ORDER BY score DESC
```

The Cypher query:

1. Creates an embedding of the `$subject` using the same OpenAI text-embedding-3-small model that was used to create embeddings of the lesson chunks.
2. Searches the `chunkText` vector index and return chunks that have a similarity `score > 0.7`.
3. Matches the lessons for the chunks.
4. Returns the lesson data, aggregating by the average score of the lesson chunks found. Averaging the score ensures single high scoring chunks don’t result in the query returning less relevant lessons as the top match.

![Results of the cypher to search lessons](/assets/img/2026/04/can-i-use-aura-agents-to-create-an-mcp-enabled-teacher-4.png)

## Aura Agent

Aura Agents allow you to create a fully functional GraphRAG agent connected to your Neo4j Aura database.

I used an [Aura agent](https://neo4j.com/product/aura-agent/) to provide the entry point to the lessons and generate responses to queries and questions.

Aura Agents require:

- a name — to indicate what the agents does.
- a prompt — that describes the agent’s purpose, approach, and instructions.
- a set of tools — to retrieve data from Neo4j as context to the questions.

The prompt instructs the agent to present the GraphAcademy lessons as a learning experience, including ensuring there is an objective, that misconceptions are challenged, and options given for next steps.

```text
Find and present Neo4j GraphAcademy lessons and appropriate progression 
to the follow on topics.

Provide lessons that:

- are standalone and meet a learning objective
- include examples and code snippets where relevant
- show outcomes and results of actions
- where there are potential misconceptions pose questions 
  and answers that challenge them
- have recommendations for next steps.
- provide a link to the full lesson to learn more.
- give options to either: continue to the next lesson, explore 
  related topics, or get more information.

Use the tool "get lesson for a chunk" after "search lesson chunks".
```

![Neo4j Aura agent setup](/assets/img/2026/04/can-i-use-aura-agents-to-create-an-mcp-enabled-teacher-5.png)

The agent accesses the lesson data through its tools. The tools are chosen by the agent based on the task. The agent will use as many of the tools as required to complete the task.

The agent only needs access to a relatively smaller number of tools which search and retrieve the lesson:

- **search for a lesson** — semantic search for lesson chunks
- **get a complete lesson** — gets a complete lesson
- **get next lesson** — gets the next lesson in the sequence

![Aura agent tools](/assets/img/2026/04/can-i-use-aura-agents-to-create-an-mcp-enabled-teacher-6.png)

Using the smallest number of tools to provide access to the data often results in better outcomes and tool use.

The agent will use the tools to find and present teaching content about Neo4j.

When given a query such as “How to use WITH in Cypher”, the agent will search for a lesson, get the complete lesson for the chunk returned, and provide a lesson.

![The agent preview answering "How to use WITH in Cypher" alongside its list of enabled tools](/assets/img/2026/04/can-i-use-aura-agents-to-create-an-mcp-enabled-teacher-7.png)

The lessons are already structured for the purpose and the prompt is enough for the agent to provide good responses.

The agent will provide follow on tasks and allow the user to progress through to the next lesson in the course.

![The end of a lesson, with recommendations for next steps and three numbered options to continue](/assets/img/2026/04/can-i-use-aura-agents-to-create-an-mcp-enabled-teacher-8.png)

## MCP Server

It's important we meet developers were they are and to do that I need to provide external access to my agent.

An Aura agent can be accessed externally via a HTTPS endpoint or as an MCP server.

![The agent's Access settings, with External selected and "Enable MCP server" switched on](/assets/img/2026/04/can-i-use-aura-agents-to-create-an-mcp-enabled-teacher-9.png)

Agent applications (VS Code, Cursor, etc) typically have the ability to interact with MCP servers to complete tasks.

You can [add your Aura agent as an MCP server](https://neo4j.com/developer/genai-ecosystem/aura-agent-getting-started/#_part_4_deploying_the_agent_to_rest_mcp) to you agent application allowing it to use the responses your Aura agent as context to your queries.

When asking the VS Code agent to *“Teach me how to run a Cypher statement using the Neo4j Python driver”,* the agent will find lessons from GraphAcademy and create responses using the lessons content and structure.

![Aura Agent used in VS Code](/assets/img/2026/04/can-i-use-aura-agents-to-create-an-mcp-enabled-teacher-10.gif)

```text
[HUMAN]
Teach me how to run a Cypher statement using the Neo4j Python driver

[AI]
I’ll quickly pull the official Neo4j learning guidance first, then I’ll give 
you a concise, practical Python example you can run immediately.

[TOOL]
Ran Neo4j Learning
Input:
{
  "query": "How to run a Cypher statement using the Neo4j Python driver
}
Output:
Here's a lesson on how to run a Cypher statement using the Neo4j Python driver,
including connection setup and query execution.
...continued...

[AI]
Great use case. Here is the simplest way to run a Cypher statement with the 
Neo4j Python driver.

1. Install the driver
pip install neo4j

2. Use this minimal script:

from neo4j import GraphDatabase

URI = "neo4j+s://<your-instance-id>.databases.neo4j.io"
USER = "neo4j"
PASSWORD = "<your-password>"

def run_query():
    # Create a driver (connection factory)
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    try:
        # execute_query is the easiest API in driver v5+
        records, summary, keys = driver.execute_query(
            "RETURN 'Hello, Neo4j!' AS message"
        )

        for record in records:
            print(record["message"])

        print("Query ran successfully.")
        print("Database:", summary.database)
    finally:
        driver.close()

if __name__ == "__main__":
    run_query()

3. Run it
python your_script.py

Parameterized Cypher example (recommended):

records, summary, keys = driver.execute_query(
    "RETURN $name AS name",
    name="Martin"
)
print(records[0]["name"])

Why this matters:

1. Use parameters like $name instead of string concatenation for safety 
   and performance.
2. For Neo4j Aura, use neo4j+s in the URI.
3. Close the driver when done.

If you want, I can also give you:

1. A read/write transaction example with session.execute_read and 
   session.execute_write.
2. A small reusable Neo4j client class you can drop into your project.
```

The response from the agent is structured as a lesson, includes good progression from a simple example, adding features, explaining the approaches used, and giving options to continue learning.

All the code and resources are in the repository [github.com/martinohanlon/ga-mcp-poc](https://github.com/martinohanlon/ga-mcp-poc).

## Next steps

This proof-of-concept is just the beginning, an MCP server is part of our ongoing development of GraphAcademy. We are keen to meet developers where they are, and some of them are in code development environments.

You can learn the skills to create your own graph, MCP server, and Aura agent in the [GraphAcademy](https://graphacademy.neo4j.com?ref=martin-aura-agents) courses [Introduction to Vector Indexes and Unstructured Data](https://graphacademy.neo4j.com/courses/llm-vectors-unstructured/?ref=martin-aura-agents), [Building GraphRAG Python MCP tools](https://graphacademy.neo4j.com/courses/genai-mcp-build-custom-tools-python/?ref=martin-aura-agents), and [Building Agents in Neo4j Aura](https://graphacademy.neo4j.com/courses/aura-agents/?ref=martin-aura-agents).

---

*Originally published on [Neo4j](https://neo4j.com/blog/graph-database/can-i-use-aura-agents-to-create-an-mcp-enabled-teacher-2/) on 21 April 2026.*
