# Configuration


# Kafka with Zookeeper

## Install

```bash
brew install kafka
```

Homebrew's default installation path will differ based on the chips: Macs with Apple Silicon will install kafka under `/opt/homebrew/Cellar`. 

- Binaries and scrips will be in `/opt/homebrew/bin`

- Kafka configurations will be in `/opt/homebrew/etc/kafka`

- Zookeeper configurations will be in `/opt/homebrew/etc/zookeeper`

- The `log.dirs` config(the location of kafka data) will be set to `/opt/homebrew/var/lib/kafka-logs`

## Setup the $PATH environment variable

In order to easily access the kafka binaries, you can edit your PATH variable by adding the following line(edit the content to your system) to your system run commands(`~/.zshrc`)

`PATH="$PATH:/Users/seilylook/Development/Kafka/kafka_2.13-3.0.0/bin"`

This ensures that you can now run the kafka commands without prefixing them

After reloading the terminal, the following should work from any directory.

```bash
kafka-topics.sh
```

## Start Zookeeper

Apache Kafka depends on Zookeeper for cluster management. Hence, prior to starting Kafka, Zookeeper has to be started. There is no need to explicitly install Zookeeper, as it comes included with Apache Kafka.

```bash
/opt/homebrew/bin/zookeeper-server-start /opt/homebrew/etc/zookeeper/zoo.cfg
```

## Start Kafka

**Open another Terminal window** and run the following command from the root of Apache Kafka to start.

```bash
kafka-server-start.sh ./Development/Kafka/kafka_2.13-3.8.0/config/server.properties
```

Ensure to keep both terminal windows opened, otherwise you will shut down Kafka or Zookeeper.

# Kafka with KRaft: without Zookeeper

1. Download Kafka from [HERE](https://kafka.apache.org/downloads) under **Binary Downloads**

2. Extract the contents on Mac

3. Generate a cluster ID and format the storage using `kafka-storage.sh`

4. Start Kafka using the binaries

5. Setup the $PATH environment variables for easy access to Kafka binaries

## Start Kafka

The first step is to generate a new ID for your cluster

```bash
kafka-storage.sh random-uuid
```

This returns a UUID

Next, format your storage directory (replace <uuid> by your UUID obtained above)

```bash
kafka-storage.sh format -t <UUID> -c ./Development/Kafka/kafka_2.13-3.8.0/config/kraft/server.properties
```

This will format the directory that is in the `log.dirs` in the `config/kraft/server.properties` file (by default `/tmp/kraft-combined-logs`)

Now you can launch the broker itself in deamon mode by running this command

```bash
kafka-server-start.sh ./Development/Kafka/kafka_2.13-3.8.0/config/kraft/server.properties
```

# Kafka CLI

kafka Topic Management

- Create Kafka Topics

- List Kafka Topics

- Describe Kafka Topics

- Increase Partitions in a Kafka Topic

- Delete Topics
