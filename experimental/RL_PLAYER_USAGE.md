# Come Usare il Giocatore RL in Reversi42

## ✅ Giocatore Creato

Ho creato `src/Players/PlayerRL.py` che:
- ✅ Usa `latest.pth` di default
- ✅ Supporta MCTS (forte ma lento) o policy diretta (veloce)
- ✅ Integrato nel sistema Reversi42
- ✅ Utilizzabile nella web GUI e nei tornei

---

## 🎮 Come Giocare Contro il Giocatore RL

### Metodo 1: Web GUI

```bash
# Avvia web GUI
python -m src.ui.web

# Nel menu player, seleziona "Neural Prime"
```

### Metodo 2: Script Python

```python
from Players.PlayerFactory import PlayerFactory
from Reversi.BitboardGame import BitboardGame

# Crea giocatore RL
rl_player = PlayerFactory.create_player("Neural Prime")

# Oppure con parametri personalizzati
rl_player = PlayerFactory.create_player(
    "Neural Prime",
    model_path="experimental/checkpoints/latest.pth",
    use_mcts=True,
    mcts_simulations=400,
    temperature=0.1
)

# Gioca partita
game = BitboardGame()
while not game.is_finish():
    legal_moves = game.get_move_list()
    if legal_moves:
        move = rl_player.get_move(game, legal_moves)
        game.move(move)
```

### Metodo 3: Torneo

```python
from Players.PlayerFactory import PlayerFactory
from tournament.tournament import Tournament

# Crea giocatori
players = [
    PlayerFactory.create_player("RL Player"),
    PlayerFactory.create_player("Apocalyptron", depth=6),
    PlayerFactory.create_player("Minimax", depth=5),
]

# Crea torneo
tournament = Tournament(players=players, games_per_matchup=10)
tournament.run()
```

---

## ⚙️ Configurazione Giocatore RL

### Parametri Disponibili

```python
PlayerRL(
    model_path="experimental/checkpoints/latest.pth",  # Path al modello
    use_mcts=True,                                      # Usa MCTS (True) o policy diretta (False)
    mcts_simulations=400,                              # Simulazioni MCTS (se use_mcts=True)
    temperature=0.1,                                    # Temperatura sampling (0=deterministico)
    name="Neural Prime"                                   # Nome giocatore
)
```

### Configurazioni Consigliate

#### Forte ma Lento (MCTS)
```python
rl_player = PlayerFactory.create_player(
    "Neural Prime",
    use_mcts=True,
    mcts_simulations=800,  # Molte simulazioni
    temperature=0.0        # Deterministico
)
```
**Tempo per mossa**: ~14s
**Forza**: Molto alta

#### Veloce ma Forte (MCTS Ridotto)
```python
rl_player = PlayerFactory.create_player(
    "Neural Prime",
    use_mcts=True,
    mcts_simulations=400,  # Simulazioni moderate
    temperature=0.1
)
```
**Tempo per mossa**: ~7s
**Forza**: Alta

#### Molto Veloce (Policy Diretta)
```python
rl_player = PlayerFactory.create_player(
    "Neural Prime",
    use_mcts=False,      # Nessun MCTS
    temperature=0.1
)
```
**Tempo per mossa**: <1s
**Forza**: Media (dipende da qualità modello)

---

## 🔍 Verifica Disponibilità

### Controlla se il Giocatore è Disponibile

```python
from Players.PlayerFactory import PlayerFactory

# Lista tutti i player disponibili
metadata = PlayerFactory.get_all_player_metadata()
print("Player disponibili:")
for name, info in metadata.items():
    if info.get('enabled'):
        print(f"  - {name}: {info.get('description', '')}")
```

Dovresti vedere:
```
Player disponibili:
  - Neural Prime: Deep Reinforcement Learning player - Neural network trained via self-play reinforcement learning
  - Human Player: You! Play with mouse or keyboard controls
  - Apocalyptron: ...
  - ...
```

### Test Rapido

```python
from Players.PlayerFactory import PlayerFactory
from Reversi.BitboardGame import BitboardGame

# Crea giocatore
try:
    rl_player = PlayerFactory.create_player("Neural Prime")
    print(f"✓ Neural Prime creato: {rl_player.get_name()}")
    
    # Test mossa
    game = BitboardGame()
    legal_moves = game.get_move_list()
    if legal_moves:
        move = rl_player.get_move(game, legal_moves)
        print(f"✓ Mossa generata: {move}")
except Exception as e:
    print(f"✗ Errore: {e}")
```

---

## 🎯 Esempio Completo: Gioca Contro RL

```python
#!/usr/bin/env python3
"""Script per giocare contro il giocatore RL."""

from Players.PlayerFactory import PlayerFactory
from Reversi.BitboardGame import BitboardGame

def play_game():
    """Gioca una partita contro Neural Prime."""
    
    # Crea giocatori
    human_color = 'B'
    rl_color = 'W'
    
    # Crea RL player
    rl_player = PlayerFactory.create_player(
        "Neural Prime",
        use_mcts=True,
        mcts_simulations=400,
        temperature=0.1
    )
    
    # Inizia gioco
    game = BitboardGame()
    move_count = 0
    
    print("=" * 70)
    print("Gioca Contro Neural Prime")
    print("=" * 70)
    print(f"Tu giochi: {human_color}")
    print(f"Neural Prime: {rl_color}")
    print()
    
    while not game.is_finish():
        current_player = game.turn
        legal_moves = game.get_move_list()
        
        if not legal_moves:
            print(f"{current_player} passa")
            game.pass_turn()
            continue
        
        if current_player == human_color:
            # Tua mossa
            print(f"\nTua mossa ({current_player}):")
            print("Mosse legali:", [f"{m.get_x()},{m.get_y()}" for m in legal_moves])
            move_input = input("Mossa (x,y): ")
            try:
                x, y = map(int, move_input.split(','))
                move = next((m for m in legal_moves if m.get_x() == x and m.get_y() == y), None)
                if move:
                    game.move(move)
                    print(f"✓ Giocato: {x},{y}")
                else:
                    print("Mossa non valida!")
                    continue
            except:
                print("Formato non valido!")
                continue
        else:
            # RL mossa
            print(f"\nNeural Prime pensa...")
            move = rl_player.get_move(game, legal_moves)
            if move:
                print(f"RL gioca: {move.get_x()},{move.get_y()}")
                game.move(move)
        
        move_count += 1
    
    # Risultato
    black_count = bin(game.black).count('1')
    white_count = bin(game.white).count('1')
    
    print("\n" + "=" * 70)
    print("Partita Finita!")
    print(f"Black: {black_count}, White: {white_count}")
    if black_count > white_count:
        print("Vincitore: Black" + (" (Tu!)" if human_color == 'B' else ""))
    elif white_count > black_count:
        print("Vincitore: White" + (" (Tu!)" if human_color == 'W' else ""))
    else:
        print("Pareggio!")

if __name__ == "__main__":
    play_game()
```

---

## 🏆 Uso in Torneo

### Configurazione Torneo con RL

```json
{
  "name": "RL vs Others",
  "players": [
    ["Neural Prime", "Neural Prime", null, null, null],
    ["AI", "Apocalyptron", 6, null, null],
    ["AI", "Minimax", 5, null, null]
  ],
  "games_per_matchup": 10
}
```

### Script Torneo

```python
from Players.PlayerFactory import PlayerFactory
from tournament.tournament import Tournament

# Crea giocatori
players = [
    PlayerFactory.create_player("RL Player", use_mcts=True, mcts_simulations=400),
    PlayerFactory.create_player("Apocalyptron", depth=6),
    PlayerFactory.create_player("Minimax", depth=5),
]

# Crea e avvia torneo
tournament = Tournament(players=players, games_per_matchup=10)
results = tournament.run()
print(tournament.generate_report())
```

---

## 🔧 Troubleshooting

### "Model not found"

```python
# Verifica che latest.pth esista
from pathlib import Path
model_path = Path("experimental/checkpoints/latest.pth")
if model_path.exists():
    print(f"✓ Modello trovato: {model_path}")
else:
    print("✗ Modello non trovato. Avvia training prima!")
```

### "RL dependencies not installed"

```bash
# Installa dipendenze
pip install -r experimental/requirements-rl.txt
```

### "Player not found"

```python
# Verifica che PlayerRL sia registrato
from Players.PlayerFactory import PlayerFactory
metadata = PlayerFactory.get_all_player_metadata()
if "Neural Prime" in metadata:
    print("✓ Neural Prime registrato")
else:
    print("✗ Neural Prime non trovato")
```

---

## 📋 Checklist

- [x] PlayerRL creato in `src/Players/PlayerRL.py`
- [x] Integrato in PlayerFactory
- [x] Usa `latest.pth` di default
- [x] Supporta MCTS e policy diretta
- [x] Utilizzabile nella web GUI
- [x] Utilizzabile nei tornei

---

## 🎓 Conclusione

Il giocatore RL è ora **completamente integrato** nel sistema Reversi42!

Puoi:
- ✅ Giocare contro di esso nella web GUI
- ✅ Usarlo nei tornei
- ✅ Configurarlo (MCTS, temperatura, etc.)
- ✅ Usare `latest.pth` automaticamente

**Buon divertimento!** 🚀

