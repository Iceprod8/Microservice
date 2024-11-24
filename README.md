# Projet Microservices avec Docker

Ce projet est constitué de plusieurs services Docker (ex. `user_service`, `movie_service`, etc.) connectés à leurs propres bases de données PostgreSQL respectives. Ce guide vous aidera à configurer, lancer et mettre à jour les services sans avoir à redémarrer tout le projet.

## Prérequis

- **Docker** : Assurez-vous que Docker et Docker Compose sont installés sur votre machine.

## Démarrage du Projet

Pour lancer le projet, assurez-vous que tous les fichiers nécessaires (code source et fichiers de configuration) sont en place, puis exécutez la commande suivante :

```bash
docker-compose build
docker-compose up -d
```

Cette commande va :
1. Construire les images Docker pour chaque service.
2. Démarrer les conteneurs pour chaque service et leurs bases de données.

Tous les services seront disponibles et communiquent entre eux via le réseau Docker défini dans le fichier `docker-compose.yml`.

## Accéder aux Services

Chaque service est exposé via le service `gateway`, qui permet d'accéder à tous les services depuis un seul point d'entrée.

Exemple pour accéder à l'API `user_service` :
```
http://localhost:80/user_service/users
```

## Mettre à Jour un Service Spécifique

Si vous modifiez le code d'un service spécifique (par exemple `user_service`), vous n'avez pas besoin de redéployer tout le projet. Suivez les étapes ci-dessous pour mettre à jour seulement ce service :

1. **Rebuild** l'image du service mis à jour (ex. `user_service`) :

   ```bash
   docker-compose build user_service
   ```

2. **Redémarrez** uniquement ce service avec la commande suivante :

   ```bash
   docker-compose up -d user_service
   ```

Ces commandes vont reconstruire et redémarrer uniquement le service `user_service`, en gardant les autres conteneurs inchangés.

## Mettre à Jour une Base de Données Spécifique

Dans certains cas, vous pourriez avoir besoin de mettre à jour la structure d'une base de données pour un service sans toucher aux autres. Voici les étapes pour mettre à jour une seule base de données :

1. **Apportez les modifications nécessaires** dans le fichier SQL d'initialisation (par exemple `init_user_db.sql` pour la base de données `user_service`).
2. **Supprimez le volume Docker** pour cette base de données afin de forcer une réinitialisation de celle-ci.

   > Attention : Cette étape supprimera toutes les données de la base de données pour le service concerné.

   ```bash
   docker-compose down -v
   ```

3. **Redémarrez uniquement le service de base de données** pour le service que vous souhaitez mettre à jour :

   ```bash
   docker-compose up -d postgres
   ```

4. Enfin, redémarrez le service associé (par exemple `user_service`) pour que celui-ci puisse recréer les tables avec la nouvelle structure SQL :

   ```bash
   docker-compose up -d user_service
   ```

> **Note** : Assurez-vous de bien communiquer avec l'équipe avant de supprimer un volume, car cela affecte la persistance des données pour tous les développeurs.

Cela vous permet de déboguer et de vérifier les messages d’erreur, si le service ne fonctionne pas comme prévu.

## Bonnes Pratiques

- **Ne redémarrez pas tous les services si vous n'en avez pas besoin** : Évitez d'utiliser `docker-compose up -d --build` sans préciser de service pour minimiser les interruptions.
- **Utilisez des branches Git spécifiques pour chaque service** : Cela permettra à chaque développeur de travailler indépendamment sans affecter les autres services.
- **Documentez les modifications de la base de données** : Avant de mettre à jour la base de données, assurez-vous d'informer l'équipe des changements afin de synchroniser les modifications de schéma.