# sc_camera: informe devuelto por el agente

task_id: SC-MULTIAGENT-01-P1-CAMERA  
rol: sc_camera, análisis documental mediante instrucciones explícitas del perfil.  
modelo efectivo: UNKNOWN; el TOML declara `gpt-6.1-sol`, pero esta sesión no expone un identificador verificable de ejecución.  
base_commit: `33b6581353b18004a4818e8fc597b5455ba7ccf3`  
resultado: **PASS** documental.

Hallazgos:

1. **Observación:** cámara y preferencias están subordinadas a intención explícita, invariantes P0, modo y perfil ([STREETCRAFT.md:12](/Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2/STREETCRAFT.md:12)). CG-F prohíbe rediseñar proporciones, vanos, coronamiento y relaciones de señalética; exige verticales controladas y plano de fachada dominante ([CG_F_FRONTAL_ELEVATION.md:8](/Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2/command_invocation/CG_F_FRONTAL_ELEVATION.md:8)).

2. **Observación:** `/sc-front` activa CG-F y frontalización STRICT, sin cambiar por sí solo perfil, modo, relación de aspecto, calle o locks ([CG_F_FRONTAL_ELEVATION.md:25](/Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2/command_invocation/CG_F_FRONTAL_ELEVATION.md:25)). La macro completa agrega identidad STRICT y oclusión LOCKED_UNKNOWN; una elevación incompleta debe conservar incertidumbre ([CG_F_FRONTAL_ELEVATION.md:17](/Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2/command_invocation/CG_F_FRONTAL_ELEVATION.md:17)). **Inferencia:** el quickstart debe distinguir modificador y macro.

3. **Observación:** VP02 general admite CG-A/CG-B y retira la obligatoriedad de yaw≈0° y perspectiva frontal de un punto ([VISUAL_PROFILES.md:48](/Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2/transform/VISUAL_PROFILES.md:48)). BD01/BD02 seleccionan explícitamente CG-F STRICT, horizonte estable, verticales rectas y convergencia dramática mínima; rechazan overrides oblicuos/automáticos ([BACKDROP_PRESETS.md:39](/Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2/command_invocation/BACKDROP_PRESETS.md:39), [BACKDROP_PRESETS.md:54](/Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2/command_invocation/BACKDROP_PRESETS.md:54)). **Inferencia:** son restricciones del preset específico, no una nueva obligación general de VP02.

4. **Observación:** BD01 permite recomposición solamente en regiones no protegidas; P0, identidad, PR0/PR1, texto y desconocidos prevalecen, pudiendo dejar vacío el alcance disponible ([BACKDROP_PRESETS.md:76](/Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2/command_invocation/BACKDROP_PRESETS.md:76)). BD02 prohíbe trasladar masas importantes y sustituir edificios. La mención general de oclusiones reconstruidas en T08 queda acotada por evidencia y unknown locks en este preset ([TRANSFORMATION_MODES.md:24](/Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2/transform/TRANSFORMATION_MODES.md:24), [BACKDROP_PRESETS.md:94](/Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2/command_invocation/BACKDROP_PRESETS.md:94)).

5. **Observación:** Fear City confirmado conserva T06/VP03/CG-FC salvo override explícito; nombrar un perfil RDR no basta. Incluso con override siguen protegidas autoría, geografía y geometría ([AUTO_ROUTING.md:8](/Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2/transform/AUTO_ROUTING.md:8), [AUTO_ROUTING.md:69](/Users/macbookpro/Documents/STREETCRAFT_VISUAL_SYSTEM_V1_6_2/transform/AUTO_ROUTING.md:69)). **Recomendación:** usar una fuente documental no Fear City en el ejemplo BD, o declarar expresamente el override y sus límites.

Validaciones: HEAD y checkpoint coinciden al inicio y al cierre; digest `2c60a49a3d58581dc40602e9c9357ea4d8ca842a0520d18b1b0bbc8d96ea1cc0`. Diff de contratos citados contra HEAD vacío. Leídos AGENTS, perfil, README, STREETCRAFT, protocolo, checkpoint, spec del piloto y v12. Dos rutas supuestas no existían; se localizaron archivos reales con `rg --files`. `python` no estaba disponible; lectura JSON comprobada con `python3`.

Patch/archivos modificados: ninguno.  
Límites: lectura documental; sin pruebas runtime, imágenes, evaluación visual ni impresión. Permisos efectivos compartidos y sin aislamiento read-only impuesto; respetado por conducta. Uso/cuota UNKNOWN.  
Bloqueos: ninguno para esta subtarea; carga nominal del perfil y modelo efectivo no acreditados.

Cierre en tres líneas:  
Cerrar P1-CAMERA: cinco hallazgos documentales respaldados por contratos del mismo commit.  
Preservar CG-F/backdrop bajo identidad, relaciones protegidas y desconocidos; distinguir macro, modificador y routing Fear City.  
La evidencia no acredita calidad visual, impresión, carga nominal del perfil ni modelo efectivo.

Nota del orquestador: metadata local del hilo 01a132fa-db40-7f70-af47-adec2d11d90a registra modelo efectivo gpt-6.1-sol, esfuerzo medium. El UNKNOWN del informe indica lo que el agente pudo observar; no se reemplaza su respuesta original.
