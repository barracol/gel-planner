#!/usr/bin/env python3
"""Simple command-line gel planner for running and training sessions."""

import math
import re


def parse_pace(value: str) -> float:
    """Return pace in minutes/km. Accepts 4:30, 4m30s, or 4.5."""
    text = value.strip().lower().replace(" ", "")
    match = re.fullmatch(r"(\d+)(?::|m)(\d{1,2})s?", text)
    if not match:
        match = re.fullmatch(r"(\d+)\.(\d{2})", text)
    if match:
        minutes, seconds = map(int, match.groups())
        if seconds >= 60:
            raise ValueError("i secondi devono essere inferiori a 60")
        return minutes + seconds / 60
    try:
        pace = float(text.replace(",", "."))
    except ValueError as exc:
        raise ValueError("usa ad esempio 4:30 oppure 4m30s") from exc
    if pace <= 0:
        raise ValueError("il passo deve essere maggiore di zero")
    return pace


def format_duration(minutes: float) -> str:
    total_seconds = round(minutes * 60)
    hours, remainder = divmod(total_seconds, 3600)
    mins, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours}h {mins:02d}min"
    if seconds:
        return f"{mins}min {seconds:02d}s"
    return f"{mins}min"


def suggested_gels(total_minutes: float) -> int:
    """Suggest one gel at minute 25, then one every 40 minutes."""
    if total_minutes < 50:
        return 0
    return math.floor((total_minutes - 25) / 40) + 1


def build_plan(distance_km: float, pace_min_per_km: float, count: int):
    total_minutes = distance_km * pace_min_per_km
    if count <= 0 or total_minutes <= 25:
        return []
    # Keep the first gel at 25 minutes and the last one about 15 minutes
    # before the finish; distribute a user-selected number evenly between them.
    first = 25
    last = max(first, total_minutes - 15)
    if count == 1:
        times = [first]
    else:
        step = (last - first) / (count - 1)
        times = [round(first + step * index) for index in range(count)]
    return [
        (index + 1, minute, min(distance_km, minute / pace_min_per_km))
        for index, minute in enumerate(times)
    ]


def ask_number(prompt: str, minimum: float = 0) -> float:
    while True:
        try:
            number = float(input(prompt).strip().replace(",", "."))
            if number <= minimum:
                raise ValueError
            return number
        except ValueError:
            print(f"Inserisci un numero maggiore di {minimum}.")


def main() -> None:
    print("Gel planner\n")
    distance = ask_number("Quanti km? ")
    while True:
        try:
            pace = parse_pace(input("Qual è il passo (min/km, es. 4:30)? "))
            break
        except ValueError as error:
            print(f"Passo non valido: {error}")

    total = distance * pace
    suggestion = suggested_gels(total)
    print(f"\nTempo stimato: {format_duration(total)}")
    print(f"Suggerimento: {suggestion} gel (circa uno ogni 40 minuti, primo al minuto 25).")
    answer = input(f"Quanti gel vuoi pianificare? [Invio = {suggestion}] ").strip()
    if answer:
        try:
            count = max(0, int(answer))
        except ValueError:
            print("Numero non valido: uso il suggerimento.")
            count = suggestion
    else:
        count = suggestion

    plan = build_plan(distance, pace, count)
    print("\nPiano:")
    if not plan:
        print("- Nessun gel pianificato per questa durata.")
    else:
        for number, minute, km in plan:
            print(f"- {number}° gel al minuto {minute} ({format_duration(minute)}) -> km {km:.1f}")
    print("\nNota: è una stima generale; adatta il piano alla tua tolleranza e alle indicazioni del produttore.")


if __name__ == "__main__":
    main()
