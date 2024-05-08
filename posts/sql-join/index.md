# SQL Join


# Join?

JOIN은 데이터베이스 내의 여러 테이블에서 가져온 레코드를 조합하여 하나의 테이블이나 결과 집합으로 표현해 주는 것이다.

- Inner join: 교집합

- Left / Right join: 부분 집합

- Outer Join: 합집합

<img src="/images/SQL/sql-1.png"/>

예시 데이터

| ID  | ENAME |
| :-: | :---: |
|  1  |  AAA  |
|  2  |  BBB  |
|  3  |  CCC  |

| ID  | KNAME |
| :-: | :---: |
|  1  |  가   |
|  2  |  나   |
|  4  |  라   |
|  5  |  마   |

## Inner Join

조인하는 테이블의 ON 절의 조건일 일치하는 결과만 출력

<img src="/images/SQL/sql-2.png"/>

```sql
select u.userid, name
from usertbl as u inner join buytbl as b
on u.userid=b.userid
where u.userid="111" -- join을 완료하고 그다음 조건을 따진다.
```

```sql
SELECT A.ID, A.ENAME, A.KNAME
FROM A INNER JOIN B
ON A.ID = B.ID
```

| ID  | ENAME | KNAME |
| :-: | :---: | :---: |
|  1  |  AAA  |  가   |
|  2  |  BBB  |  나   |

## Left / Right Outer Join

두 테이블이 합쳐 질때 왼쪽/오른쪽을 기준으로 했느냐에 따라 기준 테이블의 것은 모두 출력되어야 한다고 이해하면 된다.

OUTER JOIN은 조인하는 테이블의 ON 절의 조건 중 한쪽의 데이터를 모두 가져온다

OUTER JOIN은 LEFT OUTER JOIN, RIGHT OUTER JOIN, FULL OUTER JOIN 이렇게 3가지가 있다.

LEFT OUTER JOIN을 거의 대부분 사용하여, FULL OUTER JOIN은 성능상 거의 사용하지 않는다.

### Left Outer Join

<img src="/images/SQL/sql-3.png"/>

LEFT JOIN은 두 테이블이 있을 경우, 첫 번째 테이블을 기준으로 두 번째 테이블을 조합하는 JOIN이다.

```sql
-- 예) 1학년 학생의 이름과 지도교수명을 출력하라.
-- 단, 지도교수가 지정되지 않은 학생도 출력되게 하라.

SELECT STUDENT.NAME, PROFESSOR.NAME
FROM STUDENT LEFT OUTER JOIN PROFESSOR -- STUDENT를 기준으로 왼쪽 조인
ON STUDENT.PID = PROFESSOR.ID
WHERE GRADE = 1
```

```sql
SELECT A.ID, A.ENAME, A.KNAME
FROM A LEFT OUTER JOIN B
ON A.ID = B.ID
```

| ID  | ENAME | KNAME |
| :-: | :---: | :---: |
|  1  |  AAA  |  가   |
|  2  |  BBB  |  나   |
|  3  |  CCC  | NULL  |

### Right Outer Join

<img src="/images/SQL/sql-4.png"/>

RIGHT JOIN은 두 테이블이 있을 경우, 두 번째 테이블을 기준으로 첫 번째 테이블을 조합하는 JOIN이다.

```sql
-- 예) 1학년 학생의 이름과 지도교수명을 출력하라.
-- 단, 지도교수가 지정되지 않은 학생도 출력되게 하라.

SELECT STUDENT.NAME, PROFESSOR.NAME
FROM STUDENT RIGHT OUTER JOIN PROFESSOR -- PROFESSOR를 기준으로 오른쪽 조인
ON STUDENT.PID = PROFESSOR.ID
WHERE GRADE = 1
```

```sql
SELECT A.ID, A.ENAME, A.KNAME
FROM A RIGHT OUTER JOIN B
ON A.ID = B.ID
```

| ID  | ENAME | KNAME |
| :-: | :---: | :---: |
|  1  |  AAA  |  가   |
|  2  |  BBB  |  나   |
|  4  | NULL  |  라   |
|  5  | NULL  |  마   |

## Exclusive Left / Right Join

<table>
    <tr>
        <td><img src="/images/SQL/sql-5.png"/></td>
        <td><img src="/images/SQL/sql-6.png"/></td>
    </tr>
</table>

### Exclusive Left Join

어느 특정 테이블에 있는 레코드만 가져오는 것

​EXCLUSIVE JOIN는 만약 테이블 두개를 JOIN한다면 둘중 한가지 테이블에만 있는 데이터를 가져온다.

다른 JOIN들과는 다르게 별도의 EXCLUSIVE JOIN함수가 있는 것은 아니고 기존의 LEFT JOIN과 Where절의 조건을 함께 사용하여 만드는 JOIN 문법이다.

```sql
-- 조인한 B 테이블의 값이 null만 출력하라는 말은,
-- 조인이 안된 A 레코드 나머지값만 출력하라는 말

SELECT *
FROM table1 A LEFT JOIN table2 B
ON A.ID_SEQ = B.ID_SEQ
WHERE B.ID_SEQ IS NULL
```

```sql
SELECT A.ID, A.ENAME, A.KNAME
FROM A LEFT OUTER JOIN B
ON A.ID = B.ID
WHERE B.ID IS NULL
```

| ID  | ENAME | KNAME |
| :-: | :---: | :---: |
|  3  |  CCC  | NULL  |

### Exclusive Right Join

어느 특정 테이블에 있는 레코드만 가져오는 것

​EXCLUSIVE JOIN는 만약 테이블 두개를 JOIN한다면 둘중 한가지 테이블에만 있는 데이터를 가져온다.

다른 JOIN들과는 다르게 별도의 EXCLUSIVE JOIN함수가 있는 것은 아니고 기존의 RIGHT JOIN과 Where절의 조건을 함께 사용하여 만드는 JOIN 문법이다.

```sql
-- 조인한 A 테이블의 값이 null만 출력하라는 말은,
-- 조인이 안된 B 레코드 나머지값만 출력하라는 말

SELECT *
FROM table1 A RIGHT JOIN table2 B
ON A.ID_SEQ = B.ID_SEQ
WHERE A.ID_SEQ IS NULL
```

```sql
SELECT A.ID, A.ENAME, A.KNAME
FROM A RIGHT OUTER JOIN B
ON A.ID = B.ID
WHERE A.ID IS NULL
```

| ID  | ENAME | KNAME |
| :-: | :---: | :---: |
|  4  | NULL  |  라   |
|  5  | NULL  |  마   |

## Self Join

<img src="/images/SQL/sql-7.png"/>

```sql
-- 예) 모든 사원에 대해 사원의 이름과 직속 상사의 이름을 검색 해라.
-- EMPNAME 테이블에 어떤 사원의 MANAGER 번호가 같은
-- 테이블 내에서 어떤 사원의 EMPNO와 같으면 그 사원이 직속 상관

SELECT E.EMPNAME as 사원, M.EMPNAME as 직속상관
FROM EMPLOYEE E, EMPLOYEE M -- inner join
WHERE E.MANAGER = M.EMPNO;
```

## Union

UNION은 여러 개의 SELECT 문의 결과를 하나의 테이블이나 결과 집합으로 표현할 때 사용

이때 각각의 SELECT 문으로 선택된 필드의 개수와 타입은 모두 같아야 하며, 필드의 순서 또한 같아야 한다.

기본 집합 쿼리에는 (DISTINCT) 중복제거가 자동 포함되어있다.

```sql
SELECT 필드이름 FROM 테이블이름
UNION
SELECT 필드이름 FROM 테이블이름
```

## Union All

UNION은 DISTINCT 자동 포함이라 중복되는 레코드를 제거한다.

따라서 중복되는 레코드까지 모두 출력하고 싶다면, ALL 키워드를 사용하면 된다.

```sql
SELECT 필드이름 FROM 테이블이름
UNION ALL
SELECT 필드이름 FROM 테이블이름
```

