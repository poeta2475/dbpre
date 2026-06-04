# -*- coding: utf-8 -*-
"""
Generador de la web de DEOSOLUCIONES.
- Lee build/template.html (el diseño: CSS + JS) y le inyecta las diapositivas.
- Escribe index.html en la raíz del repo.
- NO toca images/ (ya están optimizadas en el repo).

Uso:  python3 build/generate.py
Las imágenes ya vienen optimizadas en images/. Si necesitas regenerarlas
desde el PowerPoint original, mira la sección "Preparación de imágenes"
en PROGRESS.md (es un paso aparte que requiere el .pptx).
"""
import os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL_PATH = os.path.join(ROOT, 'build', 'template.html')
OUT_PATH = os.path.join(ROOT, 'index.html')

# ----- iconos SVG (decorativos, usan currentColor) -----
ICONS = {
 'shield':'<path d="M12 3l7 3v5c0 4.5-3 8-7 9-4-1-7-4.5-7-9V6l7-3z"/><path d="M9 12l2 2 4-4"/>',
 'cart':'<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M3 4h2l2.2 11.5a2 2 0 0 0 2 1.5h7.8a2 2 0 0 0 2-1.6L21 8H6"/>',
 'headset':'<path d="M4 13v-1a8 8 0 0 1 16 0v1"/><path d="M4 13h3v5H5a2 2 0 0 1-2-2v-3z"/><path d="M20 13h-3v5h2a2 2 0 0 0 2-2v-3z"/><path d="M17 18v1a3 3 0 0 1-3 3h-2"/>',
 'chip':'<rect x="7" y="7" width="10" height="10" rx="2"/><path d="M10 7V4M14 7V4M10 20v-3M14 20v-3M7 10H4M7 14H4M20 10h-3M20 14h-3"/>',
 'clock':'<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
 'chart':'<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 'refresh':'<path d="M20 11a8 8 0 0 0-14-5l-2 2M4 13a8 8 0 0 0 14 5l2-2"/><path d="M4 4v4h4M20 20v-4h-4"/>',
 'hands':'<path d="M3 13l4-4 3 2 4-4 3 2 4-4"/><path d="M3 17l4-4 3 2 4-4 3 2 4-4"/>',
 'spark':'<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M18 6l-2.5 2.5M8.5 15.5L6 18"/><circle cx="12" cy="12" r="3"/>',
 'lock':'<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
}
def icon(name, cls='ic'):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">{ICONS.get(name,"")}</svg>')
def esc(t): return html.escape(t)
def P(*ps): return list(ps)

# ----- constructores de diapositivas -----
def hero():
    return ('<section class="slide hero active" data-i="1"><div class="hero-bg"></div>'
            '<div class="hero-inner">'
            '<img class="hero-word" src="images/image4.png" alt="DEOSOLUCIONES — Transformamos retos en soluciones">'
            '<span class="accent-line center"></span>'
            '<div class="hero-pill">Soluciones tecnológicas 3 en 1 · Seguridad · Soporte · Comercio</div>'
            '</div></section>')

def divider(i, num, title, photo):
    return (f'<section class="slide divider" data-i="{i}">'
            f'<div class="div-photo" style="background-image:url(\'images/{photo}\')"></div>'
            f'<div class="div-overlay"></div>'
            f'<div class="div-inner"><div class="div-num">{num}</div>'
            f'<h2 class="div-title">{esc(title)}</h2><span class="accent-line"></span></div></section>')

def content(i, eyebrow, ic, title, paras, photo=None):
    body=''.join(f'<p>{esc(p)}</p>' for p in paras)
    if photo:
        return (f'<section class="slide split" data-i="{i}">'
                f'<div class="split-media"><div class="ph" style="background-image:url(\'images/{photo}\')"></div><div class="ph-grad"></div></div>'
                f'<div class="split-text"><div class="eyebrow">{icon(ic,"eic")}<span>{esc(eyebrow)}</span></div>'
                f'<h2 class="c-title">{esc(title)}</h2><span class="accent-line"></span>'
                f'<div class="c-body">{body}</div></div></section>')
    return (f'<section class="slide solo" data-i="{i}"><div class="solo-inner">'
            f'<div class="badge">{icon(ic,"bic")}</div>'
            f'<div class="eyebrow"><span>{esc(eyebrow)}</span></div>'
            f'<h2 class="c-title big">{esc(title)}</h2><span class="accent-line"></span>'
            f'<div class="c-body wide">{body}</div></div></section>')

def dual(i, eyebrow, cards):
    cs=''
    for (t,b,ic) in cards:
        cs+=(f'<div class="card"><div class="card-ic">{icon(ic,"cic")}</div>'
             f'<h3>{esc(t)}</h3><p>{esc(b)}</p></div>')
    return (f'<section class="slide dual" data-i="{i}"><div class="dual-inner">'
            f'<div class="eyebrow center"><span>{esc(eyebrow)}</span></div>'
            f'<div class="cards">{cs}</div></div></section>')

def closing(i, title, paras):
    body=''.join(f'<p>{esc(p)}</p>' for p in paras)
    return (f'<section class="slide closing" data-i="{i}"><div class="close-bg"></div>'
            f'<div class="close-inner"><img class="close-word" src="images/image4.png" alt="DEOSOLUCIONES">'
            f'<h2 class="div-title">{esc(title)}</h2><span class="accent-line center"></span>'
            f'<div class="c-body close-body">{body}</div>'
            f'<div class="hero-pill">Una solución 3 en 1 para modernizar tu empresa</div></div></section>')

# ----- CONTENIDO (texto exacto extraído del PowerPoint, no inventado) -----
slides=[]
slides.append(hero())
slides.append(content(2,'Contexto','spark','Introducción',
   P('Hoy en día las pequeñas y medianas empresas quieren modernizarse, pero tienen un problema: la tecnología es muy cara, los proveedores les venden todo por separado y nadie les ayuda a conectar los sistemas.',
     'DEOSOLUCIONES será la solución tecnológica única de las empresas, donde encuentran desde los computadores y el soporte técnico hasta los sistemas de reconocimiento facial.'),'image6.jpg'))
slides.append(divider(3,'01','¿Cuál problema resolvemos?','image7.jpg'))
slides.append(dual(4,'01 · El problema',[
   ('Descontrol de personal','Muchas empresas todavía anotan las horas de llegada, los turnos y las horas extras en cuadernos o en hojas de Excel. Esto quita tiempo, genera errores y se presta para trampas.','clock'),
   ('Falta de seguridad y soporte','No saben con certeza quién entra o sale de sus áreas importantes, y si un computador se daña, no tienen a quién llamar que les resuelva rápido.','lock')]))
slides.append(divider(5,'02','¿Qué idea o solución proponemos?','image8.jpg'))
slides.append(content(6,'02 · La solución','shield','Seguridad y soporte',
   P('Implementamos sistemas de control de acceso con biometría y cámaras para monitoreo continuo y registro preciso de entradas.',
     'Ofrecemos soporte técnico presencial y remoto para minimizar tiempos de inactividad y garantizar continuidad operativa.'),'image9.jpg'))
slides.append(content(7,'02 · La solución','cart','Tienda y pagos seguros',
   P('Plataforma web con catálogo de equipos y accesorios disponible 24/7, pagos seguros vía Wompi (PSE, tarjetas, etc.).',
     'Facilitaremos compras con historial unificado y entregas confiables.'),'image10.jpg'))
slides.append(divider(8,'03','¿Cómo lo vamos a hacer realidad?','image11.jpg'))
slides.append(content(9,'03 · Cómo lo haremos','headset','Atención unificada',
   P('Atención en cualquier canal: web, WhatsApp o correo, con visitas técnicas con historial único.',
     'Soporte rápido y soporte continuo para reparar equipos y mantener el negocio siempre funcionando.')))
slides.append(content(10,'03 · Cómo lo haremos','chip','Tecnología y bases',
   P('Compra directa a mayoristas para mejores precios, cámaras y computadores fiables.',
     'Plataforma y sistema de cobros casi listos; bases de datos seguras para que el servicio nunca se caiga.'),'image12.jpg'))
slides.append(divider(11,'04','Beneficios y recursos','image13.jpg'))
slides.append(content(12,'04 · Beneficios','clock','Soporte técnico 24/7',
   P('Equipo local en Medellín y Área Metropolitana, con atención remota inmediata y visitas programadas para mantenimiento preventivo.',
     'Servicio orientado a respuesta rápida y recuperación operativa para evitar pérdidas de negocio.')))
slides.append(content(13,'04 · Beneficios','chart','Ahorro y control',
   P('Ahorro de tiempo y dinero: procesos que antes tomaban días en Excel ahora se hacen en un clic.',
     'Visualización y análisis del flujo de personal para cotizaciones y decisiones ágiles.')))
slides.append(content(14,'04 · Beneficios','refresh','Adaptación y continuidad',
   P('Respetamos programas ya instalados y adaptamos reconocimiento facial sin interrumpir procesos.',
     'Reparaciones rápidas y soporte para que el negocio siga vendiendo sin pausas.'),'image14.jpg'))
slides.append(divider(15,'05','¿Qué se necesita para lograrlo?','image15.jpg'))
slides.append(dual(16,'05 · Qué se necesita',[
   ('Equipo técnico y plataforma','Contar con técnicos e ingenieros apasionados por el servicio que dejen las instalaciones funcionando y con soporte continuo.','headset'),
   ('Web y cobros a punto','Dejar a punto nuestra página web y el sistema de cobros para que la experiencia de compra sea impecable.','cart')]))
slides.append(content(17,'05 · Qué se necesita','hands','Apoyos institucionales y mayoristas',
   P('Buscar apoyo del Fondo Emprender (SENA), iNNpulsa, la alcaldía de Medellín para acelerar crecimiento en Antioquia.',
     'Mantener alianzas mayoristas para comprar cámaras y computadores a buen precio.')))
slides.append(closing(18,'Conclusiones',
   P('DEOSOLUCIONES ofrece una solución 3 en 1 que integra seguridad, soporte y comercio electrónico para modernizar pymes.',
     'Resultado: ahorro de tiempo y costos, mayor seguridad y operaciones siempre activas.')))

N=len(slides)
tpl=open(TPL_PATH,'r',encoding='utf-8').read()
out=tpl.replace('__SLIDES__','\n'.join(slides)).replace('__N__',str(N)).replace('__N2__',f'{N:02d}')
open(OUT_PATH,'w',encoding='utf-8').write(out)
print(f'OK -> {OUT_PATH}  ({N} diapositivas, {len(out)} bytes)')
