#!/usr/bin/env python3
"""Génère le site statique Tidiane Diop / Road to LA28 dans dist/.
Toutes les pages partagent l'en-tête, la navigation, le pied de page, site.css et site.js.
Modifier les données ci-dessous puis relancer : python3 build.py"""
import json, os, sys, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = ROOT
META = json.load(open(os.path.join(ROOT, "img_meta.json")))

# ---------------------------------------------------------------- configuration
SITE_URL = "https://visionary237.github.io/tidiane-road-to-la28"   # remplacer par le domaine définitif le jour venu
SITE_NAME = "Tidiane Diop — Road to LA28"
TIKTOK = "https://www.tiktok.com/@tidiboy29"
INSTAGRAM = "https://www.instagram.com/tidiboy29/"
MANAGER = "Resnick Njeke"
PHONE = "06 16 62 84 86"
FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,500..900"
         "&family=JetBrains+Mono:wght@400;500&family=Public+Sans:wght@400;600;700&display=swap")

NAV = [
    ("index.html", "Accueil"),
    ("athlete.html", "L’athlète"),
    ("road-to-la28.html", "Road to LA28"),
    ("media.html", "Media & Stories"),
    ("partenaires.html", "Partenaires"),
    ("devenir-partenaire.html", "Devenir partenaire"),
    ("contact.html", "Contact"),
]

def esc(s): return html.escape(s, quote=True)
def todo(s): return f'<span class="todo">{esc(s)}</span>'

def pic(name, alt, sizes="100vw", cls="", eager=False, pos=None):
    w, h = META[name]
    style = f' style="object-position:{pos}"' if pos else ""
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img src="assets/img/{name}-1600.webp" srcset="assets/img/{name}-800.webp 800w, assets/img/{name}-1600.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{esc(alt)}"{c}{style} {load}>')

def person(role, name, text, thumb=None, mono=None, links=()):
    if thumb:
        v = f'<img class="avatar" src="assets/img/{thumb}.webp" width="240" height="240" alt="" loading="lazy">'
    else:
        v = f'<span class="avatar mono" aria-hidden="true">{esc(mono or name[:2])}</span>'
    ls = "".join(
        f'<a class="btn btn-ghost btn-sm" href="{esc(u)}"' + ('' if u.endswith('.html') else ' target="_blank" rel="noopener"') + f'>{esc(t)}</a>'
        for t, u in links)
    return (f'<article class="person">{v}<div class="stack" style="gap:8px"><p class="label">{esc(role)}</p><h3>{esc(name)}</h3>'
            f'<p class="muted">{esc(text)}</p>' + (f'<div class="actions">{ls}</div>' if ls else '') + '</div></article>')

def ropes(): return '<div class="ropes" aria-hidden="true"><span></span><span></span><span></span></div>'

# ---------------------------------------------------------------- gabarit commun
def page(slug, title, desc, body, og_image="assets/img/og-tidiane.jpg", jsonld=None, full_doc=True):
    url = f"{SITE_URL}/{'' if slug == 'index.html' else slug}"
    nav_items = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == slug else ""}>{esc(t)}</a></li>' for h, t in NAV)
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    head = f"""<title>{esc(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{esc(SITE_NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0a0a0d">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
{ld}"""
    content = f"""<a class="skip" href="#contenu">Aller au contenu</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">Tidiane Diop <small>60 kg · Le Havre</small></a>
    <nav class="nav" aria-label="Navigation principale"><ul>{nav_items}</ul></nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-nav"><span class="bars" aria-hidden="true"><i></i><i></i><i></i></span><span class="txt">Menu</span></button>
  </div>
  <nav id="mobile-nav" class="mobile-nav" aria-label="Navigation mobile" hidden><div class="wrap"><ul>{nav_items}</ul></div></nav>
</header>
<main id="contenu">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="stack">
        <p class="brand">Tidiane Diop</p>
        <p class="muted">Boxeur amateur, catégorie 60 kg. Basé au Havre, en route vers Los Angeles 2028, sans qualification acquise : un objectif construit étape par étape.</p>
      </div>
      <div><h2>Le projet</h2><ul><li><a href="athlete.html">L’athlète</a></li><li><a href="road-to-la28.html">Road to LA28</a></li><li><a href="media.html">Media & Stories</a></li></ul></div>
      <div><h2>Partenaires</h2><ul><li><a href="partenaires.html">Partenaires officiels</a></li><li><a href="devenir-partenaire.html">Devenir partenaire</a></li><li><a href="opportunites.html">Opportunités</a></li><li><a href="dossier-sponsoring.html">Dossier sponsoring</a></li></ul></div>
      <div><h2>Suivre</h2><ul><li><a href="{INSTAGRAM}" rel="noopener" target="_blank">Instagram @tidiboy29</a></li><li><a href="{TIKTOK}" rel="noopener" target="_blank">TikTok @tidiboy29</a></li><li><a href="contact.html">Contact management</a></li></ul></div>
    </div>
    <div class="legal"><span>© <span data-year>2026</span> Tidiane Diop</span><a href="mentions-legales.html">Mentions légales et données personnelles</a><span>Site sans cookie de mesure d’audience</span></div>
  </div>
</footer>
<script src="assets/config.js"></script>
<script src="assets/site.js"></script>"""
    if full_doc:
        return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head}
</head>
<body>
{content}
</body>
</html>
"""
    # Version pour l'aperçu Artifact : le squelette html/head/body est ajouté à la publication
    return head + "\n" + content + "\n"

def cta_band(title, text, primary=("devenir-partenaire.html", "Devenir partenaire"), secondary=("dossier-sponsoring.html", "Voir le dossier sponsoring")):
    return f"""<section class="cta-band"><div class="wrap">
  <div class="stack"><h2>{title}</h2><p class="lead">{text}</p></div>
  <div class="actions"><a class="btn btn-ghost" href="{primary[0]}">{primary[1]}</a><a class="btn btn-ghost" href="{secondary[0]}">{secondary[1]}</a></div>
</div></section>"""

STATS = f"""<div class="stats">
  <div class="stat"><b>60 kg</b><span>Catégorie de combat, boxe amateur</span></div>
  <div class="stat"><b>Vice-champion</b><span>de Normandie · 2025</span></div>
  <div class="stat"><b>49,1 k</b><span>vues sur une publication TikTok épinglée</span></div>
  <div class="stat"><b>35 k</b><span>vues cumulées sur Instagram</span></div>
</div>
<p class="source">Sources : profil TikTok @tidiboy29 (relevé fourni en octobre 2026 : 379 abonnés, 13,9 k mentions J’aime) ; statistiques Instagram communiquées par le management, période {todo('à préciser')}. Les chiffres sont mis à jour à chaque nouveau relevé.</p>"""

CAL_ROWS = [
    ("21 nov. 2026", "Championnat de Normandie Élite", "Condé-en-Normandie (14)", "Régional", "Selon engagement du club"),
    ("28 nov. 2026", "Championnat de Normandie Élite · demi-finales", "À confirmer", "Régional", "Selon résultats"),
    ("5 déc. 2026", "Championnat de Normandie Élite · finales", "À confirmer", "Régional", "Selon résultats"),
    ("16–17 janv. 2027", "Championnats de France amateurs seniors · 1/16 et 1/8 de finale", "Maisnil-lès-Ruitz (62)", "National", "Sur sélection régionale"),
    ("23–24 janv. 2027", "Championnats de France amateurs seniors · 1/4 et 1/2 finales", "Saint-Avold (57)", "National", "Selon résultats"),
    ("30 janv. 2027", "Championnats de France amateurs seniors · finales hommes", "Saint-Quentin (02)", "National", "Selon résultats"),
    ("4–6 juin 2027", "Coupe de France seniors", "À confirmer", "National", "Selon engagement"),
]
CALENDAR = ('<div class="table-wrap"><table><thead><tr><th>Date</th><th>Compétition</th><th>Lieu</th><th>Niveau</th><th>Pour Tidiane</th></tr></thead><tbody>'
            + "".join(f"<tr><td><b>{esc(d)}</b></td><td>{esc(c)}</td><td>{esc(l)}</td><td>{esc(n)}</td><td class=\"muted\">{esc(s)}</td></tr>" for d, c, l, n, s in CAL_ROWS)
            + "</tbody></table></div>")

PERSON_LD = {"@context": "https://schema.org", "@type": "Person", "name": "Tidiane Diop",
             "description": "Boxeur amateur, catégorie 60 kg, basé au Havre.", "url": SITE_URL,
             "homeLocation": {"@type": "Place", "name": "Le Havre, France"},
             "sameAs": [INSTAGRAM, TIKTOK], "knowsAbout": "Boxe"}

# ---------------------------------------------------------------- pages
pages = {}

pages["index.html"] = ("Tidiane Diop — Road to LA28",
 "Tidiane Diop, boxeur amateur 60 kg basé au Havre. Son histoire, sa route vers Los Angeles 2028, ses partenaires et comment le soutenir.",
 f"""<section class="hero">
  <div class="hero-grid">
    <div class="hero-media">{pic('portrait_nb', 'Tidiane Diop souriant, gants aux mains, bras posés sur les cordes du ring', '(min-width: 900px) 50vw, 100vw', eager=True, pos='50% 22%')}</div>
    <div class="wrap hero-copy">
      <div class="kicker"><span class="label">Boxe amateur</span><span class="label">60 kg</span><span class="label">Le Havre</span></div>
      <h1><span>Tidiane</span><span class="violet">Diop</span></h1>
      <p class="signature">Une ambition. Un parcours. Une communauté derrière chaque combat.</p>
      <div class="actions"><a class="btn btn-primary" href="athlete.html">Découvrir son histoire</a><a class="btn btn-ghost" href="devenir-partenaire.html">Devenir partenaire</a></div>
    </div>
  </div>
</section>
<section class="section"><div class="wrap stack-lg">
  {STATS}
</div></section>
<section class="section alt"><div class="wrap split">
  <div class="stack">
    <p class="label">L’histoire</p>
    <h2>De Dakar au Havre</h2>
    <div class="prose"><p>Parti du Sénégal, Tidiane construit son parcours de boxeur depuis Le Havre, où son cousin Saliou l’a accueilli. Sourire facile, sérieux à l’entraînement, il résume sa démarche en un mot qui revient sur chacune de ses publications : <b>PROCESS</b>.</p></div>
    <div class="actions"><a class="btn btn-ghost btn-sm" href="athlete.html">Lire son parcours</a></div>
  </div>
  {pic('sac_nb', 'Tidiane frappant le sac de frappe, photo noir et blanc', '(min-width: 900px) 45vw, 100vw')}
</div></section>
<section class="section"><div class="wrap split rev">
  <div class="stack">
    <p class="label">Road to LA28</p>
    <div class="countdown"><span class="num" data-countdown>—</span><span class="lead">jours avant l’ouverture des Jeux de Los Angeles, le 14 juillet 2028</span></div>
    <p class="muted">Los Angeles 2028 est un objectif, pas une qualification acquise. La route passe par le niveau régional, puis national et international, selon les règles de sélection applicables.</p>
    <div class="actions"><a class="btn btn-ghost btn-sm" href="road-to-la28.html">Voir la feuille de route</a></div>
  </div>
  {pic('garde', 'Tidiane en garde sur le ring, lumière turquoise', '(min-width: 900px) 45vw, 100vw')}
</div></section>
<section class="section alt"><div class="wrap stack">
  <p class="label">Ils accompagnent le parcours</p>
  <div class="strip">
    <a href="partenaires.html#brothers-kitchen">{pic('bk_equipe', 'Tidiane avec deux représentants de Brothers Kitchen', '64px')}<span><b>Brothers Kitchen</b><br><span class="muted">Partenaire officiel · nutrition</span></span></a>
    <a href="partenaires.html#planete-fitness"><img src="assets/img/logo_planete_fitness.webp" width="400" height="400" alt="Logo Planète Fitness" loading="lazy"><span><b>Planète Fitness Le Havre</b><br><span class="muted">Échanges en cours</span></span></a>
  </div>
</div></section>
{cta_band('Associez votre marque à son ambition', 'Du Havre jusqu’à la scène internationale : des contenus authentiques, une présence locale et un suivi clair de chaque action.')}""", PERSON_LD)

pages["athlete.html"] = ("L’athlète — Tidiane Diop",
 "Qui est Tidiane Diop : son parcours du Sénégal au Havre, son palmarès vérifié, son équipe et ses valeurs.",
 f"""<section class="page-head"><div class="wrap stack">
  <p class="label">L’athlète</p><h1>Rencontrez Tidiane</h1>
  <p class="lead">Boxeur amateur en catégorie 60 kg, Tidiane avance avec une méthode simple : travailler, recommencer, progresser.</p>
</div></section>
<section class="section"><div class="wrap split">
  <div class="stack-lg">
    <div class="stack"><p class="label">Le parcours</p><h2>Du Sénégal au Havre</h2>
      <div class="prose">
        <p>Tidiane est parti de Dakar pour poursuivre sa route en Normandie. Au Havre, il a trouvé un point d’appui auprès de son cousin Saliou, qui l’a accueilli. Ce lien familial reste au cœur du projet : avancer avec des personnes qui se soutiennent et tiennent leurs engagements.</p>
        <p>Sur ses réseaux, il partage le quotidien de la préparation : le sac, le ballon lesté, le sparring, la récupération. Le mot qui accompagne ses publications, <b>PROCESS</b>, dit l’essentiel de sa philosophie.</p>
        <p>{todo('À compléter avec Tidiane : ses débuts en boxe, son arrivée au Havre, ce qui le motive — dans ses mots.')}</p>
      </div>
    </div>
    <div class="stack"><p class="label">Les valeurs</p>
      <div class="grid-2">
        <div class="value"><h3>Travail</h3><p class="muted">La régularité avant tout : chaque séance compte.</p></div>
        <div class="value"><h3>Famille</h3><p class="muted">La confiance d’un cercle proche qui tient parole.</p></div>
        <div class="value"><h3>Résilience</h3><p class="muted">Apprendre de chaque combat pour progresser.</p></div>
        <div class="value"><h3>Good vibes</h3><p class="muted">Une énergie collective qui fait avancer la salle.</p></div>
      </div>
    </div>
  </div>
  <div class="stack">
    {pic('sourire', 'Tidiane souriant en salle, mains bandées et gants ouverts', '(min-width: 900px) 45vw, 100vw')}
    <div class="fiche">
      <div class="fiche-head"><span class="label">Fiche boxeur</span><span class="label">Saison 2026</span></div>
      <dl>
        <div class="row"><dt>Nom</dt><dd>Tidiane Diop</dd></div>
        <div class="row"><dt>Discipline</dt><dd>Boxe amateur</dd></div>
        <div class="row"><dt>Catégorie</dt><dd>60 kg</dd></div>
        <div class="row"><dt>Base</dt><dd>Le Havre (76)</dd></div>
        <div class="row"><dt>Origine</dt><dd>Dakar, Sénégal</dd></div>
        <div class="row"><dt>Clubs</dt><dd>ROAD Boxing club · HAC kickboxing</dd></div>
        <div class="row"><dt>Réseaux</dt><dd><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram</a> · <a href="{TIKTOK}" target="_blank" rel="noopener">TikTok</a> · @tidiboy29</dd></div>
      </dl>
    </div>
  </div>
</div></section>
<section class="section alt"><div class="wrap stack-lg">
  <div class="stack"><p class="label">Palmarès vérifié</p><h2>Résultats officiels</h2>
    <p class="muted">Seuls les résultats justifiés par une source officielle (fédération, organisateur) apparaissent ici.</p></div>
  <div class="table-wrap"><table>
    <thead><tr><th>Année</th><th>Compétition</th><th>Catégorie</th><th>Résultat</th><th>Source</th></tr></thead>
    <tbody><tr><td>2025</td><td>Championnat de Normandie</td><td>60 kg</td><td><b>Vice-champion</b></td><td>{todo('lien ou document officiel')}</td></tr></tbody>
  </table></div>
</div></section>
<section class="section"><div class="wrap stack-lg">
  <div class="stack"><p class="label">L’équipe</p><h2>Ceux qui l’entourent</h2></div>
  <div class="people">
    {person('Encadrement', 'Coach du peuple', 'Houdé, coach de sports de combat suivi par plus de 50 000 personnes sur Instagram et TikTok. Il accompagne la préparation de Tidiane.', thumb='av_coach', links=[('Instagram', 'https://www.instagram.com/coach_du_peuple/'), ('TikTok', 'https://www.tiktok.com/@coach_du_peuple')])}
    {person('Club', 'ROAD · Ring Olympique Alain Dessaux', 'Club de boxe de Déville-lès-Rouen, salle Guynemer. Tidiane y combat sous les couleurs violettes du club.', thumb='av_road', links=[('Instagram', 'https://www.instagram.com/road_deville/')])}
    {person('Club', 'HAC Kickboxing', 'La section kickboxing du Havre Athletic Club, le club omnisports historique de la ville.', mono='HAC', links=[('Instagram', 'https://www.instagram.com/hac_kickboxing_officiel_/')])}
    {person('Famille', 'Saliou', 'Son cousin, qui l’a accueilli au Havre. Le premier soutien du projet.', thumb='av_famille')}
    {person('Management', MANAGER, 'Manager : partenariats, calendrier, communication et relation avec les sponsors.', mono='RN', links=[('Contacter', 'contact.html')])}
    {person('Athlète', 'Tidiane Diop', 'Les entraînements, les combats et les coulisses, chaque semaine.', thumb='av_tidiane', links=[('Instagram', INSTAGRAM), ('TikTok', TIKTOK)])}
  </div>
</div></section>
{cta_band('Suivre la suite du parcours', 'Les entraînements, les combats et les coulisses sont publiés chaque semaine sur Instagram et TikTok.', (INSTAGRAM, 'Instagram @tidiboy29'), (TIKTOK, 'TikTok @tidiboy29'))}""", PERSON_LD)

pages["road-to-la28.html"] = ("Road to LA28 — Tidiane Diop",
 "La feuille de route de Tidiane Diop vers Los Angeles 2028 : étapes, compétitions officielles, résultats et journal de progression.",
 f"""<section class="page-head"><div class="wrap stack">
  <p class="label">Road to LA28</p><h1>Une ambition, étape par étape</h1>
  <p class="lead">Los Angeles 2028 est l’objectif. Rien n’est acquis : chaque étape se gagne en compétition, selon les règles de sélection de l’instance compétente.</p>
  <div class="countdown"><span class="num" data-countdown>—</span><span class="muted">jours avant l’ouverture des Jeux, le 14 juillet 2028</span></div>
</div></section>
<section class="section"><div class="wrap split">
  <div class="stack-lg"><div class="stack"><p class="label">La feuille de route</p><h2>Quatre étapes</h2></div>
  <ol class="timeline">
    <li class="now"><span class="step">Étape 1 · en cours</span><h3>Consolidation régionale</h3><p class="muted">Confirmer le niveau en Normandie, après le titre de vice-champion régional.</p><div class="tl-meta"><span><b>Preuve attendue</b>Résultats officiels, licence à jour</span><span><b>Soutien nécessaire</b>Équipement, déplacements régionaux</span></div></li>
    <li><span class="step">Étape 2</span><h3>Progression nationale</h3><p class="muted">Se mesurer au niveau national, sur les championnats applicables.</p><div class="tl-meta"><span><b>Preuve attendue</b>Classements, convocations</span><span><b>Soutien nécessaire</b>Déplacements, préparation physique</span></div></li>
    <li><span class="step">Étape 3</span><h3>Compétitions internationales</h3><p class="muted">Tournois pertinents pour le parcours, à identifier avec l’encadrement.</p><div class="tl-meta"><span><b>Preuve attendue</b>Sélections, résultats publiés</span><span><b>Soutien nécessaire</b>Voyages, hébergement, encadrement</span></div></li>
    <li><span class="step">Étape 4</span><h3>Parcours de qualification</h3><p class="muted">Entrer dans le processus de qualification olympique applicable.</p><div class="tl-meta"><span><b>Preuve attendue</b>Critères de l’instance compétente</span><span><b>Soutien nécessaire</b>Préparation longue durée, staff</span></div></li>
  </ol></div>
  {pic('ballon', 'Tidiane en exercice avec un ballon lesté, noir et blanc', '(min-width: 900px) 45vw, 100vw')}
</div></section>
<section class="section alt"><div class="wrap stack-lg">
  <div class="stack"><p class="label">Calendrier · saison 2026–2027</p><h2>Compétitions officielles</h2><p class="muted">Calendrier officiel de la boxe amateur élite publié par le comité régional de Normandie et la Fédération française de boxe. La participation de Tidiane à chaque tour dépend de son engagement par le club et de ses résultats.</p></div>
  {CALENDAR}
  <p class="source">Sources : <a href="https://boxenormandie.fr/engagements-championnat-normandie-boxe-elite-2026-2027/" target="_blank" rel="noopener">FFBoxe Comité régional Normandie</a> (calendrier 2026-2027 et engagements, consultés le 10 novembre 2026) · <a href="https://www.ffboxe.com/actualites/calendrier-des-competitions-nationales/" target="_blank" rel="noopener">FFBoxe, calendrier des compétitions nationales</a> (mis à jour le 27 octobre 2026). Dates susceptibles d’évoluer : vérifier auprès des organisateurs.</p>
</div></section>
<section class="section"><div class="wrap stack-lg">
  <div class="stack"><p class="label">Journal de progression</p><h2>Les dernières étapes</h2></div>
  <div class="grid-2">
    <article class="card"><p class="label">2025</p><h3>Vice-champion de Normandie</h3><p>Premier titre régional en catégorie 60 kg.</p></article>
    <article class="card"><p class="label">2026</p><h3>Brothers Kitchen rejoint le projet</h3><p>Premier partenaire officiel : un soutien nutritionnel au quotidien de la préparation.</p><a href="partenaires.html#brothers-kitchen">Voir le partenariat</a></article>
  </div>
</div></section>
{cta_band('Accompagner une étape', 'Chaque étape a ses besoins : équipement, déplacements, préparation. Choisissez celle que votre entreprise soutient.')}""")

GALLERY = [
    ("portrait_nb", "Portrait noir et blanc, sourire et gants sur les cordes", ""),
    ("garde", "En garde sur le ring, lumière turquoise", "wide"),
    ("sac_nb", "Travail au sac de frappe", ""),
    ("ballon", "Préparation physique au ballon lesté", ""),
    ("sparring_nb", "Sparring à l’entraînement", ""),
    ("pushup", "Pompes sur le ring", "wide"),
    ("halteres", "Marche avec haltères", ""),
    ("profil_dore", "Portrait de profil en lumière dorée", ""),
    ("ring_public", "Échange sur le ring devant le public", "wide"),
    ("sac_couleur", "Séance au sac", ""),
    ("kettlebell", "Travail au kettlebell", ""),
    ("road_duo", "En tenue ROAD avec un membre du club", ""),
    ("bk_equipe", "Avec l’équipe de Brothers Kitchen", "wide"),
]
gal = "".join(
    f'<button type="button" class="{cls}" data-full="assets/img/{n}-1600.webp" data-caption="{esc(c)}">{pic(n, c, "(min-width: 900px) 25vw, 50vw")}</button>'
    for n, c, cls in GALLERY)

pages["media.html"] = ("Media & Stories — Tidiane Diop",
 "Photos, vidéos et coulisses de la préparation de Tidiane Diop : entraînements, portraits, combats.",
 f"""<section class="page-head"><div class="wrap stack">
  <p class="label">Media & Stories</p><h1>La préparation en images</h1>
  <p class="lead">Entraînements, portraits et coulisses. Les vidéos sont publiées en premier sur Instagram et TikTok.</p>
  <div class="actions"><a class="btn btn-primary btn-sm" href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram @tidiboy29</a><a class="btn btn-ghost btn-sm" href="{TIKTOK}" target="_blank" rel="noopener">TikTok @tidiboy29</a></div>
</div></section>
<section class="section"><div class="wrap stack">
  <p class="label">Photos</p>
  <div class="gallery">{gal}</div>
  <p class="source">Crédits photo : {todo('noms des photographes à compléter')}. Toute réutilisation nécessite l’accord du management.</p>
</div></section>
<section class="section alt"><div class="wrap stack-lg">
  <div class="stack"><p class="label">Vidéos et récits</p><h2>À voir et à lire</h2></div>
  <div class="grid-3">
    <div class="card"><p class="label">Série</p><h3>Une semaine dans la préparation</h3><p>Le quotidien d’une semaine d’entraînement, du sac à la récupération.</p><a href="{TIKTOK}" target="_blank" rel="noopener">Voir sur TikTok</a></div>
    <div class="card"><p class="label">Coulisses</p><h3>Avant et après combat</h3><p>La pesée, la montée de pression, et ce que chaque combat apprend.</p><a href="{INSTAGRAM}" target="_blank" rel="noopener">Voir sur Instagram</a></div>
    <div class="card"><p class="label">Interview</p><h3>{todo('À venir')}</h3><p>Tidiane raconte son parcours, de Dakar au Havre, dans ses mots.</p></div>
  </div>
</div></section>
<div id="lightbox" class="lightbox" hidden role="dialog" aria-modal="true" aria-label="Photo agrandie"><button class="btn btn-ghost btn-sm close" type="button">Fermer</button><figure><img alt=""><figcaption></figcaption></figure></div>""")

pages["partenaires.html"] = ("Partenaires officiels — Tidiane Diop",
 "Les entreprises qui accompagnent Tidiane Diop : Brothers Kitchen, partenaire officiel nutrition, et Planète Fitness Le Havre.",
 f"""<section class="page-head"><div class="wrap stack">
  <p class="label">Partenaires officiels</p><h1>Ils font avancer le parcours</h1>
  <p class="lead">Des entreprises du Havre qui croient au projet et s’engagent concrètement à ses côtés.</p>
</div></section>
<section class="section" id="brothers-kitchen"><div class="wrap partner">
  <div class="partner-head"><span class="pill on">Partenaire officiel</span><span class="label">Nutrition & restauration</span></div>
  <div class="split">
    <div class="stack">
      <h2>Brothers Kitchen</h2>
      <div class="prose">
        <p>Restaurant street food du Havre, Brothers Kitchen accompagne Tidiane sur un terrain décisif pour un boxeur de 60 kg : l’alimentation. Le restaurant fournit des plats pour la préparation, pensés avec l’encadrement pour soutenir l’entraînement et la gestion du poids.</p>
        <p>Au-delà de l’assiette, c’est un engagement local : une adresse du Havre qui soutient un athlète du Havre, et des moments partagés avec sa clientèle.</p>
      </div>
      <div class="card"><p class="label">Le partenariat en pratique</p><ul><li>Soutien nutritionnel : plats fournis pour la préparation</li><li>Contenus tournés au restaurant</li><li>Mentions et identification sur les réseaux de Tidiane</li><li>Bilan régulier des actions</li></ul></div>
      <p class="source">Détails et rythme du soutien : {todo('à confirmer avec Brothers Kitchen')}</p>
    </div>
    <div class="partner-photos">
      <figure>{pic('bk_equipe', 'Tidiane, poings levés, entre deux représentants de Brothers Kitchen dans le restaurant', '(min-width: 900px) 45vw, 100vw')}<figcaption>Tidiane avec l’équipe de Brothers Kitchen</figcaption></figure>
      <figure>{pic('bk_salle', 'Salle du restaurant Brothers Kitchen, suspension en fibres et mur végétal', '(min-width: 900px) 22vw, 50vw')}<figcaption>La salle</figcaption></figure>
      <figure>{pic('bk_facade', 'Façade du restaurant Brothers Kitchen de nuit, enseigne éclairée', '(min-width: 900px) 22vw, 50vw')}<figcaption>La façade</figcaption></figure>
    </div>
  </div>
</div></section>
<div class="band">{pic('bk_plat', 'Plat de Brothers Kitchen : poulet croustillant, riz, sauce et sésame', '100vw')}<div class="wrap"><p class="label">Brothers Kitchen · au menu de la préparation</p></div></div>
<section class="section alt" id="planete-fitness"><div class="wrap split">
  <div class="stack">
    <div class="partner-head"><img class="logo-disc" src="assets/img/logo_planete_fitness.webp" width="400" height="400" alt="Logo Planète Fitness" loading="lazy"><span class="pill wait">Échanges en cours</span></div>
    <h2>Planète Fitness Le Havre</h2>
    <div class="prose"><p>Une proposition de partenariat a été présentée à la salle Planète Fitness du Havre : accès à la salle et aux services de récupération, et une communication pensée pour ses adhérents et ses partenaires locaux.</p>
    <p class="muted">Aucun accord n’est signé à ce jour. Cette fiche sera mise à jour dès que le partenariat sera confirmé.</p></div>
  </div>
  <div class="card"><p class="label">Pistes à l’étude</p><ul><li>Préparation physique dans la salle</li><li>Contenus tournés sur place</li><li>Séances ouvertes aux adhérents</li></ul></div>
</div></section>
{cta_band('Votre logo à côté du leur', 'Le parcours a encore de la place pour des partenaires engagés : équipement, transport, santé, entreprises.')}""")

TIERS = [
    ("Supporter local", "300 €", "6 mois", "Soutenir une étape du parcours.",
     ["Logo sur la page Partenaires", "1 vidéo de remerciement", "1 mention en story par mois", "Bilan de fin de période"], False),
    ("Partenaire officiel", "1 200 €", "6 mois", "Être associé au quotidien de la préparation.",
     ["Tout le niveau Supporter", "1 vidéo dédiée par mois", "2 stories par mois", "Logo dans le dossier sponsoring", "Bilan trimestriel"], False),
    ("Partenaire saison", "2 000 €", "12 mois", "Accompagner toute une saison sportive.",
     ["1 vidéo dédiée par mois", "4 stories par mois", "Logo sur la tenue d’entraînement", "1 rencontre avec vos équipes ou clients", "Bilan mensuel"], True),
    ("Partenaire majeur", "dès 5 000 €", "12 mois", "Porter le projet aux côtés de Tidiane.",
     ["2 vidéos dédiées par mois", "Visibilité prioritaire sur les supports autorisés", "2 activations dans l’année", "Contenu pour votre communication interne ou RSE", "Exclusivité sectorielle limitée", "Bilan mensuel"], False),
]
def tiers_html():
    out = []
    for name, price, dur, role, items, feat in TIERS:
        lis = "".join(f"<li>{esc(i)}</li>" for i in items)
        out.append(f"""<div class="tier{' feature' if feat else ''}">
  <p class="label">{esc(name)}</p>
  <p class="price">{esc(price)} <small>/ {esc(dur)}</small></p>
  <p class="muted">{esc(role)}</p>
  <ul>{lis}</ul>
  <a class="btn {'btn-primary' if feat else 'btn-ghost'} btn-sm" href="contact.html#{name.split()[-1].lower().replace('major','majeur')}">Choisir ce niveau</a>
</div>""")
    return "\n".join(out)

BENEFITS = [
    ("Des valeurs fortes", "Discipline, persévérance, esprit de famille : votre marque s’associe à un parcours qui les incarne."),
    ("Visibilité digitale", "Mentions, identifications et vidéos dédiées sur Instagram et TikTok."),
    ("Contenus authentiques", "Des vidéos tournées à l’entraînement, en compétition et chez vous, que vous pouvez relayer."),
    ("Présence événementielle", "Votre marque sur les supports autorisés lors des galas et des compétitions."),
    ("Communauté locale", "Un athlète du Havre, suivi par sa ville, ses clubs et ses proches."),
    ("Activations commerciales", "Rencontres, dédicaces, séances ou défis avec vos clients et vos équipes."),
    ("Communication interne et RSE", "Une histoire de persévérance à partager avec vos collaborateurs, selon le projet de votre marque."),
]
pages["devenir-partenaire.html"] = ("Devenir partenaire — Tidiane Diop",
 "Associez votre marque à Tidiane Diop, boxeur 60 kg du Havre en route vers LA28 : bénéfices, niveaux d’engagement et offre sur mesure.",
 f"""<section class="hero"><div class="hero-grid">
  <div class="hero-media">{pic('profil_dore', 'Tidiane de profil, gants aux mains, en lumière dorée', '(min-width: 900px) 50vw, 100vw', eager=True, pos='50% 30%')}</div>
  <div class="wrap hero-copy">
    <p class="label">Devenir partenaire</p>
    <h1 style="font-size:clamp(2.8rem,7vw,5.6rem)">Une ambition à partager</h1>
    <p class="signature">Associez votre marque à une ambition sportive et humaine, du Havre jusqu’à la scène internationale.</p>
    <div class="actions"><a class="btn btn-primary" href="#niveaux">Voir les niveaux</a><a class="btn btn-ghost" href="contact.html">Prendre contact</a></div>
  </div>
</div></section>
<section class="section alt"><div class="wrap stack-lg">
  <div class="stack"><p class="label">Ce que vous y gagnez</p><h2>Sept bonnes raisons</h2></div>
  <div class="grid-3">{''.join(f'<div class="value"><h3>{esc(t)}</h3><p class="muted">{esc(d)}</p></div>' for t, d in BENEFITS)}</div>
</div></section>
<section class="section" id="niveaux"><div class="wrap stack-lg">
  <div class="stack"><p class="label">Niveaux d’engagement</p><h2>Choisir son niveau</h2>
  <p class="muted">Montants et contreparties proposés à titre indicatif, ajustables selon votre projet et le calendrier sportif.</p></div>
  <div class="tiers">{tiers_html()}</div>
  <div class="card" style="border-color:var(--violet)"><p class="label">Construisons une offre sur mesure</p><h3>Un apport en nature, un projet précis ?</h3><p>Équipement, repas, transport, soins, accès à une salle : nous construisons ensemble une collaboration adaptée à votre activité.</p><div class="actions"><a class="btn btn-primary btn-sm" href="contact.html#sur-mesure">Proposer un projet</a><a class="btn btn-ghost btn-sm" href="opportunites.html">Voir les opportunités par secteur</a></div></div>
</div></section>
<section class="section alt"><div class="wrap split">
  <div class="stack"><p class="label">Exemples de livrables</p><h2>Ce que vous recevez</h2>
    <div class="prose"><p>Chaque partenariat commence par un calendrier de contenus validé ensemble. Chaque mois, vous recevez un bilan : publications réalisées, liens, vues, interactions.</p>
    <p class="muted">Nous nous engageons sur des actions précises. Nous ne promettons ni ventes, ni audience garantie, ni résultat sportif.</p></div>
  </div>
  <div class="grid-2">
    <div class="card"><p class="label">Vidéo</p><h3>Une journée avec Tidiane</h3><p>Format court tourné à l’entraînement ou chez vous, publié sur Instagram et TikTok.</p></div>
    <div class="card"><p class="label">Stories</p><h3>Le quotidien</h3><p>Coulisses de la préparation, votre marque identifiée.</p></div>
    <div class="card"><p class="label">Activation</p><h3>Rencontre</h3><p>Séance, dédicace ou échange avec vos équipes ou clients.</p></div>
    <div class="card"><p class="label">Bilan</p><h3>Les preuves</h3><p>Liens, captures datées et chiffres de chaque action.</p></div>
  </div>
</div></section>
{cta_band('Parlons de votre projet', 'Un échange de 30 minutes suffit pour définir la collaboration qui vous ressemble.', ('contact.html', 'Contacter le management'), ('dossier-sponsoring.html', 'Lire le dossier sponsoring'))}""")

SECTORS = [
    ("nutrition", "Nutrition & restauration", "bk_plat",
     "Un boxeur qui combat en 60 kg vit au rythme de son assiette. Restaurants, traiteurs et marques alimentaires y trouvent un terrain naturel.",
     ["Plats ou repas fournis pour la préparation, adaptés avec l’encadrement", "Vidéo « le repas d’avant-séance » tournée chez vous", "Rencontre ou dédicace avec votre clientèle", "Mentions et identification sur les réseaux"],
     ["Une image santé et performance", "Des contenus tournés dans votre établissement", "Une visibilité auprès du public havrais", "Un engagement local concret"],
     "Brothers Kitchen accompagne déjà Tidiane sur ce terrain."),
    ("fitness", "Fitness & performance", "halteres",
     "Les salles de sport et coachs gagnent une preuve vivante : un athlète qui s’entraîne chez eux, au quotidien.",
     ["Accès à la salle et aux cours pour la préparation", "Contenus tournés dans vos espaces", "Séances ouvertes à vos adhérents", "Défis et animations pour votre communauté"],
     ["La démonstration de vos équipements par un sportif", "De l’animation pour vos adhérents", "Des contenus réguliers pour vos réseaux"], ""),
    ("equipement", "Équipement sportif", "sac_couleur",
     "Gants, protections, textile, sacs : un boxeur use son matériel. Votre équipement testé en conditions réelles.",
     ["Dotation en équipement d’entraînement et de compétition", "Vidéos d’usage à l’entraînement", "Logo sur la tenue d’entraînement et d’échauffement", "Retours d’usage sur vos produits"],
     ["Une visibilité produit authentique", "Des contenus de démonstration", "Une association à la discipline et à l’effort"], "Les logos en compétition dépendent des règlements de la fédération et des organisateurs."),
    ("transport", "Transport & mobilité", "ring_public",
     "Chaque compétition hors du Havre demande un déplacement. Votre marque accompagne la route, au sens propre.",
     ["Financement ou prise en charge des déplacements en compétition", "Billets, véhicule ou carburant", "Contenus « en route vers… » avant chaque combat", "Logo sur le sac ou les supports de voyage"],
     ["Une présence à chaque étape du parcours", "Des contenus liés à des moments forts", "Un soutien utile et visible"], ""),
    ("sante", "Santé & récupération", "pushup",
     "Kinésithérapeutes, ostéopathes, préparateurs physiques, nutritionnistes : la récupération fait partie de la performance.",
     ["Suivi kiné, ostéopathie ou préparation physique", "Contenus pédagogiques sur la récupération, avec accord", "Présentation de votre cabinet ou de votre méthode", "Ateliers ou conférences communes"],
     ["Une expertise montrée sur un vrai sportif", "Une visibilité locale ciblée", "Une image de prévention et d’accompagnement"], "Le secret médical s’applique : aucun soin n’est filmé ou commenté sans l’accord de Tidiane et du praticien."),
    ("entreprises", "Entreprises & institutions", "sourire",
     "Entreprises du territoire, collectivités, acteurs de l’emploi : une histoire de persévérance à partager avec vos équipes.",
     ["Intervention ou témoignage auprès de vos collaborateurs", "Séance d’initiation ou de team building", "Contenus pour votre communication interne ou RSE", "Présence lors de vos événements"],
     ["Une histoire inspirante pour vos équipes", "Un engagement visible sur le territoire havrais", "Des contenus pour vos rapports RSE"], ""),
]
for slug, name, img, intro, acts, bens, note in SECTORS:
    pages[f"opportunites-{slug}.html"] = (f"{name} — Partenariats Tidiane Diop",
     f"Partenariat {name.lower()} avec Tidiane Diop, boxeur 60 kg du Havre : activations possibles et bénéfices attendus.",
     f"""<section class="page-head"><div class="wrap split">
  <div class="stack"><p class="label"><a href="opportunites.html">Opportunités</a> · {esc(name)}</p><h1 style="font-size:clamp(2.6rem,7vw,5.2rem)">{esc(name)}</h1><p class="lead">{esc(intro)}</p>
  <div class="actions"><a class="btn btn-primary" href="contact.html#{slug}">Discuter d’un partenariat</a></div></div>
  {pic(img, name, '(min-width: 900px) 45vw, 100vw')}
</div></section>
<section class="section"><div class="wrap grid-2">
  <div class="card"><p class="label">Activations possibles</p><h3>Ce que nous pouvons faire ensemble</h3><ul>{''.join(f'<li>{esc(a)}</li>' for a in acts)}</ul></div>
  <div class="card"><p class="label">Bénéfices attendus</p><h3>Ce que votre marque y gagne</h3><ul>{''.join(f'<li>{esc(b)}</li>' for b in bens)}</ul></div>
</div>
<div class="wrap" style="margin-top:20px"><p class="muted">{esc(note)} Nous nous engageons sur des actions, pas sur des ventes ni sur une audience garantie.</p></div></section>
{cta_band('Construisons votre activation', 'Dites-nous ce que vous voulez accomplir : nous proposons un format et un calendrier.', ('contact.html#' + slug, 'Nous contacter'), ('devenir-partenaire.html#niveaux', 'Voir les niveaux'))}""")

pages["opportunites.html"] = ("Opportunités de partenariat — Tidiane Diop",
 "Six secteurs, six façons de soutenir Tidiane Diop : nutrition, fitness, équipement, transport, santé, entreprises.",
 f"""<section class="page-head"><div class="wrap stack">
  <p class="label">Opportunités de partenariat</p><h1>Votre secteur, votre activation</h1>
  <p class="lead">Chaque activité a sa place dans le parcours. Choisissez la vôtre pour voir les activations possibles.</p>
</div></section>
<section class="section"><div class="wrap grid-3">
{''.join(f'<a class="card" href="opportunites-{s}.html" style="text-decoration:none;color:inherit">{pic(i, n, "(min-width: 1000px) 30vw, (min-width: 640px) 45vw, 100vw")}<h3>{esc(n)}</h3><p>{esc(t)}</p><span class="label">Voir les activations</span></a>' for s, n, i, t, *_ in SECTORS)}
</div></section>
{cta_band('Un autre secteur ?', 'Nous construisons aussi des offres sur mesure.', ('contact.html#sur-mesure', 'Proposer un projet'), ('devenir-partenaire.html', 'Devenir partenaire'))}""")

pages["dossier-sponsoring.html"] = ("Dossier sponsoring — Tidiane Diop",
 "Le dossier sponsoring de Tidiane Diop : présentation, vision, parcours, palmarès, audience, calendrier, offres et contact.",
 f"""<section class="page-head"><div class="wrap stack">
  <p class="label">Dossier sponsoring · Saison 2026</p><h1>Tidiane Diop × votre marque</h1>
  <p class="lead">Tout ce qu’une entreprise doit savoir avant un premier échange.</p>
  <div class="actions"><a class="btn btn-primary" href="assets/dossier-sponsoring-tidiane-diop.pdf" download>Télécharger le PDF</a><a class="btn btn-ghost" href="contact.html">Contacter le management</a></div>
</div></section>
<section class="section"><div class="wrap split">
  <div class="stack"><p class="label">Présentation</p><h2>Tidiane Diop</h2><div class="prose"><p>Boxeur amateur, catégorie 60 kg, basé au Havre. Parti de Dakar, accueilli au Havre par son cousin Saliou, il construit son parcours avec une méthode : PROCESS.</p></div>
  <p class="label">Vision sportive</p><div class="prose"><p>Viser les Jeux de Los Angeles 2028, étape par étape : régional, national, international, puis le parcours de qualification applicable. Un objectif, pas une qualification acquise.</p></div></div>
  {pic('portrait_nb', 'Portrait de Tidiane Diop', '(min-width: 900px) 45vw, 100vw')}
</div></section>
<section class="section alt"><div class="wrap stack-lg">
  <div class="grid-2">
    <div class="stack"><p class="label">Palmarès vérifié</p><h3>Vice-champion de Normandie · 60 kg</h3><p class="muted">Saison 2025 · justificatif officiel disponible sur demande.</p></div>
    <div class="stack"><p class="label">Calendrier prévisionnel</p><h3>Saison 2026–2027</h3><p class="muted">Championnat de Normandie Élite (novembre–décembre 2026), Championnats de France amateurs seniors (janvier 2027), Coupe de France seniors (juin 2027), selon engagement et résultats.</p></div>
  </div>
  <div class="stack"><p class="label">Audience et statistiques réelles</p>{STATS}</div>
</div></section>
<section class="section"><div class="wrap stack-lg">
  <div class="stack"><p class="label">Offres de partenariat</p><h2>Quatre niveaux</h2></div>
  <div class="table-wrap"><table><thead><tr><th>Niveau</th><th>Montant</th><th>Durée</th><th>Principales contreparties</th></tr></thead><tbody>
  {''.join(f'<tr><td><b>{esc(n)}</b></td><td>{esc(p)}</td><td>{esc(d)}</td><td>{esc(", ".join(i[:3]))}</td></tr>' for n, p, d, r, i, f in TIERS)}
  </tbody></table></div>
  <p class="muted">Montants indicatifs, ajustables. Offre sur mesure possible, y compris en nature.</p>
  <div class="grid-2">
    <div class="stack"><p class="label">Exemples de livrables</p><p>Vidéos dédiées, stories, logo sur la tenue d’entraînement, rencontres avec vos équipes, bilan mensuel avec preuves.</p></div>
    <div class="stack"><p class="label">Partenaires existants</p><p>Brothers Kitchen, partenaire officiel nutrition. Planète Fitness Le Havre : échanges en cours.</p></div>
  </div>
</div></section>
<section class="section alt"><div class="wrap stack">
  <p class="label">Contact management</p><h2>{MANAGER}</h2>
  <div class="copy-row"><code>{PHONE}</code><button class="btn btn-ghost btn-sm" type="button" data-copy="{PHONE}">Copier le numéro</button></div>
  <p class="muted">Ou via le <a href="contact.html">formulaire de contact</a>.</p>
</div></section>""")

pages["contact.html"] = ("Contact — Tidiane Diop",
 "Contacter le management de Tidiane Diop pour un partenariat, une demande média ou un événement.",
 f"""<section class="page-head"><div class="wrap stack">
  <p class="label">Contact</p><h1>Parlons partenariat</h1>
  <p class="lead">Quelques informations suffisent pour que le management vous propose un format adapté.</p>
</div></section>
<section class="section"><div class="wrap split">
  <form id="contact-form" class="form" novalidate>
    <div class="grid-2">
      <div class="field"><label for="f-entreprise">Entreprise <span class="req">*</span></label><input id="f-entreprise" name="entreprise" required autocomplete="organization"></div>
      <div class="field"><label for="f-secteur">Secteur <span class="req">*</span></label><select id="f-secteur" name="secteur" required><option value="">Choisir</option><option>Nutrition & restauration</option><option>Fitness & performance</option><option>Équipement sportif</option><option>Transport & mobilité</option><option>Santé & récupération</option><option>Entreprise ou institution</option><option>Média</option><option>Autre</option></select></div>
      <div class="field"><label for="f-nom">Nom <span class="req">*</span></label><input id="f-nom" name="nom" required autocomplete="name"></div>
      <div class="field"><label for="f-fonction">Fonction</label><input id="f-fonction" name="fonction" autocomplete="organization-title"></div>
    </div>
    <div class="field"><label for="f-email">Email professionnel <span class="req">*</span></label><input id="f-email" name="email" type="email" required autocomplete="email"></div>
    <div class="grid-2">
      <div class="field"><label for="f-type">Type de partenariat <span class="req">*</span></label><select id="f-type" name="type" required><option value="">Choisir</option><option value="local">Supporter local</option><option value="officiel">Partenaire officiel</option><option value="saison">Partenaire saison</option><option value="majeur">Partenaire majeur</option><option value="sur-mesure">Offre sur mesure</option><option value="nutrition">Nutrition & restauration</option><option value="fitness">Fitness & performance</option><option value="equipement">Équipement sportif</option><option value="transport">Transport & mobilité</option><option value="sante">Santé & récupération</option><option value="entreprises">Entreprises & institutions</option><option value="media">Demande média</option></select></div>
      <div class="field"><label for="f-budget">Budget envisagé <span class="hint">(facultatif)</span></label><select id="f-budget" name="budget"><option value="">Je ne sais pas encore</option><option>Moins de 500 €</option><option>500 à 1 500 €</option><option>1 500 à 5 000 €</option><option>Plus de 5 000 €</option><option>Apport en nature</option></select></div>
    </div>
    <div class="field"><label for="f-message">Message <span class="req">*</span></label><textarea id="f-message" name="message" required placeholder="Votre activité, ce que vous souhaitez accomplir, vos délais."></textarea></div>
    <div class="hp" aria-hidden="true"><label for="f-website">Ne pas remplir</label><input id="f-website" name="website" tabindex="-1" autocomplete="off"></div>
    <label class="check" for="f-consent"><input id="f-consent" name="consent" type="checkbox" required><span id="consent-text">J’accepte que mes données soient utilisées par le management de Tidiane Diop pour répondre à ma demande et me recontacter au sujet d’un partenariat. Elles sont conservées 3 ans au plus et ne sont jamais revendues. Détails dans les <a href="mentions-legales.html#donnees">mentions légales</a>.</span></label>
    <div><button class="btn btn-primary" type="submit">Envoyer la demande</button></div>
    <p id="form-status" class="notice" tabindex="-1" hidden role="status"></p>
  </form>
  <aside class="stack">
    <div class="card"><p class="label">Management</p><h3>{MANAGER}</h3><div class="copy-row"><code>{PHONE}</code><button class="btn btn-ghost btn-sm" type="button" data-copy="{PHONE}">Copier</button></div><p class="muted">Réponse sous 72 heures ouvrées.</p></div>
    <div class="card"><p class="label">Réseaux</p><p><a href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram @tidiboy29</a><br><a href="{TIKTOK}" target="_blank" rel="noopener">TikTok @tidiboy29</a></p></div>
    {pic('road_duo', 'Tidiane souriant en tenue de club', '(min-width: 900px) 40vw, 100vw')}
  </aside>
</div></section>""")

pages["mentions-legales.html"] = ("Mentions légales — Tidiane Diop",
 "Mentions légales, données personnelles et cookies du site de Tidiane Diop.",
 f"""<section class="page-head"><div class="wrap stack"><p class="label">Informations légales</p><h1>Mentions légales</h1></div></section>
<section class="section"><div class="wrap prose">
  <h2 style="font-size:2rem">Éditeur du site</h2>
  <p>{todo('Nom ou raison sociale, forme juridique, SIREN, adresse')}<br>Directeur de la publication : {todo('nom')}<br>Contact : {MANAGER}, {PHONE}</p>
  <h2 style="font-size:2rem">Hébergement</h2>
  <p>{todo('Nom de l’hébergeur, adresse, téléphone')}</p>
  <h2 style="font-size:2rem">Propriété intellectuelle</h2>
  <p>Les textes, photos et vidéos de ce site sont protégés. Les photographies restent la propriété de leurs auteurs ({todo('crédits à compléter')}). Les logos des partenaires sont reproduits avec leur accord. Toute reproduction nécessite une autorisation écrite.</p>
  <h2 style="font-size:2rem" id="donnees">Données personnelles</h2>
  <p><b>Responsable du traitement :</b> {todo('éditeur du site')}.</p>
  <p><b>Données collectées :</b> celles saisies dans le formulaire de contact (entreprise, secteur, nom, fonction, email, type de partenariat, budget facultatif, message).</p>
  <p><b>Finalité et base légale :</b> répondre à votre demande et gérer la relation avec les prospects et partenaires, sur la base de votre consentement.</p>
  <p><b>Destinataires :</b> le management de Tidiane Diop et son outil de gestion de la relation client ({todo('nom du CRM et localisation des données')}). Aucune revente.</p>
  <p><b>Durée de conservation :</b> 3 ans au plus après le dernier contact.</p>
  <p><b>Vos droits :</b> accès, rectification, effacement, opposition, limitation et portabilité, en contactant {todo('adresse email dédiée')}. Vous pouvez saisir la CNIL (cnil.fr).</p>
  <h2 style="font-size:2rem">Cookies</h2>
  <p>Ce site ne dépose aucun cookie publicitaire ni de mesure d’audience. Les polices sont hébergées sur le site lui-même : aucune donnée n’est transmise à un service tiers à l’affichage des pages. Si un outil de mesure est ajouté, un bandeau de consentement sera mis en place avant tout dépôt.</p>
</div></section>""")

# ---------------------------------------------------------------- écriture
def build(target, index_bare=False):
    os.makedirs(target, exist_ok=True)
    for slug, (title, desc, body, *ld) in pages.items():
        bare = index_bare and slug == "index.html"
        doc = page(slug, title, desc, body, jsonld=(ld[0] if ld else None), full_doc=not bare)
        open(os.path.join(target, slug), "w", encoding="utf-8").write(doc)
    urls = "".join(f"<url><loc>{SITE_URL}/{'' if s == 'index.html' else s}</loc></url>" for s in pages)
    open(os.path.join(target, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(os.path.join(target, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")

if __name__ == "__main__":
    build(DIST)
    if len(sys.argv) > 1:
        build(sys.argv[1], index_bare=True)
    print("ok", len(pages), "pages")
