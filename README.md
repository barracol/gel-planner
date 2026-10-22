# Gel planner

Piccolo planner da terminale, senza dipendenze esterne.

```bash
cd /Users/leonardobarraco/Documents/Codex/gel-planner
python3 gel_planner.py
```

Il passo accetta formati come `4:30`, `4m30s` o `4.5`. La regola predefinita propone un gel al minuto 25 e poi ogni 40 minuti; il numero può essere modificato durante l’inserimento.

Test:

```bash
python3 -m unittest -v
```
