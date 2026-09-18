# Hero d’accueil — rue contemporaine et expériences locales

## Intention

Devantures actuelles, rue plus passante et découverte chez un commerçant : le coffret Localeo évoque des expériences et des rencontres locales. Une dégustation chez un chocolatier remplace la remise d’un achat de pain. Grandes vitrines, cadres fins et enseignes sobres modernisent les commerces. Piétons, échanges et terrasse de café animent la rue. La diversité des habitants et des générations est conservée, sans signes religieux.

Texte, actions et animations du hero conservés. Le cadrage mobile garde la rencontre à droite.

La règle qui masquait le visuel sur mobile est surchargée par `display: block`. Vérification visuelle sur ordinateur (1440 × 1000) et mobile (390 × 844) : bonne image chargée, photo visible, aucun débordement horizontal. Build de production validé.

## Visuels

Image synthétique retravaillée avec l’outil intégré `image_gen`, puis redimensionnée et encodée en WebP. Il ne s’agit pas d’une photographie d’un commerce partenaire réel.

- Source : `output/hero-variantes/19-rue-contemporaine-experiences.png`.
- Ordinateur : `public/img/hero-centre-bourg-v32-1774.webp` (1774 × 887).
- Version réduite : `public/img/hero-centre-bourg-v32-960.webp` (960 × 480).
- Anciennes variantes conservées, y compris `hero-decouverte-v32`.

## Prompt final

```text
Use case: precise-object-edit.
Asset type: Localeo homepage hero photograph, wide 2:1 landscape.
Edit target: supplied existing homepage photo. Keep the same human-scale French town street perspective, warm natural daylight, photographic realism, diverse contemporary residents and main encounter in the right third. Preserve a relatively calm left foreground for HTML text, while the street in the middle distance is visibly busy.
Primary request: substantially modernize ALL retail storefronts, make the street much more frequented, and replace the central baguette purchase with a welcoming local discovery experience.
Storefronts: current-day renovated independent shops, large clear windows, slim powder-coated metal frames, smooth cream fascias, understated small lowercase sans-serif lettering, pale oak interior details, level accessible entrances and simple contemporary furniture. Keep two-storey town buildings but refresh facades; no nostalgic gold serif signage, rustic chalkboards, ornate wood panels, heavy old awnings or tourist-village aesthetic.
Main scene: the Black male merchant and female visitor on the right now share a small chocolate tasting at the open entrance of a contemporary artisan chocolate shop. Merchant wears a clean navy apron and offers a small ceramic tasting tray with a few chocolates. Visitor is discovering and discussing the tasting, with a natural interested smile, hands anatomically plausible and separated. No baguette, no bread shelves, no shopping bag handover, no physical gift hamper or giant product. The encounter and experience are the focus. In the glass window behind them, restrained chocolate displays and a small working counter. Small correctly spelled sign: "chocolat".
Street life: about 16–20 naturally distributed people across foreground, middle distance and background, several clearly visible moving pedestrians, two friends greeting, a parent walking with a child, one person pushing a bicycle, café customers and a server. A busy walkable shopping street with convincing depth and spontaneous everyday activity, not a lined-up crowd. Neighbouring modern café terrace and independent shops suggest varied local experiences. Cosmopolitan mix of skin tones, ages and hair textures in everyday contemporary casual clothes, no religious symbols or religious attire. No church or bell tower.
Composition: main encounter fully visible in rightmost third with safe head margins for mobile crop; lively pedestrian flows recede through central street, lower left foreground remains visually calm. No person looks at camera. Authentic accessible neighborhood, not a luxury shopping mall. Warm editorial lifestyle photography, natural skin and proportions. One continuous photograph, no montage, no UI, no slogan, no watermark. Output only the edited photo.
```
