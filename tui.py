#!/usr/bin/env python3
"""
cppp TUI - Terminal User Interface for cp++
A better version of cp with parallel processing support
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Center
from textual.widgets import Header, Footer, Button, Static, Input, Checkbox, Log, Label, DirectoryTree, RadioButton, RadioSet
from textual.binding import Binding
from textual.screen import ModalScreen
from textual import on
import subprocess
import asyncio
import os
from pathlib import Path


    BINDINGS = [
        Binding("x", "btn_select", "Seç", show=False),
        Binding("escape,z", "btn_cancel", "İptal", show=False),
    ]

    CSS = """
    FilePickerScreen {
        align: center middle;
    }

    #picker-container {
        width: 80;
        height: 30;
        background: #2b3339;
        border: thick #a7c080;
    }

    #picker-title {
        height: 3;
        content-align: center middle;
        background: #a7c080;
        color: #2b3339;
        text-style: bold;
    }

    #picker-path {
        height: 3;
        padding: 0 2;
        background: #232a2e;
        color: #d3c6aa;
        content-align: left middle;
    }

    DirectoryTree {
        height: 1fr;
        background: #232a2e;
        scrollbar-gutter: stable;
    }

    #picker-buttons {
        height: 4;
        align: center middle;
        background: #2b3339;
    }

    #picker-buttons Button {
        margin: 0 1;
        min-width: 15;
    }
    """

    def __init__(self, title: str = "Dosya/Klasör Seç", start_path: str = "."):
        super().__init__()
        self.picker_title = title
        self.start_path = start_path
        self.selected_path = None

    def compose(self) -> ComposeResult:
        with Container(id="picker-container"):
            yield Static(self.picker_title, id="picker-title")
            yield Static(f"📂 {os.path.abspath(self.start_path)}", id="picker-path")
            yield DirectoryTree(self.start_path, id="file_tree")
            with Horizontal(id="picker-buttons"):
                yield Button("✓ Seç", id="btn_select", variant="success")
                yield Button("✗ İptal", id="btn_cancel", variant="error")

    @on(DirectoryTree.FileSelected)
    def on_file_selected(self, event: DirectoryTree.FileSelected) -> None:
        """Update selected path when file is clicked."""
        self.selected_path = str(event.path)
        path_display = self.query_one("#picker-path", Static)
        path_display.update(f"📄 {self.selected_path}")

    @on(DirectoryTree.DirectorySelected)
    def on_directory_selected(self, event: DirectoryTree.DirectorySelected) -> None:
        """Update selected path when directory is clicked."""
        self.selected_path = str(event.path)
        path_display = self.query_one("#picker-path", Static)
        path_display.update(f"📂 {self.selected_path}")

    @on(Button.Pressed, "#btn_select")
    def on_select(self) -> None:
        """Select the current path."""
        if self.selected_path:
            self.dismiss(self.selected_path)
        else:
            self.dismiss(os.path.abspath(self.start_path))

    @on(Button.Pressed, "#btn_cancel")
    def on_cancel(self) -> None:
        """Cancel selection."""
        self.dismiss(None)

    def action_btn_select(self) -> None:
        """Select via keyboard [x]."""
        self.on_select()

    def action_btn_cancel(self) -> None:
        """Cancel via keyboard [z or escape]."""
        self.on_cancel()


class CpppTUI(App):
    """A Textual app for cppp (cp++) - Everforest Theme."""

    CSS = """
    Screen {
        align: center middle;
        background: #1e2326;
    }

    #app-container {
        width: 90;
        height: 40;
        background: #2b3339;
        border: thick #a7c080;
    }

    #title-bar {
        height: 3;
        content-align: center middle;
        background: #a7c080;
        color: #2b3339;
        text-style: bold;
    }

    .section {
        background: #2b3339;
        padding: 0 2 1 2;
        border-bottom: solid #374247;
    }

    .input-row {
        height: 3;
        margin: 1 0 0 0;
        align: left middle;
    }

    .input-label {
        width: 15;
        content-align: left middle;
        color: #d3c6aa;
        text-style: bold;
    }

    Input {
        width: 1fr;
        height: 3;
        background: #232a2e;
        color: #d3c6aa;
        border: solid #4f585e;
    }

    Input:focus {
        border: solid #a7c080;
    }

    Select {
        width: 20;
        height: 3;
        background: #232a2e;
        color: #d3c6aa;
        border: solid #4f585e;
    }

    RadioSet {
        width: auto;
        height: 3;
        background: transparent;
        layout: horizontal;
    }

    RadioButton {
        width: auto;
        height: 3;
        background: #232a2e;
        color: #d3c6aa;
        border: solid #4f585e;
        margin-right: 1;
    }

    RadioButton:focus {
        border: solid #a7c080;
    }

    RadioButton.-selected {
        background: #a7c080;
        color: #2b3339;
    }

    .browse-btn {
        width: 10;
        min-width: 10;
        margin-left: 1;
        background: #7fbbb3;
        color: #2b3339;
    }

    .browse-btn:hover {
        background: #83c092;
    }

    .options-row {
        height: 4;
        align: left middle;
    }

    Checkbox {
        background: transparent;
        color: #d3c6aa;
        margin: 0 2 0 0;
        height: 3;
    }

    #logs-section {
        height: 13;
        padding: 0;
        margin: 0 1;
    }

    #logs-title {
        height: 1;
        background: #dbbc7f;
        color: #2b3339;
        content-align: center middle;
        text-style: bold;
    }

    #progress-section {
        height: 1;
        content-align: center middle;
        background: #272e33;
        color: #a7c080;
        text-style: bold;
    }

    Log {
        height: 11;
        background: #232a2e;
        color: #d3c6aa;
        border: none;
        padding: 0 1;
    }

    #buttons-section {
        height: 4;
        padding: 1 2 0 2;
    }

    #button-container {
        width: 100%;
        height: 3;
        align: center middle;
    }

    Button {
        min-width: 16;
        margin: 0 1;
        height: 3;
    }

    .btn-help {
        background: #7fbbb3;
        color: #2b3339;
    }

    .btn-help:hover {
        background: #83c092;
    }

    .btn-start {
        background: #a7c080;
        color: #2b3339;
    }

    .btn-start:hover {
        background: #b4d292;
    }

    .btn-stop {
        background: #e67e80;
        color: #2b3339;
    }

    .btn-stop:hover {
        background: #ef8a8c;
    }

    Footer {
        background: #374247;
        color: #d3c6aa;
    }

    Header {
        background: #a7c080;
        color: #2b3339;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Çıkış", show=True),
        Binding("ctrl+c", "quit", "Çıkış", show=False),
        Binding("s", "toggle_start", "Başlat/Durdur", show=True),
        Binding("h", "show_help", "Yardım", show=True),
        Binding("i", "focus_input", "Kaynak", show=True),
        Binding("o", "focus_output", "Hedef", show=True),
        Binding("t", "focus_thread", "Thread", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.process = None
        self.process_running = False

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        
        with Container(id="app-container"):
            yield Static("╔═══ cp++ (cppp) Terminal UI ═══╗", id="title-bar")
            
            # Input section
            with Vertical(classes="section"):
                # Mode selection with radio buttons
                with Horizontal(classes="input-row"):
                    yield Label("Mod:", classes="input-label")
                    with RadioSet(id="mode_select"):
                        yield RadioButton("Kopyala", value=True, id="mode_copy")
                        yield RadioButton("Taşı", id="mode_move")
                    yield Label("Thread:", classes="input-label")
                    yield Input(value="4", id="parts")
                
                # Input paths
                with Horizontal(classes="input-row"):
                    yield Label("Kaynak Yolu:", classes="input-label")
                    yield Input(placeholder="Örn: ./dosya.txt veya /tam/yol", id="input_path")
                    yield Button("📁", id="btn_browse_input", classes="browse-btn")
                
                # Output path
                with Horizontal(classes="input-row"):
                    yield Label("Hedef Yolu:", classes="input-label")
                    yield Input(placeholder="Örn: /hedef/klasor/", id="output_path")
                    yield Button("📁", id="btn_browse_output", classes="browse-btn")
            
            # Options section
            with Horizontal(classes="section options-row"):
                yield Checkbox("Detaylı Çıktı (-v)", id="verbose", value=True)
                yield Checkbox("Üzerine Yaz (-f)", id="force")
                yield Checkbox("SHA-256 Kontrolü (-c)", id="checksum")
            
            # Progress section
            yield Static("▶ İşlem Başlamadı", id="progress-section")
            
            # Logs section
            with Vertical(id="logs-section"):
                yield Static("─── İŞLEM KAYITLARI ───", id="logs-title")
                yield Log(id="logs", auto_scroll=True)
            
            # Buttons section
            with Vertical(id="buttons-section"):
                with Horizontal(id="button-container"):
                    yield Button("📖 Yardım", id="btn_help", classes="btn-help")
                    yield Button("▶ İşlemi Başlat", id="btn_start", classes="btn-start")
        
        yield Footer()

    async def on_mount(self) -> None:
        """Called when app is mounted."""
        log = self.query_one("#logs", Log)
        log.write_line("╔════════════════════════════════════════════╗")
        log.write_line("║     cppp TUI - Paralel Kopyalama Aracı    ║")
        log.write_line("╚════════════════════════════════════════════╝")
        log.write_line("")
        log.write_line("🎯 Başlamak için:")
        log.write_line("  1. Kaynak ve hedef yollarını girin")
        log.write_line("  2. Thread sayısını ayarlayın (4-20)")
        log.write_line("  3. '▶ İşlemi Başlat' butonuna basın")
        log.write_line("")
        log.write_line("⌨️  [i] Kaynak | [o] Hedef | [t] Thread")
        log.write_line("    [s] Başlat | [h] Yardım | [q] Çıkış")
        log.write_line("")

    @on(Button.Pressed, "#btn_browse_input")
    def browse_input(self) -> None:
        """Browse for input file/directory."""
        current_path = self.query_one("#input_path", Input).value or "."
        
        def handle_result(result):
            if result:
                self.query_one("#input_path", Input).value = result
        
        self.push_screen(
            FilePickerScreen("Kaynak Dosya/Klasör Seç", current_path),
            handle_result
        )

    @on(Button.Pressed, "#btn_browse_output")
    def browse_output(self) -> None:
        """Browse for output directory."""
        current_path = self.query_one("#output_path", Input).value or "."
        
        def handle_result(result):
            if result:
                self.query_one("#output_path", Input).value = result
        
        self.push_screen(
            FilePickerScreen("Hedef Konum Seç", current_path),
            handle_result
        )

    @on(Button.Pressed, "#btn_help")
    def on_help(self) -> None:
        """Show help."""
        self.action_show_help()

    def action_show_help(self) -> None:
        """Show help information."""
        log = self.query_one("#logs", Log)
        log.clear()
        log.write_line("╔═══════════════════════════════════════════════════════════╗")
        log.write_line("║              cppp - Kullanım Kılavuzu                    ║")
        log.write_line("╚═══════════════════════════════════════════════════════════╝")
        log.write_line("")
        log.write_line("📖 cppp Nedir?")
        log.write_line("   Paralel dosya kopyalama için optimize edilmiş bir araç.")
        log.write_line("   Dosyaları birden fazla parçaya bölerek hızlı kopyalar.")
        log.write_line("")
        log.write_line("🎯 Özellikler:")
        log.write_line("   • Çoklu thread desteği (paralel kopyalama)")
        log.write_line("   • SHA-256 checksum doğrulama")
        log.write_line("   • Gerçek zamanlı ilerleme gösterimi")
        log.write_line("   • Detaylı hata raporlama")
        log.write_line("   • Klasör ve dosya desteği")
        log.write_line("")
        log.write_line("📋 Kullanım Adımları:")
        log.write_line("   1. Mod: copy (kopyala) veya move (taşı)")
        log.write_line("   2. Kaynak: Kopyalanacak dosya/klasör")
        log.write_line("   3. Hedef: Kopyalanacağı yer")
        log.write_line("   4. Thread: İşlemci çekirdek sayınıza göre ayarlayın")
        log.write_line("      • 2-4 çekirdek: 4 thread")
        log.write_line("      • 6-8 çekirdek: 8-12 thread")
        log.write_line("      • 12+ çekirdek: 16-20 thread")
        log.write_line("")
        log.write_line("⚙️  Seçenekler:")
        log.write_line("   • Detaylı Çıktı (-v): İlerleme çubuğu ve hız gösterir")
        log.write_line("   • Üzerine Yaz (-f): Var olan dosyaları değiştirir")
        log.write_line("   • SHA-256 (-c): Kopyalama sonrası bütünlük kontrolü")
        log.write_line("")
        log.write_line("⌨️  Klavye Kısayolları:")
        log.write_line("   [i] → Kaynak yoluna odaklan")
        log.write_line("   [o] → Hedef yoluna odaklan")
        log.write_line("   [t] → Thread sayısına odaklan")
        log.write_line("   [s] → İşlemi Başlat/Durdur")
        log.write_line("   [h] → Bu yardım ekranı")
        log.write_line("   [q] → Çıkış")
        log.write_line("")
        log.write_line("   Dosya Seçici:")
        log.write_line("   [x] → Seçili dosyayı onayla")
        log.write_line("   [z] veya [Esc] → İptal")
        log.write_line("")
        log.write_line("📝 Komut Satırı Örnekleri:")
        log.write_line("   cppp -i dosya.txt -o /hedef/ -p 4 -v")
        log.write_line("   cppp -i /kaynak/klasor -o /yedek/ -p 20 -v -c")
        log.write_line("   cppp -i *.txt -o /hedef/ -p 8 -f")
        log.write_line("")
        log.write_line("🔗 GitHub: https://github.com/kernelginar/cppp")
        log.write_line("📧 Destek: GitHub Issues")
        log.write_line("")
        log.write_line("═══════════════════════════════════════════════════════════")

    @on(Button.Pressed, "#btn_start")
    async def on_start_stop(self) -> None:
        """Start or stop the cppp process."""
        if self.process_running:
            await self.stop_process()
        else:
            await self.start_process()

    async def start_process(self) -> None:
        """Start the cppp process."""
        log = self.query_one("#logs", Log)
        progress = self.query_one("#progress-section", Static)
        button = self.query_one("#btn_start", Button)
        
        # Get input values
        input_path = self.query_one("#input_path", Input).value.strip()
        output_path = self.query_one("#output_path", Input).value.strip()
        parts = self.query_one("#parts", Input).value.strip()
        
        # Get mode from radio buttons
        mode_radio = self.query_one("#mode_select", RadioSet)
        mode = "copy" if mode_radio.pressed_button.id == "mode_copy" else "move"
        
        # Get checkboxes
        verbose = self.query_one("#verbose", Checkbox).value
        force = self.query_one("#force", Checkbox).value
        checksum = self.query_one("#checksum", Checkbox).value
        
        # Validate inputs
        if not input_path:
            log.write_line("")
            log.write_line("❌ HATA: Kaynak yolu boş olamaz!")
            log.write_line("   Lütfen kaynak dosya veya klasör yolu girin.")
            return
        
        if not output_path:
            log.write_line("")
            log.write_line("❌ HATA: Hedef yolu boş olamaz!")
            log.write_line("   Lütfen hedef klasör yolu girin.")
            return
        
        # Validate parts
        try:
            parts_int = int(parts) if parts else 1
            if parts_int < 1:
                log.write_line("")
                log.write_line("❌ HATA: Thread sayısı 1'den küçük olamaz!")
                return
            if parts_int > 50:
                log.write_line("")
                log.write_line("⚠️  UYARI: Çok yüksek thread sayısı performansı düşürebilir!")
                log.write_line("   Önerilen: 4-20 arası")
        except ValueError:
            log.write_line("")
            log.write_line("❌ HATA: Thread sayısı geçerli bir sayı olmalı!")
            return
        
        # Find cppp binary
        cppp_paths = ["./build/cppp", "./cppp", "cppp"]
        cppp_bin = None
        for path in cppp_paths:
            if os.path.exists(path) or path == "cppp":
                cppp_bin = path
                break
        
        if not cppp_bin:
            log.write_line("")
            log.write_line("❌ HATA: cppp binary bulunamadı!")
            log.write_line("")
            log.write_line("Kurulum için:")
            log.write_line("  cd build")
            log.write_line("  cmake ..")
            log.write_line("  make")
            return
        
        # Build command
        cmd = [cppp_bin]
        if mode and mode != "copy":
            cmd.extend(["-m", mode])
        cmd.extend(["-i", input_path])
        cmd.extend(["-o", output_path])
        if parts:
            cmd.extend(["-p", parts])
        if verbose:
            cmd.append("-v")
        if force:
            cmd.append("-f")
        if checksum:
            cmd.append("-c")
        
        log.clear()
        log.write_line("═══════════════════════════════════════════════════════════")
        log.write_line("🚀 cppp İşlemi Başlatıldı")
        log.write_line("═══════════════════════════════════════════════════════════")
        log.write_line("")
        log.write_line("📌 Komut: " + " ".join(cmd))
        log.write_line("")
        log.write_line("─────────────────────────────────────────────────────────")
        
        try:
            # Update UI
            self.process_running = True
            button.label = "⏹ İşlemi Durdur"
            button.remove_class("btn-start")
            button.add_class("btn-stop")
            progress.update("▶ İşlem Devam Ediyor...")
            
            # Run the process
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.process = process
            
            # Read output
            async def read_stream(stream, prefix=""):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    log.write_line(prefix + line.decode().strip())
            
            await asyncio.gather(
                read_stream(process.stdout),
                read_stream(process.stderr, "⚠️  ")
            )
            
            await process.wait()
            
            log.write_line("")
            log.write_line("─────────────────────────────────────────────────────────")
            if process.returncode == 0:
                log.write_line("✅ İşlem Başarıyla Tamamlandı!")
                log.write_line("   Tüm dosyalar başarıyla kopyalandı.")
                progress.update("✅ İşlem Tamamlandı")
            else:
                log.write_line(f"❌ İşlem Başarısız! (Çıkış Kodu: {process.returncode})")
                log.write_line("   Lütfen yukarıdaki hata mesajlarını kontrol edin.")
                progress.update("❌ İşlem Başarısız")
            log.write_line("═══════════════════════════════════════════════════════════")
            
        except FileNotFoundError:
            log.write_line("")
            log.write_line("═══════════════════════════════════════════════════════════")
            log.write_line("❌ HATA: cppp bulunamadı!")
            log.write_line("═══════════════════════════════════════════════════════════")
            log.write_line("")
            log.write_line("cppp'yi kurmak için:")
            log.write_line("  1. git clone https://github.com/kernelginar/cppp")
            log.write_line("  2. cd cppp && mkdir build && cd build")
            log.write_line("  3. cmake .. && make")
            log.write_line("  4. sudo make install  (veya PATH'e ekleyin)")
            log.write_line("")
            progress.update("❌ cppp Bulunamadı")
        except Exception as e:
            log.write_line("")
            log.write_line("═══════════════════════════════════════════════════════════")
            log.write_line(f"❌ Beklenmeyen Hata: {str(e)}")
            log.write_line("═══════════════════════════════════════════════════════════")
            log.write_line("")
            progress.update("❌ Hata Oluştu")
        finally:
            self.process_running = False
            button.label = "▶ İşlemi Başlat"
            button.remove_class("btn-stop")
            button.add_class("btn-start")
            self.process = None

    async def stop_process(self) -> None:
        """Stop the running cppp process."""
        log = self.query_one("#logs", Log)
        progress = self.query_one("#progress-section", Static)
        button = self.query_one("#btn_start", Button)
        
        if self.process:
            log.write_line("")
            log.write_line("⏹️  İşlem durduruluyor...")
            self.process.terminate()
            try:
                await asyncio.wait_for(self.process.wait(), timeout=5.0)
                log.write_line("✅ İşlem başarıyla durduruldu.")
            except asyncio.TimeoutError:
                log.write_line("⚠️  İşlem yanıt vermiyor, zorla sonlandırılıyor...")
                self.process.kill()
                await self.process.wait()
                log.write_line("✅ İşlem zorla sonlandırıldı.")
            progress.update("⏹ İşlem Durduruldu")
        
        self.process_running = False
        button.label = "▶ İşlemi Başlat"
        button.remove_class("btn-stop")
        button.add_class("btn-start")

    def action_toggle_start(self) -> None:
        """Toggle start/stop via keyboard."""
        button = self.query_one("#btn_start", Button)
        button.press()

    def action_focus_input(self) -> None:
        """Focus on input path."""
        self.query_one("#input_path", Input).focus()

    def action_focus_output(self) -> None:
        """Focus on output path."""
        self.query_one("#output_path", Input).focus()

    def action_focus_thread(self) -> None:
        """Focus on thread input."""
        self.query_one("#parts", Input).focus()


def main():
    """Run the app."""
    app = CpppTUI()
    app.run()


if __name__ == "__main__":
    main()