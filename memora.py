# main.py - Memora v1.0 - Your lifelong private memory
import threading
import time
from datetime import datetime
from rich.console import Console
from capture.audio import AudioCapturer
from capture.screen import ScreenCapturer
from capture.webcam import WebcamCapturer
from db.init import init_db
from db.search import recall
from ingest.transcribe import transcribe_audio
from ingest.ocr import ocr_screen
from ingest.embed import embed_text, embed_image

console = Console()
console.clear()
console.print("[bold magenta]Memora v1.0 — Total Recall Activated[/bold magenta]")
console.print("[dim]All data stays on your machine. Forever. Encrypted.[/dim]\n")

init_db()

# Start capture threads
audio = AudioCapturer()
screen = ScreenCapturer()
webcam = WebcamCapturer()

audio.start()
screen.start()
webcam.start()

console.print("Capturing audio, screen, and life...")
console.print("Type 'recall <query>' to search your past. Type 'quit' to stop.\n")

try:
    while True:
        query = input("> ").strip()
        if query.lower() == "quit":
            break
        if query.startswith("recall "):
            q = query[7:]
            console.print(f"[yellow]Searching your entire life for:[/yellow] {q}")
            results = recall(q, limit=8)
            for dist, ts, kind, content in results:
                ago = time.strftime("%b %d %Y", time.localtime(ts))
                console.print(f"[green]{ago}[/green] [{kind}] {content[:120]}{'...' if len(content)>120 else ''}")
except KeyboardInterrupt:
    pass
finally:
    audio.stop()
    screen.stop()
    webcam.stop()
    console.print("\n[bold red]Memora stopped. Your life is safe. Forever yours.[/bold red]")
