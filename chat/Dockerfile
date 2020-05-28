##################
# Base image stage
#
FROM python:3.8

# Poetry is our packaging tool of choice
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"

# Work off source
RUN mkdir /local
WORKDIR /local

# Copy in package files for installation
COPY poetry.lock .
COPY poetry.toml .
COPY pyproject.toml .

# Install non-dev dependencies
RUN poetry install --no-dev --no-interaction

# Copy in just app code
COPY . /local

EXPOSE 5030

CMD ["python", "chatbot/webex_teams_bot.py"]
