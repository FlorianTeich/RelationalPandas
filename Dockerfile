FROM python:3.10-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y gcc build-essential
RUN python -m venv /venv
COPY Pipfile ./
ENV PIPENV_VENV_IN_PROJECT 1
RUN pipenv install

FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"
COPY . .

# create a folder to hold the downloaded/built requirements
RUN mkdir -p /srv/relationalpandas
RUN mkdir -p /srv/tests
RUN mkdir -p /srv/docs
COPY relationalpandas /srv/relationalpandas
COPY tests /srv/tests
COPY docs /srv/docs

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /srv/
USER appuser

RUN python -m pytest -v --junit-xml /home/appuser/test_results.xml tests/test.py

WORKDIR /srv/docs
RUN sphinx-apidoc -f -o ./ ../relationalpandas
RUN make html
