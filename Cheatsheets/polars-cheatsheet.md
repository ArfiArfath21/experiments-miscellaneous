# Comprehensive Polars Cheatsheet

## Table of Contents
- [Installation](#installation)
- [Basic Operations](#basic-operations)
- [Data Types](#data-types)
- [Creating DataFrames and Series](#creating-dataframes-and-series)
- [Data Inspection](#data-inspection)
- [Selection and Indexing](#selection-and-indexing)
- [Filtering Data](#filtering-data)
- [Sorting](#sorting)
- [Missing Values](#missing-values)
- [String Operations](#string-operations)
- [Datetime Operations](#datetime-operations)
- [Aggregations](#aggregations)
- [Groupby Operations](#groupby-operations)
- [Joins and Merges](#joins-and-merges)
- [Reshaping Data](#reshaping-data)
- [Apply and Map](#apply-and-map)
- [IO Operations](#io-operations)
- [Lazy Execution](#lazy-execution)
- [Schema Manipulation](#schema-manipulation)
- [Memory Management](#memory-management)
- [Window Functions](#window-functions)
- [Expressions](#expressions)
- [Optimizations](#optimizations)
- [Conversion to/from Pandas](#conversion-tofrom-pandas)

## Installation

```python
# Install Polars
pip install polars

# Install with all optional dependencies
pip install polars[all]

# Import
import polars as pl
```

## Basic Operations

```python
# Create a simple DataFrame
df = pl.DataFrame({
    "A": [1, 2, 3, 4, 5],
    "B": ["a", "b", "c", "d", "e"],
    "C": [1.1, 2.2, 3.3, 4.4, 5.5]
})

# Basic operations
df.head(2)     # First 2 rows
df.tail(2)     # Last 2 rows
df.shape       # (5, 3) - Rows and columns
df.columns     # ["A", "B", "C"]
df.dtypes      # [Int64, Utf8, Float64]
df.schema      # Schema: {A: Int64, B: Utf8, C: Float64}
df.describe()  # Statistical summary
```

## Data Types

```python
# Polars Data Types

# Boolean
pl.Boolean

# Integers
pl.Int8        # 8-bit signed integer
pl.Int16       # 16-bit signed integer
pl.Int32       # 32-bit signed integer
pl.Int64       # 64-bit signed integer
pl.UInt8       # 8-bit unsigned integer
pl.UInt16      # 16-bit unsigned integer
pl.UInt32      # 32-bit unsigned integer
pl.UInt64      # 64-bit unsigned integer

# Floating point
pl.Float32     # 32-bit floating point
pl.Float64     # 64-bit floating point

# Decimal (fixed-point)
pl.Decimal     # Arbitrary precision fixed-point

# String
pl.Utf8        # UTF-8 encoded string

# Binary
pl.Binary      # Binary data

# Date and Time
pl.Date        # Calendar date (year, month, day)
pl.Time        # Time of day (hour, minute, second, nanosecond)
pl.Datetime    # Combined date and time with timezone option
pl.Duration    # Time duration

# Complex nested types
pl.List        # List of values
pl.Struct      # Struct of named values
pl.Enum        # Enumerated type
pl.Object      # Python object type
pl.Categorical # Categorical data with dictionary encoding

# Null type
pl.Null        # Represents null values
```

### Creating and Checking Data Types

```python
# Specifying data types when creating a DataFrame
df = pl.DataFrame({
    "a": [1, 2, 3],
    "b": [1.1, 2.2, 3.3]
}, schema={
    "a": pl.Int32,
    "b": pl.Float32
})

# Check types
df.dtypes     # Returns list of types
df.schema     # Returns dictionary mapping column names to types

# Create a Series with specific type
s = pl.Series("x", [1, 2, 3], dtype=pl.Int8)

# Cast types
df.with_columns([
    pl.col("a").cast(pl.Float64),
    pl.col("b").cast(pl.Int32)
])

# Infer schema from data
df = pl.DataFrame({
    "a": [1, 2, 3],
    "b": ["a", "b", "c"]
})
# Auto-detects Int64 for 'a' and Utf8 for 'b'
```

### Special Type Operations

```python
# Date operations
df = pl.DataFrame({
    "date": ["2021-01-01", "2021-01-02"],
}).with_columns([
    pl.col("date").str.to_date().alias("date_typed")
])

# List type
df = pl.DataFrame({
    "list_col": [[1, 2], [3, 4]]
})
df.with_columns([
    pl.col("list_col").arr.first().alias("first_item"),
    pl.col("list_col").arr.lengths().alias("list_length")
])

# Struct type
df = pl.DataFrame({
    "struct_col": [{"a": 1, "b": "x"}, {"a": 2, "b": "y"}]
})
df.with_columns([
    pl.col("struct_col").struct.field("a").alias("a_field")
])

# Categorical type (for memory efficiency)
df = pl.DataFrame({
    "cat_col": ["a", "b", "a", "a", "b", "c"]
}).with_columns([
    pl.col("cat_col").cast(pl.Categorical).alias("cat_col_typed")
])

# Binary type
df = pl.DataFrame({
    "bin_col": [b"hello", b"world"]
})

# Object type (use with caution)
import numpy as np
df = pl.DataFrame({
    "obj_col": [np.array([1, 2]), np.array([3, 4])]
})
```

### When to Use Different Types

```python
# Integer types
# - Use Int8/Int16 for small ranges to save memory
# - Use Int64 for large numbers or when in doubt
# - Use UInt types when you know values are non-negative

# Float types
# - Use Float32 to save memory when precision isn't critical
# - Use Float64 for scientific calculations requiring precision
# - Use Decimal for financial calculations

# String types
# - Use Utf8 for all string data (only option)

# Date/Time types
# - Use Date for date only
# - Use Datetime for timestamp data
# - Use Time for time-of-day only
# - Use Duration for time intervals

# Nested types
# - Use List for array-like one-to-many relationships
# - Use Struct for record-like data with different types
# - Use Categorical for repeated string values (high cardinality)
```

## Creating DataFrames and Series

```python
# From dictionaries
df1 = pl.DataFrame({
    "A": [1, 2, 3],
    "B": ["a", "b", "c"]
})

# From lists
df2 = pl.DataFrame([
    {"A": 1, "B": "a"},
    {"A": 2, "B": "b"},
    {"A": 3, "B": "c"}
])

# From a list of tuples with column names
df3 = pl.DataFrame(
    [(1, "a"), (2, "b"), (3, "c")],
    schema=["A", "B"]
)

# Create a Series
s1 = pl.Series("X", [1, 2, 3, 4])
s2 = pl.Series(name="Y", values=[5, 6, 7, 8])

# Create DataFrame from Series
df4 = pl.DataFrame([s1, s2])

# Create empty DataFrame with schema
df5 = pl.DataFrame(schema={
    "A": pl.Int64,
    "B": pl.Utf8,
    "C": pl.Float64
})

# Range
df6 = pl.DataFrame({"A": pl.arange(0, 5, 1)})

# Create using named expressions
df7 = pl.DataFrame([
    pl.col("A").sum(),
    pl.col("B").mean()
])
```

## Data Inspection

```python
# Examine the data
df.head()                   # Default first 5 rows
df.tail()                   # Default last 5 rows
df.sample(n=3)              # Random sample of 3 rows
df.sample(frac=0.25)        # Random 25% of rows

# Information about DataFrame
df.shape                    # Tuple of (rows, columns)
df.columns                  # List of column names
df.dtypes                   # List of data types
df.schema                   # Schema with column names and types
df.describe()               # Statistical summary
df.null_count()             # Count of null values per column

# Memory usage
df.estimated_size()         # Size in bytes
df.flags                    # Flags related to memory

# Understanding data
df["A"].value_counts()      # Frequency of values in column A
df["A"].is_unique()         # Check if all values are unique
df["A"].is_sorted()         # Check if column is sorted
```

## Selection and Indexing

```python
# Select columns by name
df.select("A")              # Select a single column
df.select(["A", "B"])       # Select multiple columns
df["A"]                     # Select a column (returns Series)
df[["A", "B"]]              # Select multiple columns (returns DataFrame)

# Using expressions
df.select(pl.col("A"))
df.select(pl.col("A"), pl.col("B"))
df.select(pl.all())         # Select all columns
df.select(pl.all().exclude("C"))  # Select all except "C"

# Select with transformation
df.select(pl.col("A") * 2)
df.select((pl.col("A") * 2).alias("A_doubled"))

# Select by position
df.select(pl.col("^.*$").first())   # First column
df.select(pl.col("^.*$").last())    # Last column

# Slice rows
df.slice(0, 2)              # Rows 0 and 1
df.slice(2, 3)              # Rows 2, 3, and 4

# Row-based indexing (Polars uses 0-based indexing)
df.row(0)                   # First row as Python tuple
df.rows()                   # Iterator over rows as tuples
df.rows_by_key(column="A")  # Dictionary with keys from column A
```

## Filtering Data

```python
# Basic filtering
df.filter(pl.col("A") > 2)
df.filter(pl.col("B") == "a")

# Multiple conditions
df.filter((pl.col("A") > 2) & (pl.col("C") < 5))  # AND
df.filter((pl.col("A") > 2) | (pl.col("B") == "a"))  # OR

# Negation
df.filter(~(pl.col("A") > 2))

# Filter on multiple values
df.filter(pl.col("A").is_in([1, 3, 5]))
df.filter(~pl.col("A").is_in([1, 3, 5]))

# String filters
df.filter(pl.col("B").str.contains("a"))
df.filter(pl.col("B").str.starts_with("a"))
df.filter(pl.col("B").str.ends_with("e"))

# Null value filters
df.filter(pl.col("A").is_null())
df.filter(pl.col("A").is_not_null())

# Complex filters
df.filter(
    (pl.col("A") > pl.col("A").mean()) &
    (pl.col("C").is_not_null())
)
```

## Sorting

```python
# Sort by a single column
df.sort("A")                 # Ascending by default
df.sort("A", descending=True)

# Sort by multiple columns
df.sort(["A", "B"])
df.sort(["A", "B"], descending=[True, False])  # A descending, B ascending

# Using expressions
df.sort(pl.col("A").abs())   # Sort by absolute value
df.sort(pl.col("A").rank())  # Sort by rank

# Nulls handling
df.sort("A", nulls_last=True)  # Null values at the end
```

## Missing Values

```python
# Checking for nulls
df.null_count()              # Nulls per column
df.select(pl.col("A").is_null().sum())  # Count nulls in column A
df.select(pl.col("A").is_not_null().sum())  # Count non-nulls in column A

# Filling nulls
df.fill_null(0)              # Fill all nulls with 0
df.fill_null(strategy="mean")  # Fill with mean
df.fill_null(strategy="forward")  # Forward fill
df.fill_null(strategy="backward")  # Backward fill

# Column specific
df.with_columns(
    pl.col("A").fill_null(0),
    pl.col("B").fill_null("missing")
)

# Drop nulls
df.drop_nulls()              # Drop rows with any null
df.drop_nulls(subset=["A"])  # Drop rows where column A is null

# Replace with nulls
df.with_columns(
    pl.when(pl.col("A") < 0).then(None).otherwise(pl.col("A")).alias("A")
)
```

## String Operations

```python
# String methods
df.select(pl.col("B").str.to_uppercase())
df.select(pl.col("B").str.to_lowercase())
df.select(pl.col("B").str.strip())
df.select(pl.col("B").str.strip_chars("ae"))  # Strip 'a' or 'e'
df.select(pl.col("B").str.replace("a", "z"))

# String matching
df.filter(pl.col("B").str.contains("a"))
df.filter(pl.col("B").str.starts_with("a"))
df.filter(pl.col("B").str.ends_with("e"))
df.select(pl.col("B").str.lengths().alias("str_lengths"))

# Regex
df.select(pl.col("B").str.extract(r"(\w+)", group_index=0))
df.select(pl.col("B").str.extract_all(r"(\w)"))  # Returns list
df.filter(pl.col("B").str.contains(r"[a-c]"))

# Concatenation
df.select(
    pl.concat_str([pl.col("A").cast(pl.Utf8), pl.col("B")], separator="-").alias("A_B")
)
```

## Datetime Operations

```python
# Create datetime column
df = pl.DataFrame({
    "date_str": ["2022-01-01", "2022-01-02", "2022-01-03"]
})

# Parse dates
df = df.with_columns(
    pl.col("date_str").str.to_date().alias("date"),
    pl.col("date_str").str.to_datetime().alias("datetime")
)

# Datetime components
df = df.with_columns([
    pl.col("date").dt.year().alias("year"),
    pl.col("date").dt.month().alias("month"),
    pl.col("date").dt.day().alias("day"),
    pl.col("datetime").dt.hour().alias("hour"),
    pl.col("datetime").dt.weekday().alias("weekday")
])

# Date arithmetic
df = df.with_columns([
    pl.col("date").dt.offset_by("1d").alias("tomorrow"),
    pl.col("date").dt.offset_by("-1d").alias("yesterday")
])

# Timedeltas
df = df.with_columns([
    (pl.col("tomorrow") - pl.col("date")).alias("delta_days")
])

# Date ranges
dates = pl.date_range(
    low=pl.Date(2022, 1, 1),
    high=pl.Date(2022, 1, 5),
    interval="1d"
)
```

## Aggregations

```python
# Basic aggregations
df.select(pl.col("A").sum())
df.select(pl.col("A").mean())
df.select(pl.col("A").median())
df.select(pl.col("A").min())
df.select(pl.col("A").max())
df.select(pl.col("A").std())
df.select(pl.col("A").var())
df.select(pl.col("A").count())

# Multiple aggregations
df.select([
    pl.col("A").sum().alias("sum_A"),
    pl.col("A").mean().alias("mean_A"),
    pl.col("C").min().alias("min_C"),
    pl.col("C").max().alias("max_C")
])

# Quantiles
df.select(pl.col("A").quantile(0.5))  # Median (50th percentile)
df.select(pl.col("A").quantile([0.25, 0.5, 0.75]))  # Multiple quantiles

# Custom aggregations
df.select(
    ((pl.col("A").max() - pl.col("A").min()) / pl.col("A").count()).alias("range_per_count")
)
```

## Groupby Operations

```python
# Basic groupby
df.group_by("B").agg(
    pl.col("A").sum().alias("sum_A"),
    pl.col("A").mean().alias("mean_A"),
    pl.col("C").count().alias("count_C")
)

# Multiple groupby columns
df.group_by(["B", "D"]).agg(
    pl.col("A").sum(),
    pl.col("C").mean()
)

# Groupby with filter
df.group_by("B").agg(
    pl.col("A").filter(pl.col("A") > 2).sum()
)

# First/last values per group
df.group_by("B").agg([
    pl.col("A").first().alias("first_A"),
    pl.col("A").last().alias("last_A")
])

# Group by time periods
df.group_by(pl.col("date").dt.year()).agg(
    pl.col("A").sum()
)

# Count by group
df.group_by("B").count()

# Apply over groups
df.group_by("B").agg([
    pl.col("A").apply(lambda x: x.max() - x.min())
])
```

## Joins and Merges

```python
df1 = pl.DataFrame({
    "key": ["A", "B", "C"],
    "val1": [1, 2, 3]
})

df2 = pl.DataFrame({
    "key": ["A", "B", "D"],
    "val2": [10, 20, 30]
})

# Inner join (default)
df1.join(df2, on="key")

# Left join
df1.join(df2, on="key", how="left")

# Right join
df1.join(df2, on="key", how="right")

# Outer join
df1.join(df2, on="key", how="outer")

# Cross join
df1.join(df2, how="cross")

# Join on multiple columns
# For example if both DFs had 'key1' and 'key2'
# df1.join(df2, on=["key1", "key2"])

# Join with different column names
df1.join(df2, left_on="key", right_on="other_key")

# Join with expressions
df1.join(
    df2,
    on="key",
    how="inner"
).with_columns([
    (pl.col("val1") + pl.col("val2")).alias("sum_vals")
])

# Suffixes for duplicate columns
df1.join(
    df2,
    on="key",
    suffix="_right"  # Adds "_right" to columns from right DataFrame
)
```

## Reshaping Data

```python
# Melt (wide to long)
df.melt(
    id_vars=["id_column"],     # Columns to keep as is
    value_vars=["A", "B", "C"],  # Columns to unpivot
    variable_name="variable",  # Name for the column with original column names
    value_name="value"         # Name for the column with values
)

# Pivot (long to wide)
df.pivot(
    index="id_column",         # Column(s) to make into new index
    columns="variable",        # Column whose values become new columns
    values="value"             # Column with values to fill table
)

# Stack/unstack helper using melt
def stack(df, id_vars, value_vars):
    return df.melt(
        id_vars=id_vars,
        value_vars=value_vars
    )

# Stack/unstack helper using pivot
def unstack(df, index, columns, values):
    return df.pivot(
        index=index,
        columns=columns,
        values=values
    )

# Explode a list column into multiple rows
df = pl.DataFrame({
    "A": [1, 2],
    "B": [[1, 2], [3, 4]]
})
df.explode("B")  # Creates 4 rows
```

## Apply and Map

```python
# Apply a function to a column
df.with_columns(
    pl.col("A").apply(lambda x: x * 2).alias("A_doubled")
)

# Apply a function row-wise
df.select([
    pl.struct(["A", "C"]).apply(lambda x: x["A"] + x["C"]).alias("A_plus_C")
])

# Apply using expressions (preferred for performance)
df.with_columns(
    (pl.col("A") * 2).alias("A_doubled"),
    (pl.col("A") + pl.col("C")).alias("A_plus_C")
)

# Map values
mapping = {1: "one", 2: "two", 3: "three"}
df.with_columns(
    pl.col("A").map_dict(mapping).alias("A_mapped")
)

# Running/rolling aggregations
df.with_columns([
    pl.col("A").cum_sum().alias("A_cumsum"),
    pl.col("A").cum_min().alias("A_cummin"),
    pl.col("A").cum_max().alias("A_cummax")
])
```

## IO Operations

```python
# CSV
# Write to CSV
df.write_csv("data.csv")
# Read from CSV
df = pl.read_csv("data.csv")
# Read with options
df = pl.read_csv(
    "data.csv",
    sep=",",
    has_header=True,
    skip_rows=1,
    columns=["A", "B"],
    dtypes={"A": pl.Int64, "B": pl.Utf8},
    null_values=["NA", "NULL"]
)

# Parquet
# Write to Parquet
df.write_parquet("data.parquet")
# Read from Parquet
df = pl.read_parquet("data.parquet")
# Read with options
df = pl.read_parquet(
    "data.parquet",
    columns=["A", "B"],
    n_rows=100  # Limit rows
)

# JSON
# Write to JSON
df.write_json("data.json")
# Read from JSON
df = pl.read_json("data.json")

# Database (SQLite example)
import sqlite3
conn = sqlite3.connect("database.db")

# Write to SQL
df.write_database(
    table_name="my_table",
    connection=conn,
    if_exists="replace"  # or "append"
)

# Read from SQL
df = pl.read_database(
    query="SELECT * FROM my_table",
    connection=conn
)

# Excel
# Using pyarrow integration
df.write_excel("data.xlsx")  # Requires openpyxl
df = pl.read_excel("data.xlsx")
```

## Lazy Execution

```python
# Create a lazy DataFrame
ldf = pl.scan_csv("data.csv")
# or from an eager DataFrame
ldf = df.lazy()

# Build a query
result = (
    ldf
    .filter(pl.col("A") > 2)
    .group_by("B")
    .agg([
        pl.col("A").sum().alias("sum_A"),
        pl.col("C").mean().alias("mean_C")
    ])
    .sort("sum_A", descending=True)
)

# Execute the query
final_df = result.collect()

# Optimization
result = result.optimization_toggle(
    projection_pushdown=True,
    predicate_pushdown=True,
    type_coercion=True,
    simplify_expression=True
)

# Profile the query execution
final_df, profiling = result.profile()
print(profiling)
```

## Schema Manipulation

```python
# Rename columns
df.rename({"A": "newA", "B": "newB"})

# Rename with a function
df.rename(lambda col: col.lower())

# Add / modify columns
df.with_columns([
    pl.lit(5).alias("constant_col"),
    (pl.col("A") * 2).alias("A_doubled")
])

# Drop columns
df.drop(["A", "B"])
df.drop(columns=["A", "B"])  # Alternative syntax

# Select all except some columns
df.select(pl.all().exclude(["A", "B"]))

# Change data types
df.with_columns([
    pl.col("A").cast(pl.Float64),
    pl.col("B").cast(pl.Int32)
])

# Automatic type inference
df = pl.read_csv("data.csv", infer_schema_length=100000)
```

## Memory Management

```python
# Get memory usage
df.estimated_size()

# Clone a DataFrame
df_copy = df.clone()

# Using views when possible (no data copied)
subset = df.select(["A", "B"])

# Free unused memory
import gc
gc.collect()

# Using streaming mode for large datasets
for chunk in pl.read_csv_batched("large_file.csv", batch_size=10000):
    # Process each chunk
    process(chunk)
```

## Window Functions

```python
# Ranking
df.with_columns([
    pl.col("A").rank().alias("rank_A"),
    pl.col("A").rank(method="dense").alias("dense_rank_A"),
    pl.col("A").rank(method="percent").alias("percent_rank_A")
])

# Rolling/moving aggregations
df.with_columns([
    pl.col("A").rolling_mean(window_size=3).alias("A_rolling_mean"),
    pl.col("A").rolling_sum(window_size=3).alias("A_rolling_sum"),
    pl.col("A").rolling_min(window_size=3).alias("A_rolling_min"),
    pl.col("A").rolling_max(window_size=3).alias("A_rolling_max")
])

# Over partitions
df.with_columns([
    pl.col("A").mean().over("B").alias("A_mean_by_B"),
    pl.col("A").sum().over("B").alias("A_sum_by_B"),
    pl.col("A").count().over("B").alias("A_count_by_B")
])

# With sorting
df.with_columns([
    pl.col("A")
      .cum_sum()
      .over("B")
      .sort("C")
      .alias("A_cumsum_by_B_sorted")
])

# Multiple partitions and ordering
df.with_columns([
    pl.col("A")
      .mean()
      .over(["B", "D"])
      .sort(["C", "E"])
      .alias("A_mean_by_BD_sorted")
])
```

## Expressions

```python
# Literals
pl.lit(5)
pl.lit("hello")
pl.lit(True)

# Column references
pl.col("A")
pl.col("*")  # All columns
pl.col("^A.*$")  # Regex pattern

# Selection shortcuts
pl.all()  # All columns
pl.first()  # First column
pl.last()  # Last column
pl.exclude("A")  # All except column A

# Conditional expressions
pl.when(pl.col("A") > 2).then(1).otherwise(0)

# Complex conditions
(
    pl.when(pl.col("A") > 3)
    .then("high")
    .when(pl.col("A") > 1)
    .then("medium")
    .otherwise("low")
)

# String concatenation
pl.concat_str([pl.col("A").cast(pl.Utf8), pl.col("B")], separator="-")

# Struct creation
pl.struct(["A", "B"]).alias("AB_struct")

# List manipulation
pl.col("list_col").arr.first()  # First element
pl.col("list_col").arr.last()   # Last element
pl.col("list_col").arr.get(1)   # Element at index 1
pl.col("list_col").arr.lengths()  # Length of each list

# Combining expressions
(pl.col("A") + pl.col("C")).pow(2) - pl.col("A").mean()
```

## Optimizations

```python
# Use lazy evaluation for optimization
ldf = df.lazy()

# Avoid multiple collection points
# Bad:
df1 = ldf.filter(pl.col("A") > 2).collect()
df2 = df1.group_by("B").agg(pl.col("A").sum()).collect()

# Good:
df = (
    ldf
    .filter(pl.col("A") > 2)
    .group_by("B")
    .agg(pl.col("A").sum())
    .collect()
)

# Use expressions over apply where possible
# Bad:
df.with_columns(
    pl.col("A").apply(lambda x: x * 2).alias("A_doubled")
)

# Good:
df.with_columns(
    (pl.col("A") * 2).alias("A_doubled")
)

# Predicate pushdown (happens automatically in lazy mode)
# This will push filters down to the data source:
result = (
    pl.scan_csv("large_file.csv")
    .filter(pl.col("A") > 100)
    .select(["A", "B"])
    .collect()
)

# Memory usage: only select what you need
result = (
    pl.scan_csv("large_file.csv")
    .select(["A", "B"])  # Only select needed columns
    .filter(pl.col("A") > 100)
    .collect()
)

# Project early (select only needed columns)
# Bad:
df.filter(pl.col("A") > 0).select(["B", "C"])

# Good:
df.select(["A", "B", "C"]).filter(pl.col("A") > 0).select(["B", "C"])
```

## Conversion to/from Pandas

```python
# From Pandas
import pandas as pd
pandas_df = pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]})
polars_df = pl.from_pandas(pandas_df)

# To Pandas
pandas_df = polars_df.to_pandas()

# Convert Pandas types to Polars types
pl.from_pandas(pandas_df, schema_overrides={"A": pl.Int32})

# Fast conversion (with pyarrow)
polars_df = pl.from_arrow(pandas_df.to_arrow())
pandas_df = polars_df.to_arrow().to_pandas()
```

## Bonus: Common Patterns

```python
# Counting unique values
df.select(pl.col("B").n_unique())
df.group_by("B").agg(pl.count())

# Getting top N per group
(
    df.group_by("B")
    .agg([
        pl.col("A").sort().limit(3)  # Top 3 smallest values
    ])
)

# Adding row numbers
df.with_row_count("row_nr")

# Working with duplicates
df.unique()  # Keep only unique rows
df.unique(subset=["A", "B"])  # Unique based on subset of columns
df.select(pl.col("A").is_duplicated())  # Mark duplicates
df.filter(~pl.col("A").is_duplicated())  # Keep only first occurrence

# Fixed-width text
df.select(pl.col("B").str.pad_end(10, " "))
df.select(pl.col("B").str.pad_start(10, "0"))

# Column data profiling
df.select([
    pl.col("A").mean().alias("mean"),
    pl.col("A").std().alias("std"),
    pl.col("A").min().alias("min"),
    pl.col("A").max().alias("max"),
    pl.col("A").n_unique().alias("n_unique"),
    pl.col("A").is_null().sum().alias("n_null")
])
```