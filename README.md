Iris : 
- Temps d'exécution sur GCP : **0,14** s
- Temps d'exécution en local : **0,013** s

➡️ Je n’ai pas testé le cas d’Iris plus en profondeur, car le modèle était très simple.

NLP : 
- Temps d'exécution sur GCP : 0.11s sur 1 ligne de texte et 0.19s sur 9 lignes de textes.
- Temps d'exécution en local : 0.02s sur 1 ligne de texte et 0.32s sur 9 lignes de textes.

Sur 9 itérations, le modèle a fourni 9 réponses correctes sur 9.

➡️ Le déploiement sur GCP s'avère particulièrement intéressant dans ce cas, avec une réduction de plus de 40 % du temps d'exécution sur un petit lot de données — ce qui démontre un bon potentiel de scalabilité.
