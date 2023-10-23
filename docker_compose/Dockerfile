######################## Build stage ########################
FROM python:3.11-alpine as builder

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up build mode (dev or prod)
ARG BUILD_MODE
ENV MODE=${BUILD_MODE}

# Install psycopg2 dependencies
RUN apk update && apk add --no-cache make

COPY ./requirements.txt .
COPY ./requirements-dev.txt .
COPY ./Makefile .

# Create wheels for deps from requirements.txt if MODE=prod,
# create wheels with dev deps from requirements-dev.txt if MODE=dev
RUN make wheels


######################## Final stage ########################
FROM python:3.11-alpine

# Create appropriate directories
ENV APP_HOME=/home/app/web
RUN mkdir -p $APP_HOME/staticfiles
WORKDIR $APP_HOME

# Set up build mode (dev or prod)
ARG BUILD_MODE
ENV MODE=${BUILD_MODE}

# Install dependencies
RUN apk update && apk add --no-cache \
  libpq \
  make \
  gettext
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
COPY --from=builder /usr/src/app/requirements-dev.txt .
RUN pip install --no-cache-dir /wheels/*

# Copy project files
COPY . $APP_HOME

# Create non-root app user, chown all files to the app user
RUN addgroup -S app && adduser -S app -G app && chown -R app:app $APP_HOME 

# RUN chown -R app:app entrypoint.sh && \
#   chmod u+x entrypoint.sh

# Change to the app user
USER app

EXPOSE 8000

# Run production gunicorn server if MODE=prod,
# run django dev server for cot code reload if MODE=dev
CMD [ "./entrypoint.sh" ]
# CMD [ "make", "run-gunicorn-docker" ]
