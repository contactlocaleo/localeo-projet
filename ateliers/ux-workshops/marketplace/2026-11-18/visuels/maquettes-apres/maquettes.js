/* Maquettes documentaires uniquement. Aucun formulaire ni lien de paiement actif. */
const bar = '<header class="bar"><div class="brand"><i class="mark"></i>Localeo Coffrets<small>Des expériences près de vous</small></div><span class="menu" aria-hidden="true">☰ Menu</span></header>';
const title = {
  'O-01':'Accueil · proposition de valeur',
  'O-02':'Fiche coffret · promesse',
  'O-03':'Cadeau · étapes avant achat',
  'O-05':'Fiche commerçant · contenu',
  'O-06':'Animations · passage vers Live',
  'O-07':'Récapitulatif · conditions',
  'O-08':'Frontière Stripe · carte de recette'
};
const views = {
  'O-01': [
    '<div class="hero"><div class="eyebrow">Découvrir Localeo</div><h1>Un parcours d’expériences chez les commerçants d’ici.</h1>',
    '<p class="lead">À vivre dans une commune, à offrir sous forme de coffret numérique.</p>',
    '<label class="label">Trouver une commune, une adresse ou un coffret<input class="field" placeholder="Ex. Bouliac, balade…" disabled></label>',
    '<span class="btn">Rechercher les coffrets et les adresses</span><p style="margin:15px 0 0"><span class="darklink">Voir les animations de ma commune →</span></p></div>',
    '<section class="section"><div class="eyebrow">Choisir une commune</div><h2>La découverte commence ici</h2>',
    '<p class="small">Bouliac, Cavaignac-en-Bordes, Cenac et Latresne.</p><div class="line row"><strong>Bouliac</strong><span>Découvrir →</span></div>',
    '<div class="line row"><strong>Latresne</strong><span>Découvrir →</span></div></section>',
    '<section class="banner"><div class="eyebrow">Un coffret à découvrir</div><h2>À table, puis en balade</h2>',
    '<p>Un déjeuner et une balade à vélo, auprès de deux adresses locales.</p><div class="price">59,90 €</div><span class="btn">Voir le coffret</span></section>'
  ].join(''),
  'O-02': [
    '<div class="crumb">Accueil / Latresne / À table, puis en balade</div>',
    '<div class="photo" style="height:210px"></div>',
    '<section class="pad"><div class="eyebrow">Un parcours à vivre à Latresne</div><h1>À table, puis en balade</h1>',
    '<p class="lead">Un déjeuner, puis deux heures de vélo : deux moments chez des commerçants locaux.</p>',
    '<div class="row"><strong class="price">59,90 €</strong><span class="small">90 jours après activation</span></div>',
    '<div class="promise"><h3>Ce que le coffret garantit</h3><p>Un déjeuner entrée, plat et dessert pour une personne, hors boissons, et une location de vélo de ville adulte de deux heures.</p>',
    '<p class="small">Selon les modalités détaillées du coffret ; réservation auprès des adresses concernées.</p></div>',
    '<h3>Exemples de moments possibles</h3><p>Les expériences ci-dessous illustrent le parcours. Leur choix et leur disponibilité dépendent des commerces et des conditions du coffret.</p>',
    '<div class="line"><strong>Déjeuner local</strong><p class="small">Un moment à table chez une adresse partenaire.</p></div>',
    '<div class="line"><strong>Balade à vélo</strong><p class="small">Deux heures pour découvrir la commune autrement.</p></div>',
    '<span class="btn">Voir les modalités et acheter</span></section>'
  ].join(''),
  'O-03': [
    '<div class="crumb">Accueil / Latresne / À table, puis en balade</div>',
    '<section class="pad"><div class="eyebrow">Offrir un parcours local</div><h1>Un cadeau à vivre, pas un colis.</h1>',
    '<p class="lead">À table, puis en balade · 59,90 €</p>',
    '<div class="step"><span class="num">1</span><div><strong>Vous achetez le coffret</strong><p class="small">Le récapitulatif et les conditions restent visibles avant le paiement.</p></div></div>',
    '<div class="step"><span class="num">2</span><div><strong>Vous le recevez par e-mail</strong><p class="small">Après confirmation du paiement, le coffret numérique arrive à l’adresse indiquée.</p></div></div>',
    '<div class="step"><span class="num">3</span><div><strong>Vous préparez la carte cadeau</strong><p class="small">Vous pouvez ensuite transmettre le cadeau à votre proche.</p></div></div>',
    '<div class="step"><span class="num">4</span><div><strong>Votre proche active et profite du parcours</strong><p class="small">Validité de 90 jours après activation ; réservation selon les adresses.</p></div></div>',
    '<div class="promise"><label class="label">Votre adresse e-mail de réception<input class="field" placeholder="vous@exemple.fr" disabled></label>',
    '<label class="label">Téléphone de contact obligatoire<input class="field" placeholder="06 12 34 56 78" disabled></label>',
    '<p class="small">Utilisé pour le suivi de la commande et de son envoi, selon les informations de la fiche actuelle.</p></div>',
    '<span class="btn">Acheter ce coffret · 59,90 €</span><p class="small" style="margin-top:12px">Bouton inactif dans cette maquette.</p></section>'
  ].join(''),
  'O-05': [
    '<div class="crumb">Accueil / Bouliac / Café des Promeneurs</div>',
    '<div class="photo" style="height:300px"></div>',
    '<section class="pad"><div class="eyebrow">Adresse Localeo · Bouliac</div><h1>Café des Promeneurs</h1>',
    '<p class="lead">Pause après la balade.</p><p>Une adresse partenaire du parcours « Une promenade fleurie ».</p>',
    '<div class="split"><div class="mini"><strong>Bouliac</strong><p class="small">Commune</p></div><div class="mini"><strong>1 coffret</strong><p class="small">À découvrir</p></div></div>',
    '<div class="promise"><h3>Son savoir-faire dans le parcours</h3><p>Une pause café ou une composition végétale, selon la sélection du jour et les conditions du coffret associé.</p>',
    '<p class="small">Contenu et prestation à faire confirmer par le partenaire avant publication.</p></div>',
    '<span class="btn">Voir le coffret associé</span><p style="margin-top:15px"><span class="link">Découvrir Bouliac →</span></p></section>',
    '<section class="section"><div class="eyebrow">Coffret associé</div><h2>Une promenade fleurie</h2><p>Deux exemples d’expériences · Validité 90 jours.</p><strong class="price">59,90 €</strong></section>'
  ].join(''),
  'O-06': [
    '<div class="crumb">Accueil / Bouliac / Animations</div>',
    '<section class="pad"><div class="eyebrow">Agenda de Bouliac</div><h1>À vivre dans la commune</h1>',
    '<p class="small">Consultez ici les dates. Le détail et la participation se poursuivent sur Localeo Live.</p>',
    '<div class="tabs"><span class="tab selected">En ce moment · 2</span><span class="tab">À venir · 2</span></div>',
    '<article class="event"><div class="date">18–21 novembre 2026 · En cours</div><h3>Test jeu des vitrines</h3>',
    '<p>Découvrez les commerces participants et les règles du jeu.</p><span class="btn">Voir l’animation sur Localeo Live →</span></article>',
    '<article class="event"><div class="date">15–22 novembre 2026 · En cours</div><h3>Test juste prix Local</h3>',
    '<p>Une animation chez les commerçants de Bouliac.</p><span class="btn">Voir l’animation sur Localeo Live →</span></article></section>',
    '<div class="banner"><div class="eyebrow">Après le clic · Localeo Live</div><h2>Vous restez sur Bouliac</h2>',
    '<p>Vous y trouverez les conditions, les commerces et l’action pour participer.</p>',
    '<div class="line"><strong>Test juste prix Local</strong><p class="small" style="color:#d3e3e9">En cours · Bouliac · jusqu’au 22 novembre</p></div>',
    '<span class="btn" style="background:#08786f;color:white">Voir le détail de l’animation</span>',
    '<p class="small" style="color:#d3e3e9;margin-top:12px">L’action pour participer se trouve sur la page de détail Live.</p>',
    '<p style="margin:17px 0 0"><span class="darklink">← Retour à la commune Bouliac</span></p></div>'
  ].join(''),
  'O-07': [
    '<div class="crumb">Accueil / Latresne / À table, puis en balade</div>',
    '<section class="pad"><div class="eyebrow">Avant de payer</div><h1>Votre coffret en un regard</h1>',
    '<div class="line row"><div><strong>À table, puis en balade</strong><p class="small">1 coffret numérique · Latresne</p></div><strong>59,90 €</strong></div>',
    '<div class="line row"><strong>Total à payer</strong><strong class="price">59,90 €</strong></div>',
    '<div class="promise"><h3>À savoir avant de continuer</h3>',
    '<div class="check">Valable 90 jours après activation.</div>',
    '<div class="check">Réservation auprès des adresses partenaires.</div>',
    '<div class="check">Les prestations illustrées restent indicatives ; la promesse garantie figure sur la fiche.</div>',
    '<div class="check">Coffret reçu par e-mail après confirmation du paiement.</div></div>',
    '<p class="small">Consultez les <span class="link">conditions générales de vente</span> et la <span class="link">politique de confidentialité</span> avant de poursuivre.</p>',
    '<span class="btn">Acheter ce coffret · 59,90 €</span>',
    '<p class="small" style="margin-top:14px">Cette maquette documentaire ne déclenche aucune commande.</p></section>'
  ].join(''),
  'O-08': [
    '<div class="crumb">Dossier de recette / O-08</div>',
    '<section class="pad"><div class="eyebrow">Carte de contrôle · pas un écran produit</div><h1>La frontière avant Stripe</h1>',
    '<p class="lead">Ce parcours reste à vérifier dans un cadre de test autorisé.</p>',
    '<div class="flow"><div class="flowitem"><strong>1 · Fiche et récapitulatif</strong><p class="small">Observés sur le site TEST. Aucun formulaire soumis.</p></div>',
    '<div class="flowitem"><strong>2 · Initialisation de paiement</strong><p class="small">Déduit du code : crée un achat et une session avant la redirection.</p></div>',
    '<div class="flowitem unknown"><strong>3 · Page Stripe</strong><p class="small">Non observée. Ne pas la représenter comme un écran réel.</p></div>',
    '<div class="flowitem unknown"><strong>4 · Retour et état de commande</strong><p class="small">Non observés. À inclure dans la recette sûre.</p></div></div>',
    '<div class="promise"><h3>Preuves à obtenir avant ouverture large</h3>',
    '<div class="check">Effets métier de la session TEST validés comme innocuits.</div>',
    '<div class="check">Redirection, erreur et retour contrôlés.</div>',
    '<div class="check">Aucun paiement ni donnée bancaire réelle.</div></div>',
    '<span class="btn" style="background:#9aadb6;color:#123149">Soumission désactivée dans cette maquette</span></section>'
  ].join('')
};
const id=document.body.dataset.orientation;
document.title=(title[id]||'Maquette')+' — Localeo';
document.getElementById('app').innerHTML='<div class="mock">'+bar+(views[id]||'<p>Orientation inconnue.</p>')+'</div>';
