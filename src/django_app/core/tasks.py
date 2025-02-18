import requests
from celery import shared_task
from django.utils.timezone import now

from django_app.core.blockchain_config import BlockchainConfigUrl, BlockchainConfigCurrency, BlockchainConfigProvider
from django_app.core.models import Currency, Provider, Block


class BlockchainService:

    @staticmethod
    @shared_task
    def fetch_btc_block() -> str:
        """
        Fetches the latest Bitcoin block from CoinMarketCap and stores it in the database.
        """
        currency, _ = Currency.objects.get_or_create(name=BlockchainConfigCurrency.BTC_CURRENCY_NAME.value)
        provider, _ = Provider.objects.get_or_create(name=BlockchainConfigProvider.BTC_PROVIDER_NAME.value)

        if not provider.api_key:
            return "Skipping BTC block fetch: Missing API Key for CoinMarketCap"

        headers = {"X-CMC_PRO_API_KEY": provider.api_key}
        params = {"symbol": BlockchainConfigCurrency.BTC_CURRENCY_NAME.value}
        response = requests.get(BlockchainConfigUrl.BTC_COINMARKETCAP_URL.value, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()

            latest_block_number = data["data"]["BTC"]["total_blocks"]
            created_at_timestamp = data["status"].get("timestamp")

            Block.objects.update_or_create(
                currency=currency,
                provider=provider,
                block_number=latest_block_number,
                defaults={
                    "created_at": created_at_timestamp,
                    "stored_at": now(),
                },
            )
            return f"BTC Block {latest_block_number} stored."

        return f"Failed to fetch BTC block: {response.status_code} - {response.text}"

    @staticmethod
    @shared_task
    def fetch_eth_block() -> str:
        """
        Fetches the latest Ethereum block from BlockChair and stores it in the database.
        """
        response = requests.get(BlockchainConfigUrl.ETH_BLOCKCHAIR_URL.value)

        if response.status_code == 200:
            data = response.json()

            latest_block_number = data["data"]["best_block_height"]
            created_at_timestamp = data["data"].get("best_block_time")

            currency, _ = Currency.objects.get_or_create(name=BlockchainConfigCurrency.ETH_CURRENCY_NAME.value)
            provider, _ = Provider.objects.get_or_create(name=BlockchainConfigProvider.ETH_PROVIDER_NAME.value)

            Block.objects.update_or_create(
                currency=currency,
                provider=provider,
                block_number=latest_block_number,
                defaults={
                    "created_at": created_at_timestamp,
                    "stored_at": now(),
                },
            )
            return f"ETH Block {latest_block_number} stored."

        return "Failed to fetch ETH block."


@shared_task
def fetch_latest_blocks():
    """
    Scheduled task to fetch BTC and ETH blocks.
    """
    BlockchainService.fetch_eth_block.apply_async()
    BlockchainService.fetch_btc_block.apply_async()
