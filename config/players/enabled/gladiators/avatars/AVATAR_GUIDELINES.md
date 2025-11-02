# Avatar Design Guidelines - Quick Reference

## 🎨 Visual Design Themes by Player Type

### Champion Tier (ELO 1800+) - POWER & DOMINANCE

**Color Palette:**
- Primary: Dark metallics (charcoal, gunmetal)
- Accent: Glowing effects (red, purple, gold)
- Background: Deep blacks, dark gradients

**Visual Elements:**
- Bold, imposing imagery
- Sharp edges, angular design
- Energy effects, glowing elements
- Technological/futuristic aesthetic

**Examples:**
- Robotic skull with circuit patterns
- Digital singularity/black hole
- Crown with energy aura
- Mechanical dragon

---

### Advanced Tier (ELO 1600-1800) - WISDOM & MASTERY

**Color Palette:**
- Primary: Deep purples, blues, teals
- Accent: Cosmic effects (stars, nebula)
- Background: Gradient mystical auras

**Visual Elements:**
- Mystical symbols, runes
- Cosmic/space imagery
- Crystal balls, orbs
- Ancient wisdom motifs

**Examples:**
- Crystal ball with galaxy
- Ancient tome with glowing runes
- Owl with cosmic eyes
- Hourglass with flowing stars

---

### Intermediate Tier (ELO 1300-1600) - SPEED & ENERGY

**Color Palette:**
- Primary: Bright blues, yellows, whites
- Accent: Electric effects, motion blur
- Background: Dynamic gradients, light bursts

**Visual Elements:**
- Motion lines, speed effects
- Lightning bolts, electricity
- Dynamic composition
- Clean, energetic design

**Examples:**
- Lightning bolt with particles
- Comet/shooting star
- Wind/tornado symbol
- Rocket/jet imagery

---

### Beginner Tier (ELO 1000-1300) - FRIENDLY & APPROACHABLE

**Color Palette:**
- Primary: Warm colors (greens, oranges)
- Accent: Soft glows, friendly highlights
- Background: Light, welcoming tones

**Visual Elements:**
- Simple, clean design
- Rounded shapes
- Friendly imagery
- Minimal complexity

**Examples:**
- Friendly robot face
- Simple chess piece
- Geometric pattern
- Abstract symbol

---

## 📐 Technical Specifications

### Required Dimensions

```
Primary Avatar:    512 × 512 pixels (1:1 ratio)
Thumbnail:         256 × 256 pixels (generated)
Small Icon:        128 × 128 pixels (generated)
Mini Icon:          64 × 64 pixels (generated)
```

### File Format Details

**PNG (Recommended):**
```
Format: PNG-24 with alpha transparency
Color depth: 24-bit RGB + 8-bit alpha
Compression: Deflate (standard)
Max file size: 500 KB
```

**JPEG (Alternative):**
```
Format: JPEG
Quality: 90-95% (high quality)
Color space: RGB
Max file size: 300 KB
Note: No transparency support
```

**SVG (Vector):**
```
Format: SVG 1.1
Max file size: 100 KB
Note: Ensure compatibility, avoid complex effects
```

---

## 🎯 Design Checklist

### Before Creating

- [ ] Understand player personality (champion, speed, defensive, etc.)
- [ ] Choose appropriate color scheme
- [ ] Select visual theme (robot, mystical, animal, abstract)
- [ ] Gather reference images for inspiration

### During Creation

- [ ] Use square canvas (512×512)
- [ ] Keep design simple and recognizable
- [ ] Ensure readability at small sizes (64×64)
- [ ] Use high contrast (avoid similar colors)
- [ ] Add transparent background (PNG)
- [ ] Test against light and dark UI backgrounds

### After Creation

- [ ] Export at 512×512 pixels
- [ ] Optimize file size (<500 KB)
- [ ] Preview at multiple sizes (512, 256, 128, 64)
- [ ] Test in actual UI/game environment
- [ ] Verify filename follows convention

---

## 🛠️ Step-by-Step Creation Process

### Method 1: Digital Design (GIMP/Photoshop)

1. **Setup Canvas**
   ```
   - Create 512×512 pixel document
   - Set background to transparent
   - Add guide lines at center (256, 256)
   ```

2. **Create Base Shape**
   ```
   - Draw main element (circle, skull, bolt, etc.)
   - Keep centered with 20-30px padding
   - Use layers for organization
   ```

3. **Add Details**
   ```
   - Add secondary elements (glow, circuits, energy)
   - Apply layer effects (shadows, outer glow)
   - Ensure details visible at 64×64
   ```

4. **Color and Effects**
   ```
   - Apply color scheme
   - Add gradients, glows
   - Keep effects subtle (readable when small)
   ```

5. **Export**
   ```
   File → Export As → PNG
   - Enable transparency
   - Compression level: 6-9
   - Verify file size <500 KB
   ```

### Method 2: AI Generation (DALL-E/Midjourney)

1. **Craft Prompt**
   ```
   Example: "Digital skull with glowing circuit patterns, 
   cyberpunk style, red glowing eyes, dark background, 
   centered composition, icon style, 512×512, high detail"
   ```

2. **Generate Options**
   ```
   - Create 3-5 variations
   - Select best composition
   - Ensure square format
   ```

3. **Post-Processing**
   ```
   - Remove background (remove.bg or GIMP)
   - Resize to exact 512×512
   - Adjust contrast/brightness
   - Add subtle glow if needed
   ```

4. **Optimize**
   ```
   - Export as PNG with transparency
   - Compress with TinyPNG
   - Verify final file size
   ```

---

## 🎨 Quick Design Templates

### Template 1: Geometric Robot

```
Base: Circular metallic face
Eyes: Two glowing dots (cyan/red)
Accent: Circuit lines on "cheeks"
Glow: Subtle outer glow (matching eye color)
Background: Transparent
Style: Clean, modern, tech
```

### Template 2: Mystical Orb

```
Base: Translucent sphere
Center: Swirling galaxy/nebula
Border: Glowing energy ring
Particles: Floating stars/sparkles
Background: Transparent with soft aura
Style: Cosmic, magical, prophetic
```

### Template 3: Lightning Strike

```
Base: Vertical lightning bolt
Effect: Electric particles around bolt
Glow: Bright blue/yellow halo
Motion: Subtle blur for speed
Background: Transparent
Style: Dynamic, energetic, fast
```

### Template 4: Shield/Fortress

```
Base: Medieval shield shape
Details: Stone texture or metal plating
Symbol: Center emblem (tower, cross)
Border: Reinforced edges
Background: Transparent
Style: Solid, defensive, protective
```

---

## 🌈 Color Schemes Reference

### Scheme 1: Cyberpunk Menace
```
Primary: #1a1a2e (dark blue-gray)
Secondary: #16213e (navy)
Accent: #e94560 (electric red)
Glow: #ff006e (hot pink)
Use for: Aggressive, powerful AIs
```

### Scheme 2: Mystic Oracle
```
Primary: #2d1b69 (deep purple)
Secondary: #5c4d7d (lighter purple)
Accent: #9d84b7 (lavender)
Glow: #c3aed6 (pale purple)
Use for: Mystical, prophetic AIs
```

### Scheme 3: Lightning Speed
```
Primary: #00d9ff (electric cyan)
Secondary: #ffd700 (gold yellow)
Accent: #ffffff (pure white)
Glow: #7df9ff (bright cyan)
Use for: Fast, energetic AIs
```

### Scheme 4: Forest Guardian
```
Primary: #2d5016 (forest green)
Secondary: #4a7c59 (sage)
Accent: #a7c957 (lime green)
Glow: #deff8b (pale yellow-green)
Use for: Balanced, defensive AIs
```

---

## 📏 Size Testing

Test your avatar at all target sizes:

```
512×512: Full resolution (tournament display, profile)
256×256: Standard (player selection, match preview)
128×128: Medium (in-game sidebar, notifications)
 64×64:  Small (mini scoreboard, chat icons)
 32×32:  Tiny (favicon, minimal UI elements)
```

**Readability Test:**
- Is main shape recognizable at 64×64?
- Can you identify colors at 32×32?
- Does it look crisp (not blurry) at all sizes?
- Do small details disappear or remain visible?

---

## ✅ Quality Standards

### Excellent Avatar (9-10/10)
- Instantly recognizable at all sizes
- Clear visual theme matching player
- Professional color scheme
- Crisp edges, no artifacts
- File size <200 KB

### Good Avatar (7-8/10)
- Recognizable at 64×64 and above
- Appropriate colors and theme
- Minor quality issues at tiny sizes
- File size <400 KB

### Acceptable Avatar (5-6/10)
- Recognizable at 128×128
- Generic theme, works but not special
- Some blur or artifacts
- File size <500 KB

### Needs Improvement (<5/10)
- Hard to recognize at small sizes
- Unclear theme or poor colors
- Visible compression artifacts
- File size >500 KB or low resolution

---

## 🔗 Useful Resources

### Free Stock Images
- Unsplash: https://unsplash.com/ (high-res photos)
- Pexels: https://www.pexels.com/ (free stock)
- Pixabay: https://pixabay.com/ (public domain)

### Icon Libraries
- Flaticon: https://www.flaticon.com/ (icons, shapes)
- Font Awesome: https://fontawesome.com/ (vector icons)
- Heroicons: https://heroicons.com/ (simple icons)

### Color Tools
- Coolors: https://coolors.co/ (palette generator)
- Adobe Color: https://color.adobe.com/ (color wheel)
- Paletton: https://paletton.com/ (scheme designer)

### Optimization Tools
- TinyPNG: https://tinypng.com/ (compress PNG)
- Squoosh: https://squoosh.app/ (optimize images)
- Remove.bg: https://remove.bg/ (background removal)

### Design Software
- GIMP: https://www.gimp.org/ (free Photoshop alternative)
- Inkscape: https://inkscape.org/ (vector graphics)
- Krita: https://krita.org/ (digital painting)
- Photopea: https://www.photopea.com/ (online editor)

---

## 💡 Pro Tips

1. **Keep It Simple:** Complex designs lose detail at small sizes
2. **High Contrast:** Ensure visibility on any background
3. **Test Early:** Check 64×64 preview frequently during design
4. **Use Layers:** Organize design in layers for easy editing
5. **Save Source:** Keep original PSD/XCF file for future edits
6. **Version Control:** Save iterations (v1, v2, v3) during design
7. **Get Feedback:** Show to others before finalizing
8. **Match Theme:** Visual should reflect player's playing style
9. **Transparency:** Use PNG transparency for professional look
10. **Optimize Last:** Design first, compress at the end

---

## 📝 Naming Examples

```
divzero.png                    ✅ Good (simple, descriptive)
the_oracle.png                 ✅ Good (matches name)
lightning_strike.png           ✅ Good (underscores for spaces)
my_custom_ai_v2.png           ✅ Good (versioned)

DivZero.PNG                    ❌ Bad (use lowercase)
The Oracle.png                 ❌ Bad (no spaces)
avatar-lightning.png           ❌ Bad (use underscores, not hyphens)
IMG_1234.png                   ❌ Bad (non-descriptive)
```

---

## 🎓 Learning Path

### Beginner (1-2 hours)
1. Use icon library (Flaticon)
2. Simple shape + color
3. Add basic glow effect
4. Export PNG

### Intermediate (3-5 hours)
1. Learn GIMP basics
2. Create custom shape/composition
3. Apply gradients and effects
4. Layer management

### Advanced (1-2 days)
1. Digital painting in Krita
2. Complex lighting and shadows
3. Particle effects
4. Professional finishing

### Expert (1+ weeks practice)
1. 3D rendering integration
2. Advanced compositing
3. Unique artistic style
4. Portfolio-quality work

