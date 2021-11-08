FROM python:3.9.7-alpine

# https://www.psycopg.org/psycopg3/docs/basic/install.html#pure-python-installation
# https://stackoverflow.com/a/51543463/6587143
RUN apk update && apk add libpq
RUN apk add gcc python3-dev musl-dev postgresql-dev

# Install dependencies
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install coverage flake8

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .

# Run app
CMD [ "python", "-u", "app.py" ]
