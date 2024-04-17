# Big Data Research Note


# What is Big Data?

`Big data` is data whose scale, diversity, and complexity `require` new architecture, techniques, algorithms, and analytics to `manage` it and `extract value and hidden knowledge` from it.

`Big data` is refers to things one can do at a largee scale that cannot be done at a smaller one, to `extract new insights or create new forms` of value,

in ways that change markets, organizations, the relationship between citizens and governments, and more.

# 4V in Big Data

## Data Volume

44x increase from 2009 to 2020.

From 0.8 zettabytes to 35zb.

Data volume is increasing exponentially.

## Data Variety

Various formats, types, and structures Text, numericial, images, audio, video, sequences, time series, social media data, multi-dimensional arrays, etc... Static data vs streaming data.

## Data Velocity

Data is being generated fast and need to be processed fast(e.g., online data analytics)

Late desicion -> missing opportunities

### example

- e-promotions: your current location, your purchase history, what you like - send promotions right now for stores next to you.

- heathcare monitoring: sensors monitoring your activities and body - find any abnormal measurements that require immediate reaction.

## Data Veracity

This property means data quality or accuracy. It sometimes get referred to as validity or volatility referring to the lifetime of the data.

Data is of no value if it's not accurate, the results of big data analysis are only as good as the data being analyzed.

Veracity is very important for making big data operational.

# Big Data Field

- Smart Healthcare

- Mul-ti channel Sales

- Finance

- Log Analysis

- Homeland Security

- Traffic Control

- Telecom

- Search Quality

- Manufacturing

- Trading Anaysis

- Fraud and Risk

- Retail: Chum, NBO

# Big Data Processing Steps

## Acquisition 획득

- Transaction data

- Web data

- Social interaction data

- Mobile / Sensor data

- `Real time collection and update`

## Storage 저장

- Distributed file system

- Database

- Data warehouse

- `ETL and integration`

- `Data Security and privacy`

## Analysis 분석

- Data Mining

- Text analytics

- OLAP

- High-perfomanct BI

- Data visualization

- `New, integratice analysis`

## Access 접근

- Improved productivity

- Effective decision making

- Enhanced customner satisfaction

- Increased business competitiveness

- `Learning from feedback`

# Scheduler?

## What if a schedule's added with the market-index crawler?

In Linux there is a handy scheduling damon called `cron`.

The cron daemon is a long-running process that `executes commands at specific times`.

This is to `schedule` activites, either as `one-time` events or as `recurring` tasks.

## 작업 스케쥴 설정

```bash
* * * * * 명령어
```

<img src="/images/cron-cmd.png" />

