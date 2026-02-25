from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from rich.text import Text as RichText
from textual.screen import ModalScreen
from textual.widgets import Input


class RenameChat(ModalScreen[str]):
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Cancel", key_display="esc"),
        Binding("enter", "app.pop_screen", "Save"),
    ]

    def compose(self) -> ComposeResult:
        with Vertical():
            title_input = Input(placeholder="Enter a title...")

            rich_text = RichText()
            rich_text.append("[")
            rich_text.append("enter", style="#FFFFFF")
            rich_text.append("]")
            rich_text.append(" Save  ")
            rich_text.append("[")
            rich_text.append("esc", style="#FFFFFF")
            rich_text.append("]")
            rich_text.append(" Cancel")
            
            title_input.border_subtitle = rich_text

            yield title_input

    @on(Input.Submitted)
    def close_screen(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)
