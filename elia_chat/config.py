import os
from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, SecretStr


class EliaChatModel(BaseModel):
    name: str
    """The name of the model e.g. `gpt-3.5-turbo`.
    This must match the name of the model specified by the provider.
    """
    id: str | None = None
    """If you have multiple versions of the same model (e.g. a personal
    OpenAI gpt-3.5 and a work OpenAI gpt-3.5 with different API keys/org keys),
    you need to be able to refer to them. For example, when setting the `default_model`
    key in the config, if you write `gpt-3.5`, there's no way to know whether you
    mean your work or your personal `gpt-3.5`. That's where `id` comes in."""
    display_name: str | None = None
    """The display name of the model in the UI."""
    provider: str | None = None
    """The provider of the model, e.g. openai, anthropic, etc"""
    api_key: SecretStr | None = None
    """If set, this will be used in place of the environment variable that
    would otherwise be used for this model (instead of OPENAI_API_KEY,
    ANTHROPIC_API_KEY, etc.)."""
    api_base: AnyHttpUrl | None = None
    """If set, this will be used as the base URL for making API calls.
    This can be useful if you're hosting models on a LocalAI server, for
    example."""
    organization: str | None = None
    """Some providers, such as OpenAI, allow you to specify an organization.
    In the case of """
    description: str | None = Field(default=None)
    """A description of the model which may appear inside the Elia UI."""
    product: str | None = Field(default=None)
    """For example `ChatGPT`, `Claude`, `Gemini`, etc."""
    temperature: float = Field(default=1.0)
    """The temperature to use. Low temperature means the same prompt is likely
    to produce similar results. High temperature means a flatter distribution
    when predicting the next token, and so the next token will be more random.
    Setting a very high temperature will likely produce junk output."""
    max_retries: int = Field(default=0)
    """The number of times to retry a request after it fails before giving up."""

    @property
    def lookup_key(self) -> str:
        return self.id or self.name


def get_builtin_openai_models() -> list[EliaChatModel]:
    return [
        # GPT-4o series
        EliaChatModel(
            id="elia-gpt-4o",
            name="gpt-4o",
            display_name="GPT-4o",
            provider="OpenAI",
            product="ChatGPT",
            description="Fastest and most affordable flagship model.",
            temperature=0.7,
        ),
        EliaChatModel(
            id="elia-gpt-4o-mini",
            name="gpt-4o-mini",
            display_name="GPT-4o Mini",
            provider="OpenAI",
            product="ChatGPT",
            description="Fast, affordable small model for focused tasks.",
            temperature=0.7,
        ),
        # GPT-4.1 series
        EliaChatModel(
            id="elia-gpt-4.1",
            name="gpt-4.1",
            display_name="GPT-4.1",
            provider="OpenAI",
            product="ChatGPT",
            description="Most capable GPT-4 series model for complex tasks.",
            temperature=0.7,
        ),
        EliaChatModel(
            id="elia-gpt-4.1-mini",
            name="gpt-4.1-mini",
            display_name="GPT-4.1 Mini",
            provider="OpenAI",
            product="ChatGPT",
            description="Beats GPT-4o on many benchmarks, efficient small model.",
            temperature=0.7,
        ),
        EliaChatModel(
            id="elia-gpt-4.1-nano",
            name="gpt-4.1-nano",
            display_name="GPT-4.1 Nano",
            provider="OpenAI",
            product="ChatGPT",
            description="Smallest and fastest GPT-4.1 model.",
            temperature=0.7,
        ),
        # o1 reasoning series
        EliaChatModel(
            id="elia-o1",
            name="o1",
            display_name="o1",
            provider="OpenAI",
            product="ChatGPT",
            description="Advanced reasoning model for STEM and complex tasks.",
            temperature=1.0,
        ),
        EliaChatModel(
            id="elia-o1-mini",
            name="o1-mini",
            display_name="o1 Mini",
            provider="OpenAI",
            product="ChatGPT",
            description="Faster reasoning model for focused STEM tasks.",
            temperature=1.0,
        ),
        EliaChatModel(
            id="elia-o1-pro",
            name="o1-pro",
            display_name="o1 Pro",
            provider="OpenAI",
            product="ChatGPT",
            description="Most powerful reasoning model for expert-level tasks.",
            temperature=1.0,
        ),
        # o3 reasoning series
        EliaChatModel(
            id="elia-o3",
            name="o3",
            display_name="o3",
            provider="OpenAI",
            product="ChatGPT",
            description="Next-generation reasoning model.",
            temperature=1.0,
        ),
        EliaChatModel(
            id="elia-o3-pro",
            name="o3-pro",
            display_name="o3 Pro",
            provider="OpenAI",
            product="ChatGPT",
            description="Most advanced reasoning model available.",
            temperature=1.0,
        ),
        # o4-mini reasoning series
        EliaChatModel(
            id="elia-o4-mini",
            name="o4-mini",
            display_name="o4 Mini",
            provider="OpenAI",
            product="ChatGPT",
            description="Fast reasoning model with advanced capabilities.",
            temperature=1.0,
        ),
        EliaChatModel(
            id="elia-o4-mini-high",
            name="o4-mini-high",
            display_name="o4 Mini High",
            provider="OpenAI",
            product="ChatGPT",
            description="Higher capability version of o4-mini.",
            temperature=1.0,
        ),
        # Legacy models
        EliaChatModel(
            id="elia-gpt-4-turbo",
            name="gpt-4-turbo",
            display_name="GPT-4 Turbo",
            provider="OpenAI",
            product="ChatGPT",
            description="Previous high-intelligence model.",
            temperature=0.7,
        ),
        EliaChatModel(
            id="elia-gpt-3.5-turbo",
            name="gpt-3.5-turbo",
            display_name="GPT-3.5 Turbo",
            provider="OpenAI",
            product="ChatGPT",
            description="Fast & inexpensive model for simple tasks.",
            temperature=0.7,
        ),
    ]


def get_builtin_anthropic_models() -> list[EliaChatModel]:
    return [
        # Claude 4 series
        EliaChatModel(
            id="elia-claude-opus-4",
            name="claude-opus-4-20250514",
            display_name="Claude Opus 4",
            provider="Anthropic",
            product="Claude 4",
            description="Most intelligent model for building agents and coding.",
        ),
        EliaChatModel(
            id="elia-claude-sonnet-4",
            name="claude-sonnet-4-20250514",
            display_name="Claude Sonnet 4",
            provider="Anthropic",
            product="Claude 4",
            description="Best combination of speed and intelligence.",
        ),
        # Claude 3.7 series
        EliaChatModel(
            id="elia-claude-3-7-sonnet",
            name="claude-3-7-sonnet-20250219",
            display_name="Claude 3.7 Sonnet",
            provider="Anthropic",
            product="Claude 3.7",
            description="Most intelligent Claude 3 series model.",
        ),
        # Claude 3.5 series
        EliaChatModel(
            id="elia-claude-3-5-sonnet",
            name="claude-3-5-sonnet-20241022",
            display_name="Claude 3.5 Sonnet (Latest)",
            provider="Anthropic",
            product="Claude 3.5",
            description="Anthropic's most intelligent model - latest version.",
        ),
        EliaChatModel(
            id="elia-claude-3-5-sonnet-20240620",
            name="claude-3-5-sonnet-20240620",
            display_name="Claude 3.5 Sonnet (Jun 2024)",
            provider="Anthropic",
            product="Claude 3.5",
            description="Anthropic's most intelligent model - earlier version.",
        ),
        EliaChatModel(
            id="elia-claude-3-5-haiku",
            name="claude-3-5-haiku-20241022",
            display_name="Claude 3.5 Haiku",
            provider="Anthropic",
            product="Claude 3.5",
            description="Fastest model with near-frontier intelligence.",
        ),
        # Claude 3 series (legacy)
        EliaChatModel(
            id="elia-claude-3-opus",
            name="claude-3-opus-20240229",
            display_name="Claude 3 Opus",
            provider="Anthropic",
            product="Claude 3",
            description="Excels at writing and complex tasks.",
        ),
        EliaChatModel(
            id="elia-claude-3-sonnet",
            name="claude-3-sonnet-20240229",
            display_name="Claude 3 Sonnet",
            provider="Anthropic",
            product="Claude 3",
            description="Ideal balance of intelligence and speed.",
        ),
        EliaChatModel(
            id="elia-claude-3-haiku",
            name="claude-3-haiku-20240307",
            display_name="Claude 3 Haiku",
            provider="Anthropic",
            product="Claude 3",
            description="Fastest and most compact for quick responses.",
        ),
    ]


def get_builtin_google_models() -> list[EliaChatModel]:
    return [
        # Gemini 2.5 series
        EliaChatModel(
            id="elia-gemini-2.5-pro",
            name="gemini/gemini-2.5-pro",
            display_name="Gemini 2.5 Pro",
            provider="Google",
            product="Gemini",
            description="Most capable Gemini model for complex reasoning tasks.",
        ),
        EliaChatModel(
            id="elia-gemini-2.5-flash",
            name="gemini/gemini-2.5-flash",
            display_name="Gemini 2.5 Flash",
            provider="Google",
            product="Gemini",
            description="Fast and versatile model for a wide range of tasks.",
        ),
        EliaChatModel(
            id="elia-gemini-2.5-flash-lite",
            name="gemini/gemini-2.5-flash-lite",
            display_name="Gemini 2.5 Flash Lite",
            provider="Google",
            product="Gemini",
            description="Most efficient model for high-frequency, simple tasks.",
        ),
        # Gemini 2.0 series
        EliaChatModel(
            id="elia-gemini-2.0-flash",
            name="gemini/gemini-2.0-flash",
            display_name="Gemini 2.0 Flash",
            provider="Google",
            product="Gemini",
            description="Fast multimodal model with native tool use.",
        ),
        EliaChatModel(
            id="elia-gemini-2.0-flash-lite",
            name="gemini/gemini-2.0-flash-lite",
            display_name="Gemini 2.0 Flash Lite",
            provider="Google",
            product="Gemini",
            description="Lightweight model for simple, high-volume tasks.",
        ),
    ]


def get_builtin_models() -> list[EliaChatModel]:
    return (
        get_builtin_openai_models()
        + get_builtin_anthropic_models()
        + get_builtin_google_models()
    )


class LaunchConfig(BaseModel):
    """The config of the application at launch.

    Values may be sourced via command line options, env vars, config files.
    """

    model_config = ConfigDict(frozen=True)

    default_model: str = Field(default="elia-gpt-4o-mini")
    """The ID or name of the default model."""
    system_prompt: str = Field(
        default=os.getenv(
            "ELIA_SYSTEM_PROMPT", "You are a helpful assistant named Elia."
        )
    )
    message_code_theme: str = Field(default="monokai")
    """The default Pygments syntax highlighting theme to be used in chatboxes."""
    models: list[EliaChatModel] = Field(default_factory=list)
    builtin_models: list[EliaChatModel] = Field(
        default_factory=get_builtin_models, init=False
    )
    theme: str = Field(default="nebula")

    @property
    def all_models(self) -> list[EliaChatModel]:
        return self.models + self.builtin_models

    @property
    def default_model_object(self) -> EliaChatModel:
        from elia_chat.models import get_model

        return get_model(self.default_model, self)

    @classmethod
    def get_current(cls) -> "LaunchConfig":
        return cls()
