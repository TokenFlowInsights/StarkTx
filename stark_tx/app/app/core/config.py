import secrets
from enum import Enum, EnumMeta

from pydantic import AnyHttpUrl, BaseSettings

from app.base_exceptions import NotSupportedChainError


class Settings(BaseSettings):

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # StarkNet environments
    SEQUENCERS = dict()
    SEQUENCERS['mainnet']: AnyHttpUrl = "https://alpha-mainnet.starknet.io/feeder_gateway"
    SEQUENCERS['testnet']: AnyHttpUrl = "https://alpha4.starknet.io/feeder_gateway"
    SEQUENCERS['integration']: AnyHttpUrl = "https://external.integration.starknet.io/feeder_gateway"

    DEFAULT_SEQUENCER_URL: AnyHttpUrl = SEQUENCERS['mainnet']

    PROJECT_NAME: str

    class Config:
        case_sensitive = True
        use_enum_values = True


settings = Settings()


class EnumValidator(EnumMeta):
    def __getitem__(cls, name):
        try:
            if not name:
                return super().__getitem__("DEFAULT")
            return super().__getitem__(name)
        except KeyError:
            raise NotSupportedChainError(name)


class SequencerURL(str, Enum, metaclass=EnumValidator):

    DEFAULT = settings.DEFAULT_SEQUENCER_URL

    mainnet = settings.SEQUENCERS['mainnet']
    testnet = settings.SEQUENCERS['testnet']
    integration = settings.SEQUENCERS['integration']
