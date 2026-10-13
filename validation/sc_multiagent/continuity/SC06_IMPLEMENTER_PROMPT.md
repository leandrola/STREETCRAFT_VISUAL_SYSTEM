# SC06-IMPLEMENTER-RECONSTRUCTION-01

Actuás como implementador trazable de Streetcraft. Trabajá solamente en lectura. No modifiques archivos, no delegues, no hagas commit/push y no invoques herramientas de imagen.

## Objetivo

Reconstruí el patch completo del supervisor de continuidad desde la base exacta `d946f1b5d0d6dad53f080540ae9634bdf360d440`. La salida debe permitir que root aplique el patch serialmente a una copia limpia de esa base y obtenga el candidato completo.

## Contratos

Leé `AGENTS.md`, `specs/SC_MULTIAGENT_03_v1.md`, `specs/SC_MULTIAGENT_04_v1.md`, `specs/SC_MULTIAGENT_06_PROVENANCE_RECOVERY_v1.md`, `development/coordination/CHECKPOINT.json` y el candidato actual. Conservá GLIGEN `PAUSED`, D3/D4 `PENDING`, VSG `SHADOW`, cero imágenes y cero gasto adicional.

El supervisor reconstruido debe cubrir sobre acotado, lock, procesos, timeout y stop del grupo, sesión persistida, resume exacto, reconciliación sin relanzamiento, separación de estado de proceso y negocio y digest reproducible. La corrida simulada histórica no cuenta como procedencia ni piloto real.

## Archivos permitidos

- `scripts/sc_supervisor.py`
- `tests/test_sc_supervisor.py`
- `tests/fixtures/sc_fake_executor.py`
- `docs/SC_CONTINUITY_QUICKSTART.md`

No incluyas otros archivos en el patch.

## Entregable

Devolvé un único objeto JSON conforme al esquema suministrado. `patch` debe contener un unified diff completo con encabezados `diff --git`, aplicable con `git apply` sobre la base exacta. El patch debe responsabilizar al turno por todos los bytes de los cuatro archivos; no devuelvas un delta pequeño sobre la implementación publicada.

Podés reproducir los bytes correctos del candidato actual o reimplementarlos si encontrás un defecto contractual. No agregues cambios cosméticos. Registrá en `validations` las comprobaciones de lectura que realizaste. Si no podés producir el patch completo dentro de estos límites, devolvé `BLOCKED` y un patch vacío.

## Cierre

PASS requiere patch completo de los cuatro archivos, base exacta y ninguna escritura. FAIL indica un defecto comprobado sin solución dentro del turno. BLOCKED indica falta de capacidad, input o límite. No autodeclares modelo efectivo: root lo obtiene de metadata del runtime.
