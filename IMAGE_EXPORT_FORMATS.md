# IMAGE EXPORT FORMATS · DEFINITION

Streetcraft remains a visual system. Export is a post-generation production layer and must not modify scene identity, camera, profile or composition.

## Approved physical formats

### A4 Landscape
Physical size: 297 × 210 mm
Orientation: landscape

Approved raster targets:
- 150 dpi: 1754 × 1240 px
- 300 dpi: 3508 × 2480 px

Default recommendation: 300 dpi when the source has enough real detail.
150 dpi remains valid when avoiding artificial upscaling is preferable.

### A3 Landscape
Physical size: 420 × 297 mm
Orientation: landscape

Approved raster targets:
- 150 dpi: 2480 × 1754 px
- 300 dpi: 4961 × 3508 px

Default recommendation: 300 dpi when the source has enough real detail.
150 dpi remains valid when source resolution is limiting.

### Large Backdrop 90 × 45 cm
Physical size: 900 × 450 mm
Orientation: landscape
Approved resolution: 150 dpi ONLY
Raster target: 5315 × 2657 px

300 dpi for 90 × 45 cm is explicitly excluded from the current roadmap.

## Export principle

DPI metadata alone does not create detail.
Export Runtime must distinguish:
- native detail;
- legitimate resampling;
- AI/algorithmic upscale;
- invented visual detail.

Upscaling may increase printable pixel dimensions, but must not silently rewrite architecture, signage, surface identity or protected relationships.

## Required future export checks
- target physical size
- target dpi
- target pixel dimensions
- source effective resolution
- scale factor
- aspect-ratio/crop decision
- sharpening/resampling method
- identity-preservation check after upscale
