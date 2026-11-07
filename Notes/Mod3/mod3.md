# MapReduce

- MapReduce is a framework for processing huge amount of data in parallel on large clusters of commodity hardware in reliable manner.
- A MapReduce program consists of two major tasks:
  - Map
  - Reduce

## The Map task

- The **map tas**k reads the input and produces a set of **key value pairs**.
- The map function is **provided by the programmer**.
- The generally form is: `map(keym value) -> key-value pairs`
- The Map task extracts the information required from the input data.
- MapReduce processes data through **sequential reads** of the input data.

### Example: Word Count

- **Problem:** Count how many times each distinct word of appears in a huge text document.
- The map function receives:
  - **Key:** document name
  - **Value:** text of the document.
- For everywhere `w` in the input value, the mapper produces: `emit(w, 1)`
- Example intermediate output:
  - `(crew, 1)`
  - `(space, 1)`
  - `(the, 1)`
  - `(shuttle, 1)`
- The Map task therefore converts the input document into multiple **key-value pairs**, where the **word is the key** and `1` is the value.

## Grouping by key

- **Grouping by Key** is the stage between **Map** and **Reduce** tasks.
- It collects all **key value pairs having the same key** and provides the grouped values to the reduce task.
- The grouping stage involves **shuffle and start**.

### Working

1. The Map task produces intermediary key-value pairs.
2. The system identifies pairs having the **same key**.
3. All values associated with the same key or **collected together**.
4. The grouped key and its list of values are passed to the **Reduced task**.

### Example: Word Count

Suppose Map task produce:

- `(crew, 1)`
- `(space, 1)`
- `(crew, 1)`
- `(the, 1)`
- `(crew, 1)`
- `(the, 1)`

After **grouping by key**:

- `crew → [1, 1, 1]`
- `space → [1]`
- `the → [1, 1]`

The reduce task can then process each key and its corresponding list of values.

## Reduce Task

- The **reduce task** is a second major processing stage of Map Reduce.
- It receives the **grouped key-value pairs** produced after the **group-by-key / shuffle and sort** stage.
- It's purpose is to aggregate, summarize, filter or transform the values associated with same key.

### Reduce Function

- General form: `reduce(key, values) → output`
- For each **key**, the reducer receives a list of all values associated with that key.
- It processes these values and produces the final output for that key.

### Example: Word Count

After grouping:

- `crew → [1, 1]`
- `space → [1]`
- `the → [1, 1, 1]`

The **Reduce task** adds the values for each key:

- `crew → 1 + 1 = 2`
- `space → 1 = 1`
- `the → 1 + 1 + 1 = 3`

Thus, the output is:

- `(crew, 2)`
- `(space, 1)`
- `(the, 3)`

### Reduce Algorithm

```python
reduce(key, values):
    result = 0
    for each value v in values:
        result += v
    emit(key, result)
```

- The **key** represents the item being processed.
- **values** contains all values associated with that key.
- The reducer combines these values and emits the resulting **key-value pair**.

### Example: Aggregation

For grouping and aggregation, each key represents a **group**.

- The reducer applies an **aggregation operator** to the list of values.
- Possible aggregation functions given in the material are:
  - **SUM**
  - **COUNT**
  - **AVG**
  - **MIN**
  - **MAX**

For example, with SUM:

`a → [b₁, b₂, ..., bₙ]`

becomes:

`a → b₁ + b₂ + ... + bₙ`

## Combiner

- A **Combiner** is used to **optimize MapReduce** by performing some processing locally at each **Mapper**.
- When an operation is **associative and commutative**, a **Combiner can be used in each Mapper** to optimize MapReduce.

### Purpose of a Combiner

- A Combiner performs a preliminary combination of intermediate results **before the data is passed to the Reduce task**.
- It helps reduce the amount of intermediate data that needs to be processed by the Reduce stage.

### Example: Projection

- In **Projection**, only selected attributes of each tuple are retained.
- Projection may cause the **same tuple to appear multiple times**.
- Therefore, the **Reduce function eliminates duplicates**.
- Since the operation is **associative and commutative**, a **Combiner** can be used at each Mapper to optimize the processing.

## Details of MapReduce Execution

- **MapReduce** distributes a task across multiple nodes.
- Each node processes the data stored on that node wherever possible.
- MapReduce provides:
  - **Automatic parallelization and distribution**
  - **Fault-tolerance**
  - **Status and monitoring tools**
  - A **clean abstraction for programmers**

### Execution Flow

The complete MapReduce processing sequence is:

**Sequentially read data** → **Map** → **Group by Key** → **Reduce** → **Write Result**

1. **Input**
   - Large amounts of data are read sequentially.
2. **Map Phase**
   - The **Mapper** reads the input and extracts the information of interest.
   - It produces **key-value pairs**.
3. **Group by Key**
   - Intermediate pairs are **collected according to their keys**.
   - This stage performs **shuffle and sort**.
4. **Reduce Phase**
   - The **Reducer** receives all values belonging to a key.
   - It **aggregates, summarizes, filters, or transforms** the data.
5. **Output**
   - The final result is written to the output.

### MapReduce Components
- A MapReduce program consists of three main portions:
  - **Driver Code** — runs on the client to configure and submit the job.
  - **Mapper**
  - **Reducer**
- The programmer mainly concentrates on implementing the **Map** and **Reduce** functions, while MapReduce handles the required processing and management.

## Coping with Node Failures

- **Fault-tolerance** is an important feature of MapReduce.
- MapReduce is designed to process huge amounts of data reliably on clusters containing many commodity machines.
- Large-scale data processing must handle:
  - **Fault/crash tolerance**
  - **Parallelization and distribution**
  - **I/O scheduling**
  - **Status and monitoring**

### Handling Node Failures

- MapReduce distributes a task across multiple nodes.
- Each node processes data stored on that node.
- The underlying **Distributed File System** provides **redundant storage** of large amounts of data.
- Files are **replicated** so that hardware failures can be handled.
- The system can **detect failures and recover from them**.

### Data Replication

- Files in the distributed file system are divided into **blocks**.
- Each block is **replicated on multiple DataNodes**.
- Replication provides protection against hardware failure.