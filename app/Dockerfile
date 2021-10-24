FROM python:3.9.7-alpine

# Install psycopg
# https://www.psycopg.org/psycopg3/docs/basic/install.html#pure-python-installation
# https://stackoverflow.com/a/51543463/6587143
RUN apk update && apk add libpq
RUN apk add gcc python3-dev musl-dev postgresql-dev

RUN pip install --upgrade pip
RUN pip install psycopg

# Other dependencies
RUN pip install Flask
RUN pip install flask-cors
RUN pip install flake8
RUN pip install coverage

# Copy source code
WORKDIR /app
COPY . .

# Run app
CMD [ "python", "-u", "app.py" ]