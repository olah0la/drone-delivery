


```bash
docker compose run --rm event-collector alembic revision --autogenerate -m "init" 
```


```bash
docker compose run --rm event-collector alembic upgrade head
```

