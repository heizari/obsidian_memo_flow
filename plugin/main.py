from pathlib import Path
from datetime import datetime
import shutil
from flox import Flox

class ObsidianDailyNote(Flox):
    def __init__(self):
        super().__init__()

    @property
    def vault_path(self):
        """Get vault path from settings or default"""
        custom_path = self.settings.get("vault_path", "").strip()
        if custom_path:
            return Path(custom_path)
        else:
            vault_name = self.settings.get("vault_name", "obsidian_vault")
            return Path.home() / vault_name

    @property
    def daily_note_dir(self):
        return self.settings.get("daily_note_dir", "002_daily_note")

    @property
    def template_dir(self):
        return self.settings.get("template_dir", "004_template")

    @property
    def template_filename(self):
        return self.settings.get("template_filename", "daily_note.md")

    def query(self, query):
        if not query.strip():
            return [self.add_item(
                title="Enter your note",
                subtitle="Type something to add to today's daily note"
            )]

        results = []

        # Main action to add note
        results.append(self.add_item(
            title=f"Add to daily note: {query}",
            subtitle=f"Will append to {datetime.now().strftime('%Y-%m-%d')}.md with timestamp",
            method=self.add_to_daily_note,
            parameters=[query]
        ))

        return results

    def add_to_daily_note(self, content):
        try:
            # Validate vault path
            if not self.vault_path.exists():
                self.show_msg("Error", f"Vault path does not exist: {self.vault_path}")
                return

            # Generate file paths
            today = datetime.now().strftime('%Y-%m-%d')
            daily_note_path = self.vault_path / self.daily_note_dir / f"{today}.md"
            template_path = self.vault_path / self.template_dir / self.template_filename

            # Create daily note from template if it doesn't exist
            if not daily_note_path.exists():
                # Create directory if it doesn't exist
                daily_note_path.parent.mkdir(parents=True, exist_ok=True)

                assert template_path.exists(), f"{template_path=} is not exists."
                if template_path.exists():
                    shutil.copy2(template_path, daily_note_path)
                    message = "デイリーノートをテンプレートから作成しました"
                else:
                    # Create empty file if template doesn't exist
                    with open(daily_note_path, 'w', encoding='utf-8') as f:
                        f.write(f"# {today}\n\n")
                    message = "Create daily note."
            else:
                message = "Add memo: "

            # Format and append content
            timestamp = datetime.now().strftime('%H:%M')
            formatted_content = f"\n- {timestamp} {content}"

            with open(daily_note_path, 'a', encoding='utf-8') as f:
                f.write(formatted_content)

            # Show success message
            self.show_msg("Success", f"{message}: {content}")

        except Exception as e:
            self.show_msg("Error", f"Failed to add note: {str(e)}")

    def context_menu(self, data):
        return [self.add_item(
            title="Open daily note",
            subtitle="Open today's daily note in Obsidian",
            method=self.open_daily_note,
            parameters=[]
        )]

    def open_daily_note(self):
        try:
            import os
            today = datetime.now().strftime('%Y-%m-%d')
            daily_note_path = self.vault_path / self.daily_note_dir / f"{today}.md"

            if daily_note_path.exists():
                # Open with default application (should be Obsidian if configured)
                os.startfile(daily_note_path)
            else:
                self.show_msg("Error", "Daily note doesn't exist yet")

        except Exception as e:
            self.show_msg("Error", f"Failed to open daily note: {str(e)}")

    def reload_plugin(self):
        """Reload plugin settings"""
        self.show_msg("Info", "Plugin settings reloaded")

if __name__ == "__main__":
    ObsidianDailyNote()
