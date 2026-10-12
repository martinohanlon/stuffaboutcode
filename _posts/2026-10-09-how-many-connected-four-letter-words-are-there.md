---
title: 'How Many Connected Four-Letter Words Are There?'
date: 2026-10-09 10:00:00 +01:00
tags: [neo4j, cypher, shortest-path]
canonical_url: https://graphacademy.neo4j.com/blog/four-letter-word-graph
---

I have been playing [Poople](https://poople.io), a puzzle where you turn a four-letter word into `poop` by changing a single letter at a time.

![A solved Poople puzzle, from rent to poop in six steps](/assets/img/2026/10/how-many-connected-four-letter-words-are-there-1.png)

A few rounds in, I stopped thinking about the puzzle and started wondering about the words. How many four-letter words are there? How many are one letter apart? Can every word reach every other word?

Those are questions about connections, which makes them graph questions. I loaded every four-letter word into Neo4j, linked each pair that differs by one letter, and let Cypher answer the questions.

## Where the words come from

The words come from [dwyl/english-words](https://github.com/dwyl/english-words), an open-source list of over 466,000 English words. The `words_alpha.txt` file contains only alphabetic entries, one per line.

I used `LOAD CSV` to read the file directly from GitHub:

```cypher
CREATE CONSTRAINT word_word IF NOT EXISTS
FOR (word:Word)
REQUIRE word.word IS UNIQUE;

LOAD CSV FROM 'https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words_alpha.txt' AS row
CALL (row) {
  WITH toLower(trim(row[0])) AS word
  WHERE size(word) = 4
  MERGE (:Word {word: word})
} IN TRANSACTIONS OF 1000 ROWS;
```

The statement creates 7,186 `Word` nodes.

The list is generous about what counts as a word. Alongside `care` and `cold` you get abbreviations such as `awol` and `bkgd`, and archaic words such as `yare`.

## Most combinations are not words

With 26 letters in each of four positions, there are 26<sup>4</sup> = 456,976 possible letter combinations. Only 7,186 of them are in the list, about 1.6%.

That sparseness is what makes the puzzle work. Every word has 100 one-letter variations (four positions, 25 other letters each), but on average only 13.7 of them are real words. Most changes lead nowhere. The puzzle is finding the few that do.

## Connecting words without comparing every pair

The obvious (brute force) approach compares every word with every other word and counts the letters that differ. With 7,186 words, that is 25,815,705 comparisons. The work grows with the square of the number of words, O(n<sup>2</sup>).

A better approach only compares words that could be neighbours. Replace one letter of a word with a wildcard and you get a signature. `fate` produces `*ate`, `f*te`, `fa*e` and `fat*`. Two words are one letter apart exactly when they share a signature, so `fate` and `fade` meet at `fa*e`.

Each word gets one signature property per position, and each property gets an index:

```cypher
MATCH (word:Word)
SET word.p0 = '*' + substring(word.word, 1),
    word.p1 = substring(word.word, 0, 1) + '*' + substring(word.word, 2),
    word.p2 = substring(word.word, 0, 2) + '*' + substring(word.word, 3),
    word.p3 = substring(word.word, 0, 3) + '*';

CREATE INDEX word_p0 IF NOT EXISTS FOR (word:Word) ON (word.p0);
CREATE INDEX word_p1 IF NOT EXISTS FOR (word:Word) ON (word.p1);
CREATE INDEX word_p2 IF NOT EXISTS FOR (word:Word) ON (word.p2);
CREATE INDEX word_p3 IF NOT EXISTS FOR (word:Word) ON (word.p3);
```

I then found the neighbours for each word using the indexed signatures:

```cypher
MATCH (source:Word)
MATCH (target:Word {p2: source.p2})
WHERE source.word > target.word
MERGE (source)-[difference:ONE_LETTER_DIFFERENT]->(target)
SET difference.diff = '##' + substring(target.word, 2, 1) + '#';
```

The `source.word > target.word` condition creates each pair once rather than once in each direction. The `diff` property records the letter the target has at the changed position, so `fate` to `fade` stores `##d#`.

I matched all the other neighbours by repeating the patterns:

```cypher
MATCH (source:Word)
MATCH (target:Word {p0: source.p0})
WHERE source.word > target.word
MERGE (source)-[difference:ONE_LETTER_DIFFERENT]->(target)
SET difference.diff = substring(target.word, 0, 1) + '###';

MATCH (source:Word)
MATCH (target:Word {p1: source.p1})
WHERE source.word > target.word
MERGE (source)-[difference:ONE_LETTER_DIFFERENT]->(target)
SET difference.diff = '#' + substring(target.word, 1, 1) + '##';

MATCH (source:Word)
MATCH (target:Word {p3: source.p3})
WHERE source.word > target.word
MERGE (source)-[difference:ONE_LETTER_DIFFERENT]->(target)
SET difference.diff = '###' + substring(target.word, 3, 1);
```

The four passes create 49,326 relationships.

Once the relationships between words have been created, the signature properties and their indexes are no longer needed:

```cypher
DROP INDEX word_p0 IF EXISTS;
DROP INDEX word_p1 IF EXISTS;
DROP INDEX word_p2 IF EXISTS;
DROP INDEX word_p3 IF EXISTS;

MATCH (word:Word)
REMOVE word.p0, word.p1, word.p2, word.p3;
```

## Solving the puzzle with SHORTEST

A puzzle has a target word, the aim to find the fewest changes between `poop` and the target. That is a shortest path problem, and the Cypher `SHORTEST` keyword solves it in one statement.

`SHORTEST 1` returns a single solution:

```cypher
MATCH p = SHORTEST 1 (:Word {word: 'raft'})-[:ONE_LETTER_DIFFERENT]-+(:Word {word: 'poop'})
RETURN p;
```

![Graph of the shortest path from raft to poop: raft, rant, pant, pont, poot, poop, linked by ONE_LETTER_DIFFERENT relationships](/assets/img/2026/10/how-many-connected-four-letter-words-are-there-2.png)

`ALL SHORTEST` returns every solution of the minimum length:

```cypher
MATCH p = ALL SHORTEST
  (:Word {word: 'raft'})-[:ONE_LETTER_DIFFERENT]-+(:Word {word: 'poop'})
RETURN [n IN nodes(p) | n.word] AS ladder, length(p) AS steps;
```

The statement returns the following results:

| ladder | steps |
|---|---|
| `["raft", "rant", "pant", "pont", "poot", "poop"]` | 5 |
| `["raft", "taft", "toft", "toot", "poot", "poop"]` | 5 |
| `["raft", "taft", "toft", "toot", "toop", "poop"]` | 5 |
| `["raft", "rift", "riot", "root", "poot", "poop"]` | 5 |
| `["raft", "rift", "riot", "root", "roop", "poop"]` | 5 |
| `["raft", "laft", "loft", "loot", "poot", "poop"]` | 5 |
| `["raft", "laft", "loft", "loot", "loop", "poop"]` | 5 |
| `["raft", "saft", "soft", "soot", "poot", "poop"]` | 5 |

> **[Intermediate Cypher Queries](https://graphacademy.neo4j.com/courses/cypher-intermediate-queries/)**

## The most connected words

A `COUNT` subquery counts each word's neighbours:

```cypher
MATCH (w:Word)
RETURN w.word AS word, COUNT { (w)-[:ONE_LETTER_DIFFERENT]-() } AS neighbours
ORDER BY neighbours DESC, word
LIMIT 5;
```

The statement returns the following results:

| word | neighbours |
|---|---|
| care | 43 |
| cone | 41 |
| mare | 41 |
| bare | 40 |
| hare | 40 |

`care` connects to 43 words, from `bare` and `cure` to `cark` and `yare`. Patterns like `_are`, where many consonants fit, produce the busiest words.

At the other end, 91 words have no neighbours at all, including `adze`, `ankh` and `awol`. No puzzle can start or finish on them:

```cypher
MATCH (w:Word)
WHERE COUNT { (w)-[:ONE_LETTER_DIFFERENT]-() } = 0
RETURN count(w) AS isolated;
```

## How connected is the language?

Isolated words raise a bigger question: can the remaining words all reach each other? The [GDS (Graph Data Science)](https://neo4j.com/docs/graph-data-science/current/introduction/) [Weakly Connected Components](https://neo4j.com/docs/graph-data-science/current/algorithms/wcc/) algorithm groups nodes that can reach one another:

```cypher
CALL gds.graph.project(
  'words',
  'Word',
  {ONE_LETTER_DIFFERENT: {orientation: 'UNDIRECTED'}}
);

CALL gds.wcc.stream('words')
YIELD componentId
WITH componentId, count(*) AS size
RETURN size, count(*) AS components
ORDER BY size DESC;

CALL gds.graph.drop('words');
```

The statement returns the following results:

| size | components |
|---|---|
| 7081 | 1 |
| 5 | 1 |
| 3 | 1 |
| 2 | 3 |
| 1 | 91 |

7,081 words, 98.5% of the list, sit in one giant component. Pick any two of them and a solution exists. The rest form small islands. `oryx`, `onyx`, `eryx`, `onym` and `pnyx` only connect to each other.

> **[Get started with Graph Data Science](https://graphacademy.neo4j.com/courses/gds-fundamentals/)**

## Try it yourself

You can build the entire four-letter word graph yourself using the Cypher statements provided above.

Create a free AuraDB instance and build the graph yourself.

[Create a free AuraDB instance](https://console.neo4j.io?attribution=graphacademy)

Try your own puzzles by changing the words in the `SHORTEST` query or look for the pair of words with the longest ladder.

---

*Originally published on [Neo4j GraphAcademy](https://graphacademy.neo4j.com/blog/four-letter-word-graph) on 9 October 2026.*
