FROM python:3.7-slim as release
RUN apt-get update
RUN apt-get install -y vim
ARG GIT_COMMIT=unspecified
LABEL git_commit=$GIT_COMMIT

ARG BRANCH=unspecified
LABEL git_branch=$BRANCH

EXPOSE 8000

COPY --from=listener-service-db-pre-build /install /usr/local
COPY ./build/dist/app /app

# Add docker-compose-wait tool -------------------
ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000","--env-file", "app/dev.env"]
