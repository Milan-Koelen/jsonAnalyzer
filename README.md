
# JSON analyser

A python based JSON analyzer and transformation generator/assistant.

Test in action @ http://optimus.milankoelen.com/
## Deploy and Testing Pipelines

![Deploy badge](https://github.com/milan-koelen/jsonAnalyzer/actions/workflows/test.yaml/badge.svg?branch=test)
## Features

- List *all* JSON fields and nested fields
- List all Arrays in json
- List all fields with pottential empty objects
- Make and analyze request 
- Create mongodb transformation pipeline


## API Reference

### Test Connection

#### Returns Pong

```http
  GET /ping
```

#### Response
``
"Pong"
``

### Return "Hello World"

```http
  GET /
```

#### Response
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `message ` | `string ` | Hello World|

### Explore JSON

#### Returns fields

```http
  POST /fields
```
**Expects:**  JSON object or array 

Provide raw json and returns all fields and arrays found.

#### Response
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `arrays ` | `array ` | List of arrays found in the provided JSON|
| `fields ` | `array ` | List of fields found in the provided JSON (in dotnotation and deduplicated)|



#### Returns flat json object

```http
  POST /flatten
```
**Expects:**  JSON object or array 

Returns flatten json object from first object in array.

#### Response
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `JSON ` | `object ` | 1 level deep JSON object with all nested fields on top level (dotnotation and deduplicated)|



## Tech Stack


**Server:** Python, Flask, Flask-limiter


