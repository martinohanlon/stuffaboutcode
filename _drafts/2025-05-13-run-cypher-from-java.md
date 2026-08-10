---
title: 'Run Cypher From Java'
date: 2025-05-13 19:20:03 +01:00
tags: [neo4j, cypher, java]
canonical_url: https://neo4j.com/blog/developer/run-cypher-from-java/
---

Are you a Java developer looking to take advantage of graphs and Neo4j?

There’s a new [GraphAcademy](https://graphacademy.neo4j.com) course called [Using Neo4j with Java](https://graphacademy.neo4j.com/courses/drivers-java/), where you can learn how to integrate the Neo4j Java driver into your Java application.

![Course banner: Using Neo4j with Java — learn how to interact with Neo4j using the Neo4j Java driver, with the Java logo on a dark blue background](/assets/img/2025/05/run-cypher-from-java-1.png)

The most common thing you will need to do when using Neo4j with Java is run a Cypher query and parse the results. The process is really simple:

1. Import the driver
2. Connect to a server
3. Verify the connection
4. Execute a Cypher query
5. Parse the results
6. Close the connection

## Import the Driver

The driver is distributed via Maven, you can find snippets and example POM files on the [Maven Central Repository — neo4j-java-driver package](https://central.sonatype.com/artifact/org.neo4j.driver/neo4j-java-driver/overview).

You’ll need to import the GraphDatabase and AuthTokens classes from the Neo4j driver package:

```java
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.AuthTokens;

public class App {
    public static void main(String[] args) {
        String NEO4J_URI = "bolt://localhost:7687";
        String NEO4J_USERNAME = "neo4j";
        String NEO4J_PASSWORD = "mypassword";

        // Create a new Neo4j driver instance

        // Verify the connection 

        // Execute a Cypher query

        // Parse the results

        // Close the connection

    }
}
```

## Connect to a Server

Create an instance of the `GraphDatabase.driver` class, passing your credentials:

```java
        // Create a new Neo4j driver instance
        var driver = GraphDatabase.driver(
                NEO4J_URI,
                AuthTokens.basic(
                    NEO4J_USERNAME,
                    NEO4J_PASSWORD)
            );
```

## Verify the Connection

You can test the connection by calling the `verifyConnectivity` method:

```java
        // Verify the connection 
        driver.verifyConnectivity();
```

The driver will raise an exception if the connection cannot be made.

## Execute a Cypher Query

The `executableQuery` method executes a Cypher query and returns the results:

```java
        // Execute a Cypher query
        var result = driver.executableQuery(
            "MATCH (c:Customer) RETURN c.name AS name, c.age AS age"
            ).execute();
```

## Parse the Results

The `execute` method fetches a list of records and loads them into memory:

```java
        // Parse the results
        var records = result.records();
        records.forEach(r -> {
            System.out.println(r.get("name"));
            System.out.println(r.get("age"));
        });
```

You can iterate through the records and use `get` to retrieve return values.

## Close the Connection

Once you finish with the driver, call `close` to release any resources:

```java
        // Close the connection
        driver.close();
```

Here’s the complete code that makes a connection, executes a query, and parses the results:

```java
import org.neo4j.driver.GraphDatabase;
import org.neo4j.driver.AuthTokens;

public class App {
    public static void main(String[] args) {
        String NEO4J_URI = "bolt://localhost:7687";
        String NEO4J_USERNAME = "neo4j";
        String NEO4J_PASSWORD = "mypassword";

        // Create a new Neo4j driver instance
        var driver = GraphDatabase.driver(
                NEO4J_URI,
                AuthTokens.basic(
                    NEO4J_USERNAME,
                    NEO4J_PASSWORD)
            );

        // Verify the connection 
        driver.verifyConnectivity();

        // Execute a Cypher query
        var result = driver.executableQuery(
            "MATCH (c:Customer) RETURN c.name AS name, c.age AS age"
            ).execute();

        // Parse the results
        var records = result.records();
        records.forEach(r -> {
            System.out.println(r.get("name"));
            System.out.println(r.get("age"));
        });

        // Close the connection
        driver.close();

    }
}
```

## Learn More

You can learn more about how to use the Neo4j Java driver in the [Using Neo4j with Java course on GraphAcademy](https://graphacademy.neo4j.com/courses/drivers-java).

The course will get you started developing Java applications with Neo4j and covers topics such as passing parameters to queries, dealing with graph data types, and managing transactions.

---

*Originally published on the [Neo4j Developer Blog](https://neo4j.com/blog/developer/run-cypher-from-java/) on 13 May 2025.*
