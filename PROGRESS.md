# PROGRESS — Web de DEOSOLUCIONES S.A.S

> Bitácora del proyecto. **Lee esto primero** para retomar sin releer todo el código.
> Última actualización: 2026-06-04

---

## 1. Qué es este proyecto

Página web (para **GitHub Pages**) que presenta la información de la presentación
de **DEOSOLUCIONES S.A.S** ("Transformamos retos en soluciones"). Es una
**reconstrucción nativa en HTML/CSS** del contenido del PowerPoint original —
**no** son las diapositivas pegadas como imágenes. Navegación tipo presentación,
diapositiva a diapositiva, con diseño moderno, responsivo y claro.

- **URL en vivo:** https://poeta2475.github.io/dbpre/
- **Rama de trabajo:** `main` (la única que importa; `lan` quedó obsoleta).
- **Origen del contenido:** PowerPoint `DEOSOLUCIONESiii.pptx` (18 diapositivas).
  El texto de la web es **el mismo del pptx** (no se inventa texto).

---

## 2. Estructura del repo

```
index.html          <- LA WEB (autocontenida: HTML + CSS + JS). Es lo que sirve GitHub Pages.
images/             <- imágenes optimizadas (logos + fotos). ~1.3 MB en total.
build/
  template.html     <- el DISEÑO (todo el CSS y el JS). Tiene marcadores __SLIDES__, __N__, __N2__.
  generate.py       <- inyecta el CONTENIDO (textos + qué foto/icono) en template.html y escribe index.html.
PROGRESS.md         <- este archivo.
README.md
.nojekyll           <- evita el procesado Jekyll en GitHub Pages.
```

**Flujo de construcción:** `build/generate.py` lee `build/template.html`,
mete las 18 diapositivas y genera `index.html`.

```bash
python3 build/generate.py     # regenera index.html (no necesita el pptx ni internet)
```

Para **cambiar textos/orden/iconos** -> editar la lista de `slides` en `build/generate.py`.
Para **cambiar el diseño (CSS/JS)** -> editar `build/template.html`.
Después, correr `python3 build/generate.py` y commitear `index.html`.

---

## 3. Diseño actual (decisiones tomadas)

- **Tema CLARO** (fondo `#F5F8FF` con degradados suaves lavanda/durazno).
  Motivo: el logo de la empresa es azul muy oscuro y sobre fondo oscuro
  **se perdía**. En claro se ve nítido.
- **Paleta de marca** (del tema del pptx):
  - navy `#0C0A9E` · morado `#8208D5` · naranja `#EB9109` · lavanda `#BFBEF7`
  - tinta de texto `#16142b` · gris texto `#4c4a63`
  - degradado de acento: `linear-gradient(120deg, naranja, morado 55%, navy)`
- **Tipografías:** Sora (títulos) + Inter (cuerpo), vía Google Fonts; con
  fallback a `system-ui`/Arial si no cargan.
- **Tipos de diapositiva** (clases CSS y funciones en generate.py):
  - `hero` — portada: SOLO el logotipo completo (`image4.png`, que ya incluye
    símbolo + nombre + lema) + línea de acento + pastilla. **Un solo logo.**
  - `divider` — separador de sección: número gigante en degradado + pregunta +
    foto en tarjeta redondeada al lado.
  - `split` (`content` con foto) — foto en tarjeta + texto al lado.
  - `solo` (`content` sin foto) — icono + título + texto centrado.
  - `dual` — dos tarjetas blancas (slides 4 y 16).
  - `closing` — cierre con logotipo + conclusiones.
- **Marca fija** (esquina sup. izq., `image3.png`): aparece en las diapositivas
  de contenido, pero se **oculta en portada y cierre** (ahí ya está el logo
  completo) para no duplicar logos. Lógica en `show()` dentro del JS.
- **Iconos**: SVG inline (`ICONS` en generate.py), decorativos.

### Interacción / JS (en template.html)
- Navegación: flechas ←/→, espacio, PgUp/PgDn, Home/End; botones ‹ ›; puntos;
  botón pantalla completa ⛶.
- **Swipe SOLO horizontal** -> cambia diapositiva. Los gestos verticales se
  dejan al navegador (para no romper scroll ni pull-to-refresh).
- Barra de progreso superior + contador "NN / 18".

---

## 4. Responsividad

- `index.html` usa `100dvh`, `clamp()` para tipografías y media queries.
- Móvil **vertical**: las `split` se apilan (foto arriba, texto abajo); las
  `dual` pasan a 1 columna (<640px). Verificado: **sin desbordes**.
- Móvil **horizontal** (alto ~390px): si una diapositiva no cabe, **hace scroll
  interno** dentro de la propia diapositiva (no se corta nada).
- `align-items:safe center` evita recortes cuando el contenido es más alto que
  la pantalla.

---

## 5. Imágenes — notas importantes

- Optimizadas de **12 MB -> 1.3 MB** (las fotos a JPG máx. 1280px; los logos PNG
  con transparencia). Esto arregló la carga lenta en móvil.
- **GOTCHA resuelto:** `image8` (la bombilla) venía con **fondo transparente**;
  al aplanarla a RGB quedó **toda negra** (la diapositiva 5 "no se veía").
  Solución: aplanar sobre **blanco** `(245,248,255)`. Si re-extraes imágenes con
  transparencia, **aplánalas sobre blanco**, no sobre negro.
- Mapa logo/fotos (nombres en `images/`):
  - `image3.png` = símbolo circular (marca fija) · `image4.png` = logotipo
    completo (símbolo+nombre+lema) · `image5.png` = variante del símbolo.
  - Fotos: `image6` intro · `image7` problema · `image8` bombilla/idea ·
    `image9` seguridad · `image10` tienda · `image11` "cómo" · `image12`
    tecnología · `image13` beneficios · `image14` adaptación · `image15` equipo.

### Preparación de imágenes (paso aparte, requiere el .pptx)
No es necesario para editar textos/diseño. Solo si hay que regenerar assets:
1. Descomprimir el `.pptx` (es un zip) -> `ppt/media/`.
2. Optimizar con Pillow: fotos a JPG (máx 1280px, q80); logos PNG.
   Transparencias -> aplanar sobre blanco.
3. Copiar a `images/`.

---

## 6. GitHub Pages

- **Settings -> Pages -> Source: "Deploy from a branch" -> rama `main` -> `/ (root)`.**
  (Si está en "GitHub Actions", cambiarlo a "Deploy from a branch".)
- El repo debe ser **público** (ya lo es) para Pages gratis.
- Tras hacer push a `main`, esperar 1-2 min y recargar.

---

## 7. Historial de cambios (lo que ya se hizo)

1. Primer intento: clon 1:1 de las diapositivas (HTML+SVG desde el XML del pptx).
   Descartado: el usuario quería una web rediseñada, no las diapositivas pegadas.
2. **Rediseño nativo** en HTML/CSS con el contenido extraído.
3. Imágenes optimizadas (12 MB -> 1.3 MB).
4. `text-size-adjust:100%` para que el móvil no infle la fuente (desfase).
5. Cambio a **tema claro** (el logo oscuro ya no se pierde).
6. Portada con **un solo logo** (se quitaron símbolo y lema duplicados; marca
   fija oculta en portada/cierre).
7. **Fix `image8`** (bombilla negra -> sobre blanco). Slide 5 ya se ve.
8. **Pull-to-refresh**: se quitó `overflow:hidden` del body y se ajustó
   `overscroll-behavior` para no bloquear el gesto de recargar.

---

## 8. Pendientes / ideas

- [ ] Confirmar visualmente en el móvil del usuario (el entorno de build no
      puede "ver" capturas; se valida midiendo píxeles y layout por DOM).
- [ ] Posible pulido extra "estilo landing moderna": micro-animaciones de
      entrada por sección, hover-lift en tarjetas, patrón sutil de fondo.
- [ ] (Opcional) Botón de descarga / contacto en el cierre.

---

## 9. Cómo verificar sin "ver" (entorno headless)

Hay scripts de prueba con Puppeteer en `/tmp` durante el desarrollo (no se
commitean). Verifican: ausencia de errores JS, que las imágenes cargan
(`naturalWidth>0`), que ninguna diapositiva desborda en desktop/móvil, y el
brillo medio de los píxeles (para confirmar que el tema es claro). El error de
consola `ERR_CERT_AUTHORITY_INVALID` es solo Google Fonts en el sandbox de
pruebas; en un dispositivo real cargan bien.
