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

3. Create database "journey" and "journey" collection, importing file sample_data/journeys.json

4. Add "stage" collection and import files:
 - sample_data/journeyc.json
 - sample_data/journeyf.json
 - sample_data/journeyl.json
 - sample_data/journeym.json


### API docs:
access swagger route via: http://localhost:5000/swagger