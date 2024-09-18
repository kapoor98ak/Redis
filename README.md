# Build Your Own Redis Server

Welcome to the Redis-lite repository! This project involves creating a lite version of Redis, an in-memory data structure server. The goal is to support operations similar to the original Redis server.

## Introduction
Redis is a famous in-memory data structure store that serves as a database, cache, and message broker. Known for its versatility and performance, Redis supports a variety of data types, including strings, hashes, lists, sets, and sorted sets. It is widely used in applications requiring high-speed data access, real-time analytics, and caching.

## Project Objective
This project aims to create a lightweight, Python-based version of Redis, termed "Redis Lite." The goal is to replicate essential functionalities of Redis while simplifying its core operations. This project will focus on understanding and implementing the core concepts behind Redis, including:

- **Redis Serialization Protocol (RESP)**: I implemented my version of the communication protocol used by Redis, which defines how data is serialized and deserialized between the server and clients.
- **Basic Commands**: Implemented fundamental commands such as SET and GET, which are crucial for data storage and retrieval.
- **Concurrency**: Handled simultaneous multiple client connections to mimic Redis’s ability to manage concurrent requests.
- **Expiry Mechanisms**: Added support for command expiry options to understand Redis’s data expiration capabilities.
- **Additional Commands**: Expanded functionality to include various Redis commands such as EXISTS, DEL, INCR, DECR, LPUSH, and RPUSH.
- **Performance Testing**: Compare the performance of your Redis Lite server against the official Redis server to assess efficiency and speed.

## Educational Goals
By building this Redis Lite server, I gained hands-on experience with:

- **Network Programming**: Learnt to manage client-server communication over TCP/IP in Python.
- **Serialization Protocols**: Understood how data is encoded and decoded in a real-world system.
- **Concurrency Models**: Explored multi-threading or asynchronous approaches to handle multiple simultaneous connections.
- **System Design**: Develop a deeper understanding of how in-memory data stores are designed and optimized.

This project was an excellent opportunity to delve into the inner workings of Redis and gain practical experience in building a high-performance data structure server.

## Table of Contents

- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Setup](#setup)
- [Steps](#steps)
  - [Step Zero: Environment Setup](#step-zero-environment-setup)
  - [Step One: RESP Serialization/Deserialization](#step-one-resp-serializationdeserialization)
  - [Step Two: Building the Redis Server](#step-two-building-the-server)
  - [Step Three: Core Functionality - SET and GET](#step-three-core-functionality---set-and-get)
  - [Step Four: Handling Concurrent Clients](#step-four-handling-concurrent-clients)
  - [Step Five: SET Command Expiry Options](#step-five-set-command-expiry-options)
  - [Step Six: Additional Commands](#step-six-additional-commands)
  - [Step Seven: Performance Testing](#step-seven-performance-testing)
- [Further Development](#further-development)
- [Contact](#contact)

## Introduction

Redis is an in-memory data structure server supporting strings, hashes, lists, sets, sorted sets, and more. This project is inspired by Redis's original goal as a REmote DIctionary Server. To do this, I built a lite version of Redis supporting similar operations, implemented in Python.

## Project Overview

The project is divided into several steps, each focusing on different aspects of building a Redis server:

1. **Environment Setup**: Prepare the development environment.
2. **RESP Serialization/Deserialization**: Implement the Redis Serialization Protocol.
3. **Building the Server**: Create a server that listens for client connections and handles basic commands.
4. **Core Functionality**: Implement the SET and GET commands.
5. **Concurrent Clients**: Handle multiple client connections concurrently.
6. **SET Command Expiry Options**: Extend the SET command to support expiry options.
7. **Additional Commands**: Implement commands like EXISTS, DEL, INCR, DECR, LPUSH, RPUSH, and SAVE.
8. **Performance Testing**: Compare performance with the original Redis.

## Setup

To get started, clone this repository and set up your development environment. Ensure you have Python installed and optionally install Redis for testing purposes.

```bash
git clone https://github.com/kapoor98ak/redis-lite.git
cd redis-lite
```

## Steps
### Step Zero: Environment Setup
Set up your development environment, including your editor and necessary tools for network programming and test-driven development (TDD). Optionally, install Redis for testing your implementation.

### Step One: RESP Serialization/Deserialization
Implement the Redis Serialization Protocol (RESP). This protocol is used to communicate with a Redis Server. Create tests for example messages to ensure correct serialization and deserialization.

### Step Two: Building the Server
Create a Redis Lite server that starts and listens on port 6379. Implement the PING command to respond with PONG.

### Step Three: Core Functionality - SET and GET
Implement the core functionality of Redis by adding support for the SET and GET commands.

```bash

% redis-cli set Name John
OK
% redis-cli get Name
"John"
```

### Step Four: Handling Concurrent Clients
Make your Redis Lite server handle multiple concurrent clients. You can choose between multi-threading or asynchronous programming.

### Step Five: SET Command Expiry Options
Extend the SET command to support the EX, PX, EXAT, and PXAT expiry options. Ensure that the expiry is implemented efficiently.

### Step Six: Additional Commands
Implement additional commands:

1. EXISTS: Check if a key is present.
2. DEL: Delete one or more keys.
3. INCR: Increment a stored number by one.
4. DECR: Decrement a stored number by one.
5. LPUSH: Insert values at the head of a list.
6. RPUSH: Insert values at the tail of a list.
7. SAVE: Save the database state to disk and implement load on startup.

### Step Seven: Performance Testing
Use Redis Benchmark to test the performance of your server. Compare your server's performance with the original Redis server.


```bash
% redis-benchmark -t SET,GET -q
SET: 108225.10 requests per second, p50=0.223 msec
GET: 115606.94 requests per second, p50=0.215 msec
```





