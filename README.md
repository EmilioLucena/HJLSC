# simple-flask-mongo-api
super simple db + api

1. run api:
```console
docker-compose up
```
2. access mongo via compass:
```console
mongodb://mongodbuser:mongodbpassword@localhost:27017/?authSource=admin
```

3. Create database "jornada" and add "etapa" collection using example file (sample_data/etapas.json)

### API docs:
access swagger route via: http://localhost:5000/swager