# Contribuer

Ce dépôt est un petit projet pédagogique, mais les modifications doivent rester faciles à relire et reproductibles.

## Processus de contribution

1. Créez une branche ciblée depuis `main` ; ne travaillez pas directement sur `main`.
2. N’ajoutez jamais à Git des secrets, fichiers `.env`, kubeconfigs, états Terraform ou identifiants cloud.
3. Préservez l’application existante, la conception de l’infrastructure et le contrat de l’API asynchrone. Placez toute proposition de modification du comportement technique dans une pull request distincte, soumise à une revue explicite.
4. Exécutez les contrôles pertinents ci-dessous.
5. Ouvrez une pull request qui explique la modification, les validations effectuées et les limites restantes.

## Contrôles locaux

Copiez `.env.example` vers `.env` avant d’exécuter les commandes Compose. L’application actuelle utilise les identifiants par défaut de Pika pour le développement local ; ne réutilisez pas cette configuration de compatibilité en dehors d’une machine de développement isolée.

```bash
python -m compileall -q application tests
python -m unittest discover -s tests -v
docker compose config --quiet
docker compose build
terraform -chdir=foundation fmt -check
terraform -chdir=foundation init -backend=false
terraform -chdir=foundation validate
```

Lorsque les manifestes Kubernetes sont modifiés, exécutez également :

```bash
kubeconform -strict -summary kubernetes/
```

Utilisez `docker compose up --build -d` et envoyez au moins un calcul lorsque vous modifiez la communication entre les composants.

## Périmètre et sécurité

- Ne publiez pas d’images, ne déployez pas d’infrastructure et ne modifiez pas les paramètres du dépôt depuis une pull request sans autorisation explicite.
- N’incluez jamais d’identifiants réels ni de détails sur une infrastructure interne dans les exemples, journaux, captures d’écran ou jeux de données de test.
- Ne modifiez pas la logique de l’application, les ressources Kubernetes ou les ressources Terraform dans le cadre d’un travail de portfolio limité à la documentation.
- Préférez les améliorations ciblées aux réécritures importantes et décrivez précisément les fonctionnalités partielles.
