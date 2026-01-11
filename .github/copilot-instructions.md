# GL Strategic Web - Copilot Instructions

## Project Overview
This is a **single-page website** for GL Strategic, a boutique high-level consulting firm based in Chile. The site showcases their strategic anticipation services, team expertise, and advisory methodology.

**Key Identity**: "Ingeniería de Anticipación" (Engineering of Anticipation) – combining deep technical expertise with strategic foresight grounded in Chile's Proyecto País.

---

## Architecture & Structure

### Single-File HTML Foundation
- **[index.html](../index.html)** is the entire application (~396 lines)
- Uses **Tailwind CSS** (CDN) with inline custom configuration
- **No JavaScript frameworks** – vanilla JS only for tab/accordion interactions
- **No build step** – pure HTML delivered as-is to browser

### Asset Organization
```
assets/
├── images/      (logos, team photos, diagrams, icons)
├── videos/      (background videos for sections: bosque, nuestro_adn, servicios, puerto, panel_solar, etc.)
└── docs/        (PDFs and reference documentation for clients)
```

### Color System (Tailwind Extended)
```javascript
colors: {
  navy: '#0F2F4A',      // Primary dark background
  dark: '#051c2c',      // Deepest background (body)
  gold: '#D4AF37',      // Primary accent, prestige
  cyan: '#00E5FF',      // Secondary accent (step 02)
  green: '#00C851',     // Step accent
  orange: '#FFBB33',    // Step accent
  red: '#FF4444',       // Step accent
  purple: '#AA66CC',    // Step accent
  info: '#33B5E5'       // Secondary info color
}
```

### Font System
- **Serif (Display)**: Playfair Display (headings, brand)
- **Sans (Body)**: Montserrat (content, labels)

---

## Critical Patterns & Components

### 1. Section Structure
Each major section follows this pattern:
```html
<section id="[anchor]" class="relative py-24">
  <div class="video-container">
    <video autoplay muted loop playsinline class="video-bg">
      <source src="assets/videos/[name].mp4" type="video/mp4">
    </video>
    <div class="overlay-navy"></div>
  </div>
  <div class="container...relative z-10"><!-- Content --></div>
</section>
```

**Pattern Details**:
- `id` attribute enables nav anchor links
- Video container absolutely positioned behind content (z-index: -1)
- Overlay provides content readability (rgba opacity varies)
- Content div has `relative z-10` to sit above video

**Sections (in order)**:
1. `#inicio` – Hero with manifesto CTA
2. `#adn` – Company DNA + Chart.js PIB forecast comparison
3. `#servicios` – Three-tab service methodology (CAM+/Pré-Futur, CAF, SEM)
4. `#equipo` – Team cards (Directors, Specialists, Regional Directors)
5. `#clientes` – Accordion-based client lists by industry
6. `#contacto` – Footer contact info

### 2. Card Components

#### Pre-Futur Flip Cards (7 steps)
```html
<div class="pf-card">
  <div class="pf-inner">
    <div class="pf-front"><!-- Icon + label --></div>
    <div class="pf-back"><!-- Detail text --></div>
  </div>
</div>
```
- 3D rotate on hover (rotateX 180deg)
- Tall format (420px height, 7-column layout)
- Colored top border per step (cyan, green, orange, red, purple, info, gold)

#### Team Flip Cards
```html
<div class="team-card">
  <div class="team-inner">
    <div class="team-front"><img class="team-img"><!-- Name/title --></div>
    <div class="team-back"><!-- Details + LinkedIn --></div>
  </div>
</div>
```
- Smaller (210px), rotateY 180deg
- Image fills top 75% of front
- Back has navy background with white text

#### Client Cards
- 100px height, rotateY flip
- Display client name front, category back

### 3. Interactive Elements

#### Tabs (Services Section)
```javascript
function switchTab(id) {
  document.querySelectorAll('[id^="tab-"]').forEach(el => el.classList.add('hidden'));
  document.getElementById('tab-' + id).classList.remove('hidden');
  // Update active button styling
}
```
- Three tab buttons toggle visibility of `.hidden` divs
- Active button gets `bg-gold` + gold text

#### Accordions (Clients Section)
```javascript
function toggleAccordion(btn) {
  const panel = btn.nextElementSibling;
  if (panel.style.maxHeight) { panel.style.maxHeight = null; }
  else { panel.style.maxHeight = panel.scrollHeight + "px"; }
}
```
- Uses `max-height` for smooth CSS transition (0 → scroll height)
- Expands/collapses accordion-content divs

#### Chart.js Integration
- PIB comparison chart in `#adn` section
- Three datasets: Oficial (dashed red), Proyección GL (green), Realidad (white)
- Custom styling with white labels, transparent grid

### 4. Glassmorphism & Styling Patterns
```css
.glass-panel {
  background: rgba(15, 47, 74, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(212, 175, 55, 0.2);
}
.glass-card-light {
  background: rgba(255, 255, 255, 0.95);
  color: #0F2F4A;
}
```
- Used for content panels and cards
- Subtle gold borders for premium feel
- Light variants for content areas

---

## Maintenance & Content Updates

### Image References
Images are linked from `assets/images/[filename].png`. When adding or updating images:
- Team photos: Use consistent sizing (suggest 400x500px)
- Diagrams: `diagrama_cam_glass.png`, `diagrama_caf_glass.png`, `diagrama_sem_glass.png`
- Icons: Keep consistent 40-60px rendered size
- Use `onerror="this.style.display='none'"` on diagrams (fallback for missing files)

### Video References
Background videos in `assets/videos/`:
- `bosque.mp4` (hero)
- `nuestro_adn.mp4`
- `servicios.mp4`
- `puerto.mp4`
- `panel_solar.mp4`
- Others referenced in CAF section

**Pattern for video failures**: Videos won't break layout if missing (autoplay + loop + playsinline ensures compatibility).

### Document Links
PDFs in `assets/docs/`:
- `LA VENTAJA IMPOSIBLE DE COPIAR.pdf` – Manifesto (hero button)
- `Ecoparque Industrial proyecto.doc` – Project detail
- Others: reference docs for internal use

---

## Development Workflow

### Making Changes
1. **Edit HTML directly** – No build step required
2. **Test locally** – Open `index.html` in browser
3. **Verify video/image paths** – Test on poor connections
4. **Check tab/accordion functions** – Inspect console for JS errors
5. **Test on mobile** – Viewport meta tag enables responsive behavior

### Git Workflow (from `.gitattributes` presence)
- Repository is tracked with Git
- Single `index.html` file + assets folder = clean versioning
- No compiled artifacts or dependencies to commit

### Common Tasks

**Adding a team member**:
1. Add image to `assets/images/[name].png`
2. Duplicate a `team-card` div in appropriate section
3. Update image src, name, role, LinkedIn URL

**Adding a client**:
1. Create `client-card` div in accordion matching category
2. Format: `<div class="client-front">Name</div><div class="client-back">Category</div>`

**Updating methodology steps**:
- Edit the 7 `pf-card` divs in `#tab-cam`
- Keep numbering (01–07), icons, colors, and flip text consistent

**Modifying colors**:
- Update Tailwind config in `<script>` section (theme.colors)
- Rebuild affected classes inline or use Tailwind utility classes
- Gold (#D4AF37) is the primary accent – rarely changes

---

## Known Constraints & Assumptions

1. **No server-side processing** – Static HTML/assets only
2. **Email link** (`contacto@glstrategic.cl`) opens default mail client
3. **LinkedIn URLs** for team members use public profile links (some point to "#" as fallback)
4. **No analytics/tracking** – Pure content delivery
5. **Mobile responsiveness** relies on Tailwind breakpoints (`sm:`, `md:`, `lg:`, `xl:`)
6. **Video autoplay** may not work on iOS Safari without user gesture (acceptable limitation)
7. **Chart.js data** is hardcoded (PIB chart shows 2015–2020 forecast vs reality)

---

## Team & Governance

**Leadership**: Gastón L'Huillier (Principal), Pablo Canobra, Claudio Maggi, Guillermo Muñoz, Rafael Sotil, Carlos Vergara, José Inostroza (Socios)

**Key Brand Values** (reflected in UI/copy):
- No junior staff – all senior consultants
- Boutique firm with big-firm depth
- Grounded in Chile's Proyecto País network (2,000+ experts)
- Strategic anticipation through data + expertise
- Personalized, transformation-focused engagement

---

## AI Agent Guidance

**Do**:
- Maintain glassmorphism + navy/gold aesthetic consistency
- Keep vanilla JS patterns for interactivity (no framework imports)
- Test section visibility, video playback, tab switching locally
- Preserve section anchor IDs for nav linking
- Use Tailwind utilities from extended config only

**Don't**:
- Add npm/build dependencies (breaks single-file model)
- Change core color palette without approval
- Add external JS frameworks or minifiers
- Remove video containers (integral to brand identity)
- Break responsive layout for mobile

**When uncertain**:
- Reference existing patterns (flip cards, accordions)
- Check CSS classes in inline `<style>` block
- Test on mobile viewport (375px width minimum)
- Verify all asset paths resolve to `assets/` folder
