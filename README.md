# mh-team3


### Code style and formatting

The docker image checks for proper styling using
[black](https://black.readthedocs.io/en/stable/).

You should install `black` locally to automatically format your code with
`black .` at the repo root.

### Running stack locally

```bash
docker-compose up api
```

### Running tests

```bash
docker-compose up --exit-code-from test test
```
