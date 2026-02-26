from __future__ import annotations

import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from textual.app import App
from textual.binding import Binding
from textual.reactive import Reactive, reactive
from textual.signal import Signal

from elia_chat.chats_manager import ChatsManager
from elia_chat.models import ChatData, ChatMessage
from elia_chat.config import EliaChatModel, LaunchConfig
from elia_chat.runtime_config import RuntimeConfig
from elia_chat.screens.chat_screen import ChatScreen
from elia_chat.screens.help_screen import HelpScreen
from elia_chat.screens.home_screen import HomeScreen
from elia_chat.themes import BUILTIN_THEMES, Theme, load_user_themes

if TYPE_CHECKING:
    from litellm.types.completion import (
        ChatCompletionUserMessageParam,
        ChatCompletionSystemMessageParam,
    )


class Elia(App[None]):
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = Path(__file__).parent / "elia.scss"
    BINDINGS = [
        Binding("q", "app.quit", "Quit", show=False),
        Binding("f1,?", "help", "Help"),
    ]

    def __init__(self, config: LaunchConfig, startup_prompt: str = ""):
        self.launch_config = config

        available_themes: dict[str, Theme] = BUILTIN_THEMES.copy()
        available_themes |= load_user_themes()

        self.themes: dict[str, Theme] = available_themes

        self._runtime_config = RuntimeConfig(
            selected_model=config.default_model_object,
            system_prompt=config.system_prompt,
        )
        self.runtime_config_signal = Signal[RuntimeConfig](
            self, "runtime-config-updated"
        )
        """Widgets can subscribe to this signal to be notified of
        when the user has changed configuration at runtime (e.g. using the UI)."""

        self.startup_prompt = startup_prompt
        """Elia can be launched with a prompt on startup via a command line option.

        This is a convenience which will immediately load the chat interface and
        put users into the chat window, rather than going to the home screen.
        """

        # Store the config theme for use in on_mount
        self._config_theme = config.theme or "nebula"
        super().__init__()

    theme: Reactive[str] = reactive("textual-dark", init=False)

    @property
    def runtime_config(self) -> RuntimeConfig:
        return self._runtime_config

    @runtime_config.setter
    def runtime_config(self, new_runtime_config: RuntimeConfig) -> None:
        self._runtime_config = new_runtime_config
        self.runtime_config_signal.publish(self.runtime_config)

    def _validate_theme(self, theme_name: str) -> str:
        """Override to allow custom themes that aren't registered with Textual."""
        if theme_name in self.themes:
            return theme_name
        # Fall back to Textual's validation for built-in themes
        return super()._validate_theme(theme_name)

    @property
    def current_theme(self):
        """Override to return our custom theme object."""
        theme_name = self.theme
        if theme_name in self.themes:
            return self.themes[theme_name]
        # Fall back to Textual's current_theme for built-in themes
        return super().current_theme

    async def on_mount(self) -> None:
        await self.push_screen(HomeScreen(self.runtime_config_signal))
        self.theme = self._config_theme
        if self.startup_prompt:
            await self.launch_chat(
                prompt=self.startup_prompt,
                model=self.runtime_config.selected_model,
            )

    async def launch_chat(self, prompt: str, model: EliaChatModel) -> None:
        current_time = datetime.datetime.now(datetime.timezone.utc)
        system_message: ChatCompletionSystemMessageParam = {
            "content": self.runtime_config.system_prompt,
            "role": "system",
        }
        user_message: ChatCompletionUserMessageParam = {
            "content": prompt,
            "role": "user",
        }
        chat = ChatData(
            id=None,
            title=None,
            create_timestamp=None,
            model=model,
            messages=[
                ChatMessage(
                    message=system_message,
                    timestamp=current_time,
                    model=model,
                ),
                ChatMessage(
                    message=user_message,
                    timestamp=current_time,
                    model=model,
                ),
            ],
        )
        chat.id = await ChatsManager.create_chat(chat_data=chat)
        await self.push_screen(ChatScreen(chat))

    async def action_help(self) -> None:
        if isinstance(self.screen, HelpScreen):
            self.pop_screen()
        else:
            await self.push_screen(HelpScreen())

    def get_css_variables(self) -> dict[str, str]:
        theme = self.current_theme
        if hasattr(theme, 'to_color_system'):
            # Our custom Theme object
            color_system = theme.to_color_system()
            css_vars = color_system.generate()
            # Add any custom CSS variables from the theme
            if theme.variables:
                css_vars.update(theme.variables)
            return css_vars
        else:
            # Textual's built-in ColorSystem
            return theme.generate()

    def watch_theme(self, theme: str) -> None:
        self.refresh_css(animate=False)

    @property
    def theme_object(self) -> Theme | None:
        try:
            return self.themes[self.theme]
        except KeyError:
            return None


if __name__ == "__main__":
    app = Elia(LaunchConfig())
    app.run()
