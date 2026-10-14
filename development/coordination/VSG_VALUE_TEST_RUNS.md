# Corridas de la prueba de valor A/B de VSG

Estado: **PREPARADAS / GENERACIÓN NO INICIADA**.

Cada comando imprime en stdout la rama canónica completa como JSON compacto. En
una sesión nueva de ChatGPT por corrida, adjuntar la fuente indicada y pegar la
salida exacta del comando, sin edición semántica. Conservar la primera imagen
válida, sin reintentos selectivos, con el nombre neutral indicado.

## Fuentes y contratos confirmados

| Caso | Fuente a adjuntar | SHA-256 | Contrato vinculado |
| --- | --- | --- | --- |
| D | `benchmark/r2b_1_9_1/evidence_2026_09_21/R2B-191-D_source.jpg` | `282ddf02a476851fa231accfceebd3b83d5d7d5ae72e6a5153097b4081d368fc` | `visual_scene_graph/pilot/fixtures/r2b_d_new_01/contract.json` |
| E | `benchmark/r2b_1_9_1/evidence_2026_09_21/R2B-191-E_source.jpg` | `f0ba6e1f5bb5e3f40f39c0847f3d980e25c8c110b15b932cb1b3a10984a62860` | `visual_scene_graph/pilot/fixtures/r2b_e_new_01/contract.json` |
| Kenny's Shop | `visual_scene_graph/pilot/fixtures/kennys/source/kennys-shop.jpg` | `45b8bff5c33ea411ffef3c88db99d757ce462a7f13b56df3f2fbc62b994357b2` | `visual_scene_graph/pilot/fixtures/kennys_new_01/contract.json` |

Los manifests de dry run vinculan cada fuente, contrato y payload. Los hashes
de las seis ramas extraídas coinciden con el manifiesto de campaña.

Las "seis fuentes candidatas" A–F son un conjunto aparte: pertenecen al carril
de aporte de SC de 12 salidas y siguen `UNKNOWN_PENDING_LEAN_CONFIRMATION`. No
son estas tres fuentes ni las seis corridas de la prueba de valor VSG.

## Orden congelado

Semilla aleatoria: `adbe972f90f746031ac341c25146db96`. El orden se obtuvo
ordenando por SHA-256 de `semilla:caso-condición` y queda congelado aquí.

1. **IMG_0001** — adjuntar `benchmark/r2b_1_9_1/evidence_2026_09_21/R2B-191-D_source.jpg`  
   Comando exacto: `jq -c '.B' validation/vsg_2b/dry_runs/ed04d917-c5d3-4fe3-b6de-62c13f532f7f/payloads.json`
2. **IMG_0002** — adjuntar `benchmark/r2b_1_9_1/evidence_2026_09_21/R2B-191-E_source.jpg`  
   Comando exacto: `jq -c '.B' validation/vsg_2b/dry_runs/77c95bce-a381-4b8d-85e8-340121a67dd4/payloads.json`
3. **IMG_0003** — adjuntar `visual_scene_graph/pilot/fixtures/kennys/source/kennys-shop.jpg`  
   Comando exacto: `jq -c '.A' validation/vsg_2b/dry_runs/96c3a2c0-0243-4640-8079-e3bc720fc72d/payloads.json`
4. **IMG_0004** — adjuntar `benchmark/r2b_1_9_1/evidence_2026_09_21/R2B-191-D_source.jpg`  
   Comando exacto: `jq -c '.A' validation/vsg_2b/dry_runs/ed04d917-c5d3-4fe3-b6de-62c13f532f7f/payloads.json`
5. **IMG_0005** — adjuntar `benchmark/r2b_1_9_1/evidence_2026_09_21/R2B-191-E_source.jpg`  
   Comando exacto: `jq -c '.A' validation/vsg_2b/dry_runs/77c95bce-a381-4b8d-85e8-340121a67dd4/payloads.json`
6. **IMG_0006** — adjuntar `visual_scene_graph/pilot/fixtures/kennys/source/kennys-shop.jpg`  
   Comando exacto: `jq -c '.B' validation/vsg_2b/dry_runs/96c3a2c0-0243-4640-8079-e3bc720fc72d/payloads.json`

La clave autoritativa IMG/caso/condición está separada en
`development/coordination/VSG_VALUE_TEST_AB_KEY.json`. No mostrarla durante una
evaluación ciega.

El reloj de 168 horas permanece `NOT_STARTED`. Al generar la primera imagen
válida se deben registrar su timestamp con zona horaria, ID y SHA-256; ese evento
inicia el reloj y no se reemplaza por una fecha de vencimiento escrita.
