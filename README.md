# JARVIS — asistente de voz local

Asistente de voz personal, 100 % local: el audio nunca sale de tu máquina.
Se construye por fases (ver `ESPECIFICACION.md`).

**Fases activas:**

- **Fase 1 — Dictado (F9):** mantienes F9, hablas, la sueltas, y el texto se
  pega donde tengas el cursor.
- **Fase 2 — Comandos (F10):** mantienes F10, le pides algo ("abre VS Code",
  "¿qué es Supabase?"), y JARVIS actúa y te contesta con voz. **Esc** lo calla
  a media frase.

El modo comando usa el CLI de Claude Code que ya tienes en tu máquina
(reutiliza tu sesión, sin claves de API). Si no lo tienes instalado, F10 se
desactiva solo y el dictado sigue funcionando.

---

## Instalación (una sola vez)

1. Descarga o clona este repositorio.
2. Doble clic en **`instalar.bat`**. Crea un entorno virtual `venv` dentro de
   la carpeta e instala todo ahí — no toca nada global de tu Windows.
3. Corre el diagnóstico (descarga el modelo la primera vez, ~500 MB):

   ```
   venv\Scripts\python diagnostico.py --modelo
   ```

   Debe decir que la GPU se detectó, que hay micrófono, y al final
   **"El modelo corre en GPU"**. Si dice CPU, lee los mensajes de error
   que salen arriba.

## Uso diario

```
venv\Scripts\python jarvis.py
```

Cuando diga "Listo":

1. Pon el cursor donde quieras escribir (Bloc de notas, VS Code, el navegador…).
2. Mantén **F9** — suena un bip agudo — y habla.
3. Suelta **F9** — suena un bip grave — y en un momento el texto aparece pegado.

El pegado va por portapapeles (Ctrl+V), así que salen bien las ñ y las
tildes aunque el teclado físico no las tenga. Tu portapapeles anterior se
restaura solo después de pegar.

Para darle una orden: mantén **F10**, habla ("abre el bloc de notas",
"abre YouTube", "explícame qué es un endpoint"), y suéltala. Te contesta
hablado; si la respuesta es larga, lee un resumen y deja el texto completo
en el portapapeles. **Esc** corta la voz.

Las aplicaciones que sabe abrir están en `config.py` (`APLICACIONES`) —
agrega ahí las tuyas con la ruta de su ejecutable.

Para salir: **Ctrl+C** en la consola de JARVIS.

## Actualizar a la última versión

Doble clic en **`actualizar.bat`**. Descarga los archivos nuevos del
repositorio y actualiza las dependencias, sin tocar el `venv` ni tus datos.

## Ajustes

Todo se cambia en **`config.py`**: la tecla, el modelo (`small` → `medium`
si quieres más precisión), el vocabulario de programación que se le pasa a
Whisper, y los bips.

## Si algo falla

- **Dice que corre en CPU:** el diagnóstico (`diagnostico.py`) te dice si el
  problema es el driver de NVIDIA (falta `nvidia-smi`) o las dependencias.
  Con CPU igual funciona, solo más lento.
- **No pega nada:** revisa la consola — ahí sale el texto transcrito y
  cualquier error.
- **No graba:** revisa que Windows tenga un micrófono por defecto
  (Configuración → Sistema → Sonido) y que las apps tengan permiso de
  micrófono.
