# REST API Documentation

This project provides a REST API for managing "perevals".

## Endpoints

### Get Pereval by ID

**GET** `/submitData/<int:id>`

#### Parameters

- `id` (int, required): ID of the Pereval

#### Responses

- `200 OK`: Pereval found
- `404 Not Found`: Pereval not found

### Update Pereval by ID

**PATCH** `/submitData/<int:id>`

#### Parameters

- `id` (int, required): ID of the Pereval
- `body` (JSON, required):
  - `name` (string): Name of the Pereval
  - `height` (integer): Height of the Pereval
  - `difficulty` (string): Difficulty level of the Pereval

#### Responses

- `200 OK`: Pereval updated
- `400 Bad Request`: Invalid request
- `500 Internal Server Error`: Server error

### Get Perevals by Email

**GET** `/submitData/`

#### Parameters

- `user__email` (string, required): Email of the user

#### Responses

- `200 OK`: Perevals found
- `400 Bad Request`: Email parameter is required
- `500 Internal Server Error`: Server error

## Running Tests

To run tests:
```sh
pytest
