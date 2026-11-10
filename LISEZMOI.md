# Site Tidiane Diop — Road to LA28

Site statique en HTML, CSS et JavaScript, sans dépendance. Il est prêt à déposer chez n'importe quel hébergeur, par exemple dans le dossier `public_html` sur Hostinger.

## Pages
- `index.html` : accueil
- `athlete.html` : l'athlète
- `road-to-la28.html` : Road to LA28
- `media.html` : Media & Stories
- `partenaires.html` : partenaires officiels
- `devenir-partenaire.html` : page commerciale, avec les quatre niveaux d'engagement
- `opportunites.html` et six pages sectorielles `opportunites-*.html`
- `dossier-sponsoring.html` : version web du dossier, avec le PDF dans `assets/dossier-sponsoring-tidiane-diop.pdf`
- `contact.html` : formulaire qualifiant
- `mentions-legales.html` : mentions légales et données personnelles

## Avant la mise en ligne
1. **Domaine :** le site est publié sur GitHub Pages à `https://visionary237.github.io/tidiane-road-to-la28/`. Pour passer sur un domaine propre, changer `SITE_URL` dans `build.py`, relancer `python3 build.py`, puis ajouter un fichier `CNAME`.
2. **Éléments à compléter :** chaque information manquante apparaît sur le site dans un cadre en pointillés. La liste :
   - année du titre de vice-champion de Normandie et lien vers le justificatif officiel ;
   - histoire de Tidiane, racontée dans ses propres mots ;
   - rôle exact de Coach du peuple et nature du lien avec HAC kickboxing ;
   - calendrier des compétitions ;
   - période couverte par les statistiques Instagram ;
   - détails du soutien Brothers Kitchen ;
   - crédits des photographes ;
   - éditeur, hébergeur et responsable du traitement dans les mentions légales.
3. **Autorisations :** obtenir l'accord écrit de Brothers Kitchen et de Planète Fitness pour l'usage de leurs noms, logos et photos. Faire de même avec les personnes reconnaissables sur les photos.
4. **Planète Fitness :** la fiche indique « Échanges en cours ». Elle est à changer dans `partenaires.html` une fois l'accord signé.

## Connexion au CRM MFM
Le formulaire envoie un POST JSON à l'adresse définie dans `assets/config.js`, dans le champ `crmEndpoint`. Tant que ce champ est vide, le formulaire affiche un message d'aperçu et n'envoie rien.

Champs envoyés : `entreprise`, `secteur`, `nom`, `fonction`, `email`, `type_partenariat`, `budget`, `message`, `consentement`, `texte_consentement`, `page`, `date`, `source`.

L'adresse de réception doit être en HTTPS (webhook, n8n ou API du CRM). Côté serveur, elle doit :
- revalider les champs ;
- refuser les envois dont le champ `website` est rempli (c'est le champ piège anti-spam) ;
- limiter le nombre d'envois par adresse IP ;
- conserver la preuve du consentement.

N'y faire figurer aucune règle de scoring ni aucune donnée de budget interne.

## Modifier les contenus
Les textes, niveaux de partenariat et pages sectorielles se modifient dans `build.py`. Relancer ensuite `python3 build.py` pour régénérer toutes les pages. Les styles sont dans `assets/site.css`.

Les polices sont hébergées sur le site, dans `assets/fonts`, et aucun cookie n'est déposé. Si un outil de mesure d'audience est ajouté plus tard, il faudra mettre en place un bandeau de consentement.
