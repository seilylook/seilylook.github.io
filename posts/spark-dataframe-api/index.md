# Spark DataFrame API


# DataFrame Transformations

## Selecting Columns

## Renaming Columns

## Change Columns data type

## Adding Columns to a DataFrame

## Removing Columns from a DataFrame

## Basics Arithmetic with DataFrame

## Apache Spark Architecture: DataFrame Immutability

## How to filter a DataFrame

## Apache Spark Architecture: Narrow Transformations

## Dropping Rows

## How to Drop rows and columns

## Handling NULL Values I - Null Functions

```python
Dfn = customerDf.selectExpr( \
    "salutation", \
    "firstname", \
    "lastname", \
    "email_address", \
    "year(birthdate) birthyear" \
)
```

| salutation | firstname | lastname | email_address        | birthyear |
| ---------- | --------- | -------- | -------------------- | --------- |
| null       | James     | null     | james@efsefa.org     | null      |
| null       | Adrian    | null     | null                 | null      |
| null       | Ruth      | null     | null                 | null      |
| null       | Christine | Jimenez  | Christine@adfacg.net | null      |

### Where 사용

```python
Dfn.where($"salutation".isNotNull) # Good
```

```python
Dfn.where($"salutation" === null) # Error
```

## Handling NULL Values II - DataFrameNaFunctions

### na 사용

```python
# 모든 Column 값이 NULL인 것 삭제.
Dfn.na.drop(how="all")

# 어떤 Columnd 이던 NULL 인 것 삭제.
Dfn.na.drop("any")

# firstname && lastname이 NULL인 것 삭제.
Dfn.na.drop("all", Seq("firstname", "lastname"))

# firstname || lastname이 NULL 인 것 삭제.
Dfn.na.drop("any", Seq("firstname", "lastname"))
```

### na & fill 사용

```python
# 모든 NULL 값에 abcdefg 채워준다.
# 주의할 점) Type이 일치해야 채워줄 수 있다.
# abcedfg(String) != birthyear(Datetime)이기에 그대로 NULL로 남아있다.
Dfn.na.fill("abcdefg")

# 특정 Column이 NULL 값일 때 특정 값을 채워줄 수 있다.
Dfn.na.fill(Map( \
    "salutation" -> "Unknown", \
    "firstname" -> "John", \
    "lastname" -> "Doe", \
    "bithyear" -> 9999 \
))
```

## Sort and Order Rows - Sort & OrderBy

```python
# NULL 값이 없는 데이터들을
# firstname을 오름차순 정렬
# month를 내림차순 정렬

# sort와 orderBy는 서로 연관이 없기 때문에
# 최종적으로는 firstname 정렬은 적용되지 않고 month만 적용된다.
customerDf \
.na.drop("any") \
.sort("firstname") == .sort(expr("firstname")) \
.orderBy(expr("month(birthdate)").desc)
.select("firstname", "lastname", "birthdate")

# firtname 오름차순 & lastname 내림차순으로 정렬하려면 다음과 같다.
customerDf \
.na.drop("any") \
.sort($"firstname", $"lastname".desc) \
.select("firstname", "lastname", "birthdate")
```

## Create Group of Rows: GroupBy

## DataFrame Statics

## Joining DataFrames - Inner Join

## Joining DataFrames - Right Outer Join

## Joining DataFrames - Left Outer Join

## Appending Rows to a DataFrame - Union

## Cashing a DataFrame

## DataFrameWriter I

## DataFrameWriter II - PartitionBy

## User Defined Functions

# Apache Spark Architecture: Execution

