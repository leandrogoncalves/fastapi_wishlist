start:
  docker compose up -d
  docker exec -it app cp .env.example .env

run-tests:
  docker compose up test --abort-on-container-exit --exit-code-from test

stop:
  docker compose down test

test: run-tests stop

view-coverage:
  xdg-open htmlcov/index.html || open htmlcov/index.html || start htmlcov/index.html