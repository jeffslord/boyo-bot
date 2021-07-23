FROM python:3

WORKDIR /usr/src/app

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --deploy --system

COPY . .

CMD ["sh", "scripts/run.sh"]
