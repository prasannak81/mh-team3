##################
# Base image stage
#
FROM python:3.8 AS base

# Poetry is our packaging tool of choice
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"

# Work off source
WORKDIR /usr/local/src

# Copy in package files for installation
COPY poetry.lock .
COPY poetry.toml .
COPY pyproject.toml .

# Install non-dev dependencies
RUN poetry install --no-dev --no-interaction

############
# Test stage
#
FROM base AS test

# Install all dependencies
RUN poetry install --no-interaction

# Copy in source tree
COPY . /usr/local/src/

# Codestyle check
RUN black --check .

# Code convention and syntax check
RUN flake8 .

# Run pure unit tests
RUN UNIT_ONLY=True pytest -v --color=yes test/

###################
# Final image stage
#
FROM base AS final

EXPOSE 8080

# Copy in just app code
COPY ./quickpickup/ /usr/local/src/quickpickup/

CMD ["python", "-m", "quickpickup"]
