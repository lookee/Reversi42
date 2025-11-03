# Player Avatar Images

Questa directory contiene le immagini avatar per i giocatori.

## 📁 Struttura

```
config/players/avatar/
└── human.png          # Avatar per giocatori umani
```

## 🎨 File Attuali

### `human.png`
- **Uso**: Avatar visualizzato per tutti i giocatori umani
- **Formato**: PNG (1024×1024)
- **Visualizzazione**: Circolare con bordo bianco leggero e ombra elegante

## 🔄 Comportamento

- **Giocatori Umani** (Black o White): Usano `/avatars/human.png`
- **Giocatori AI**: Usano `/avatars/default.png` o icone specifiche dal loro config

## ✏️ Personalizzazione

Per cambiare l'avatar dei giocatori umani:

```bash
# Sostituisci human.png con la tua immagine
cp /path/to/your-avatar.png config/players/avatar/human.png

# Ricarica la pagina del gioco nel browser
```

### Requisiti Immagine
- **Formato**: PNG (preferito per trasparenza)
- **Dimensioni**: 512×512 o 1024×1024 pixels (quadrata)
- **Sfondo**: Trasparente o tinta unita
- **Stile**: Riconoscibile anche a 72×72 pixels

## 🎯 Visualizzazione nel Gioco

L'avatar viene automaticamente:
- Ridimensionato a 72×72 pixels
- Trasformato in forma circolare (border-radius: 50%)
- Arricchito con bordo bianco (2px, trasparenza 15%)
- Ombreggiato con effetto elegante

## 📂 Posizioni Avatar

Il server cerca le immagini avatar in questo ordine:
1. `config/players/avatar/` (per human.png e altri avatar comuni)
2. `config/players/enabled/gladiators/avatars/` (per avatar AI specifici)

## 🔗 Collegamenti

- **Avatar AI**: `../enabled/gladiators/avatars/`
- **Configurazioni AI**: `../enabled/gladiators/*.yaml`
- **Documentazione**: `../README.md`

