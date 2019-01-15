# PAM Challenge

### running the app

You can run the app using docker compose, in the app dir just run the command:

```
docker-compose up
```

to change the port of the app, please edit it in docker-compose.yml then run again.

### running tests

You can run the tests using another docker compose config file, just run:

```
docker-compose -f ./docker-compose.test.yml up
```

### TODOs:
The API is still missing the support for different responses like in the case when the input parameters or the headers are not valid (I was picking up my battles here)
