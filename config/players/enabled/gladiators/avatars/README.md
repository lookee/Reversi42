# Gladiators Avatars

This directory contains avatar images for all Gladiator AI players.

## 📁 Structure

```
avatars/
├── default.png          # Default avatar (used by all players)
└── README.md           # This file
```

## 🎨 Avatar Specifications

### Default Avatar
- **File:** `default.png`
- **Size:** 512×512 pixels (recommended)
- **Format:** PNG with transparency
- **Usage:** All Gladiators use this default avatar

### Creating Custom Avatars

To create custom avatars for specific players:

1. Create a 512×512 PNG image
2. Save as `player_name.png` (e.g., `divzero.png`)
3. Update the player's YAML config:
   ```yaml
   avatar: "avatars/divzero.png"
   ```

### Recommended Design Guidelines

- **Size:** 512×512 pixels (square)
- **Format:** PNG with alpha transparency
- **File size:** < 500 KB
- **Style:** Match player personality
- **Background:** Transparent or solid color
- **Visibility:** Clear and recognizable at 64×64 scale

## 🎯 Player-Specific Avatar Ideas

### Champion Tier
- **DIVZERO.EXE** (💀): Dark metallic skull with glowing circuits
- **THE ORACLE** (🔮): Crystal ball with swirling galaxies
- **FORTRESS ETERNAL** (🏰): Stone fortress with protective barriers

### Advanced Tier
- **THE STRANGLER** (🐙): Octopus tentacles wrapping around pieces
- **THE EXECUTIONER** (⚔️): Hooded figure with glowing weapon
- **CORNER REAPER** (👹): Demon collecting corner pieces

### Intermediate Tier
- **LIGHTNING STRIKE** (⚡): Electric lightning bolt with motion blur
- **GLITCH LORD** (👾): Pixelated sprite with glitch effects

### Beginner Tier
- **BLITZ DEMON** (😈): Red demon with speed trails
- **ZEN MASTER** (🧘): Peaceful monk in meditation

### Premium
- **APOCALYPTRON** (⚡): Energy core with power rings

## 🛠️ Creating default.png

To create the default avatar image:

### Option 1: Simple Icon (Quick)
```bash
# Use ImageMagick to create a simple colored square
convert -size 512x512 xc:#3498db \
  -font Arial -pointsize 200 -fill white \
  -gravity center -annotate +0+0 "🤖" \
  avatars/default.png
```

### Option 2: Design Tool (Recommended)
1. Open GIMP/Photoshop/Figma
2. Create 512×512 canvas with transparent background
3. Design a generic robot/AI symbol
4. Use neutral colors (blue, silver, gray)
5. Export as PNG with transparency

### Option 3: Placeholder Text
Create a simple text-based placeholder:
- Background: Gradient (blue to purple)
- Text: "AI" or "🤖" centered
- Border: Subtle glow effect

## 📋 Usage in Configurations

All player configs reference avatars relative to the gladiators directory:

```yaml
metadata:
  name: "DIVZERO.EXE"
  icon: "💀"
  avatar: "avatars/default.png"  # ← Relative to gladiators/ directory
```

Path resolution:
- Relative path: `avatars/default.png`
- Full path: `config/players/gladiators/avatars/default.png`

## 🔄 Fallback Behavior

If avatar file is missing or invalid:
1. System checks `avatars/default.png`
2. If default missing, uses `icon` emoji from metadata
3. If both missing, uses generic robot emoji 🤖

## 📝 Notes

- All players currently use `default.png` for simplicity
- Custom avatars can be added per-player as needed
- Avatar images are optional (icons are sufficient)
- For tournaments/GUI, custom avatars enhance visual appeal

## 🎨 Default Avatar Recommendation

For the default.png, we recommend:
- **Theme:** Generic AI/robot
- **Colors:** Blue (#3498db) and silver (#95a5a6)
- **Design:** Simple, clean, modern
- **Symbol:** Robot head, circuit pattern, or "AI" text
- **Style:** Minimalist, recognizable at all sizes
