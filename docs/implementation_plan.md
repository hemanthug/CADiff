# Implementation Plan

## Phase 1 (done in this MVP scaffold)
1. Build backend API contract and schema for compare report.
2. Implement STEP parsing, topology extraction, and mass properties.
3. Implement baseline COM alignment and transform reporting.
4. Implement boolean add/remove volume diff and classify into structured change objects.
5. Build frontend workflow (upload -> settings -> compare -> report + viewer).

## Phase 2
1. Add robust region segmentation from boolean result solids.
2. Introduce feature correspondence graph (hole/boss/slot/etc).
3. Implement click-to-zoom integration between change list and viewer camera.
4. Add CSV/PDF export endpoints and UI actions.

## Phase 3
1. Improve alignment with PCA + ICP refinement.
2. Add tolerance-adaptive noise filtering and confidence tuning.
3. Performance optimization (meshing cache, async jobs).
4. Extend to assemblies and native CAD conversion pipeline.
