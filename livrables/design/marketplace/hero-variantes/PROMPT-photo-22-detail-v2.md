# Photo 22 — amélioration des détails

Outil : image_gen intégré. Source : `22-degustation-fromager-rue-vivante.png`.

Sortie : `22-degustation-fromager-rue-vivante-detail-v2.png` et export WebP à qualité 0,94. La composition est conservée dans son ensemble ; les détails sont reconstruits par IA. La résolution demandée était de 3840 × 1920, mais la sortie réelle reste de 1774 × 887 pixels. Il s’agit d’une amélioration de netteté, pas d’une augmentation de la définition native.

## Prompt final

```text
Use case: identity-preserve.
Input image: EDIT TARGET, the selected Localeo photo 22. Improve resolution and fine photographic detail of this EXACT photo, not a new interpretation.
Output target: 3840 × 1920 pixels, 2:1 landscape, highest available native resolution.
Perform faithful high-resolution restoration / super-resolution: resolve natural skin and hair detail, fabric weave, cheese rind and crumb texture, wood grain, foliage and limestone masonry, and the distant storefronts and pedestrians. Restrained natural microcontrast, optically credible detail, no oversharpening, halos, waxy faces, painterly texture or artificial HDR.
Strict invariants: preserve the original exact framing, camera angle, perspective, composition, positions and number of all people, the identities and expressions of the three main people, skin tones, age, clothing, body language, every hand gesture, the tasting action, cheese board, table, phone, buildings, awnings, shopfronts, signs, market stalls, trees and street. Preserve the original warm daylight, shadows, exposure and colors. Keep the busy French village street inspired by Latresne, and the cheesemonger guiding her two guests on the right. Preserve all readable lettering as it is, especially "Localeo" on the phone. Do not add, remove or rearrange anything. Do not crop or extend the image. No border, no watermark, no overlay.
Return only the faithfully enhanced photograph at 3840 × 1920 pixels if supported.
```
