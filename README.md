# mini-spend-tracker

mini-spend-tracker is a simple HTTP server allowing users to track their spendings which can be used as a simple budgeting tool.
Data is stored in a SQLite database (`db/schema.db` can be cloned to create a new database). 

## Features

- Minimalistic HTTP server, to add daily spendings per category.
- A dashboard allows to display the current month spendings per category, and the spendings variations over previous months.
- Rule patterns can be created allowing to simply add spendings coming from bank statements.

Example rule pattern:
```
{"pattern": "^begin (\\d+) (.+) test (\\d)$", "variable_positions": {"day": 0, "month": 1, "amount": 2}}
```

means that when you add the following line:

```
begin 18 january test 10
```

the server will add a spending of 10$ on the 18th of January.

## Installation

- Clone the repository
- Copy `db/schema.db` to `db/spendings.db` (or change `DB_FILENAME` to a different filename if needed). 
- `docker-compose up --build -d`. docker-compose.yml is provided to run the server in a Docker container (Python 3.10+ required).

