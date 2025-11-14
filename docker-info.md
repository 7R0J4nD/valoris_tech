# Construire et lancer les containers
## Construire l'image
```bash

docker-compose build
```

## Lancer les services
```bash

docker-compose up
```
L’application FastAPI sera accessible sur : http://localhost:5500

PostgreSQL est exposé sur le port 5432 pour l’accès externe (pgAdmin, DBeaver, etc.).

## Étapes post-lancement (Optionnel)
1. Vérifier la connexion DB dans src/db/database.py.
2. Utilisation manuelle de Alembic pour les migrations :

```shell
# Entrer dans le container de l'app
docker exec -it valoris_app bash

# Lancer les migrations
alembic upgrade head

```
## Commandes utiles

```shell

docker-compose down            # Stop et supprime les containers

docker-compose up --build      # Reconstruire et lancer

docker logs -f valoris_app     # Voir les logs de l'application

docker exec -it valoris_app bash  # Entrer dans le container

```