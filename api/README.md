# RestaurantX Contactless Pickup API Backend Microservice

## Developing/Running

- Install Python3, Poetry
- Run `poetry install --no-dev --no-interaction`
- Run `python -m quickpickup`

## Testing

### Codestyle

- Run `black --check .`

### Convention and Syntax

- Run `flake8 .`

### Unit Tests
- Run `UNIT_ONLY=True pytest -v --color=yes test/`