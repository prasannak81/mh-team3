# quickpickup

A meraki app to facilitate contactless pickup for customer orders.

### Code style and formatting

This section descripts our code formatting tools.

#### Python

The docker image checks for proper styling using
[black](https://black.readthedocs.io/en/stable/).

You should install `black` locally to automatically format your code with
`black .` at the repo root.

### Running stack locally

The local stack provides all the services needed to run the application.

<!-- TODO: Switch this to bring up the nginx container when we have it. -->

```bash
# Build and bring up the API container and its dependencies
docker-compose up --build api
```

### Running tests

Unit tests which are mocked or require no external dependencies will always run
during the container build process to prevent building broken images. For
integration tests, we use docker-compose to bring up dependent services and run
our tests.

```bash
# Build and run integration tests
docker-compose up --build --exit-code-from test test
```

### Running the stack in a "production" setting

We're not really using Production or we'd be building and publishing images,
but we have a "production"-ish docker-compose we can use to spin up the
services we want in a more locked fashion.

```bash
# Start up the stack in daemon mode, rebuilding the images as needed
docker-compose -f docker-compose.prod.yml up -d --build
```

