# Hero d’accueil — prestation Localeo vécue

Le visuel met au premier plan une cliente savourant une dégustation guidée de chocolats. L’artisan accompagne ce moment ; l’assiette de dégustation et le pass Localeo sur le téléphone rendent l’expérience concrète. La rue commerçante contemporaine reste en arrière-plan.

Image synthétique retravaillée avec l’outil intégré `image_gen`, puis redimensionnée et encodée en WebP. Elle ne représente pas un partenaire réel.

- Source : `output/hero-variantes/20-prestation-degustation-localeo.png`.
- Ordinateur : `public/img/hero-prestation-v33-1774.webp`.
- Version réduite : `public/img/hero-prestation-v33-960.webp`.
- Description accessible actualisée dans `src/pages/AccueilPage.jsx`.
- Vérification du chargement des deux images et de l’absence de débordement horizontal à 1440 et 390 pixels.

## Prompt final

```text
Use case: precise-object-edit.
Asset type: photorealistic Localeo homepage hero, wide landscape 2:1.
Input image: edit target, current homepage photograph.
Primary request: emphasize a customer actively enjoying a Localeo service. Transform the foreground encounter into an unmistakable guided artisan chocolate tasting experience, with the pleasure of consuming the experience as the main subject.
Preserve the contemporary independent chocolate shop, warm natural daylight, French human-scale shopping street, cosmopolitan everyday residents in background and photographic realism. The street is supporting context, the experience is the visual priority.
In the RIGHT THIRD show the same middle-aged woman comfortably seated at a small contemporary pale-oak tasting counter at the open shop frontage. She is actually tasting a small chocolate, holding a visibly bitten piece just beside her lips, with a relaxed delighted natural expression, looking toward the same friendly Black male chocolatier in a navy apron beside her. He guides her tasting with a natural open-hand gesture toward a clearly visible ceramic tasting plate with four different chocolates, a halved praline revealing its filling, a small cup and a water glass. Their faces, her tasting gesture and the plate are visually prominent and close together. Medium shot, human proportions, fully visible heads, anatomically natural separate hands. This should look like an enjoyable hosted activity with time spent together, not a free sample handed out on the pavement.
On the tasting counter near the plate, a discreet smartphone displays a simple cream and navy digital experience pass with ONLY the accurately spelled brand "Localeo" and a small orange checkmark. Screen is subtly readable, secondary to the human experience, with no tiny illegible text. No physical gift box, no shopping bags, no cash register or payment scene.
Composition: retain the calm left 45 percent with the receding street for existing HTML text overlay. Place both main faces and the tasting activity within x=62 to 88 percent of the frame, y=20 to 72 percent, so a portrait crop on the right retains both people and the plate. Customer's body turned three-quarter toward camera but eyes toward artisan, artisan behind and to right of counter. Background street pedestrians and modern cafes softly out of focus. Do not look at camera. Keep small chocolate shop sign "chocolat". No added overlay text, watermark or UI outside the phone. Natural skin texture and candid editorial photography, no advertising pose, no exaggerated smile. Output only the edited photograph.
```
