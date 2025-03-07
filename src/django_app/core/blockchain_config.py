from enum import Enum


class BlockchainConfigProvider(Enum):
    ETH_PROVIDER_NAME = "BlockChair"
    BTC_PROVIDER_NAME = "CoinMarketCap"


class BlockchainConfigCurrency(Enum):
    ETH_CURRENCY_NAME = "ETH"
    BTC_CURRENCY_NAME = "BTC"


class BlockchainConfigUrl(Enum):
    ETH_BLOCKCHAIR_URL = "https://api.blockchair.com/ethereum/stats"
    BTC_COINMARKETCAP_URL = "https://pro-api.coinmarketcap.com/v1/blockchain/statistics/latest"
