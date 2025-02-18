from django.core.paginator import Paginator, EmptyPage
from fastapi import APIRouter, Query, HTTPException, Depends

from django_app.core.models import Block
from django_app.core.serializers import BlockSerializer
from fastapi_app.dependencies import get_current_user
from fastapi_app.schemas import BlockSchema

blocks_router = APIRouter()


@blocks_router.get("/", response_model=list[BlockSchema], dependencies=[Depends(get_current_user)])
def get_blocks(currency: str | None = Query(None), page: int = 1, page_size: int = 10):
    """
    Get a paginated list of blocks, optionally filtered by currency name.
    """
    queryset = Block.objects.all()

    if currency:
        queryset = queryset.filter(currency__name=currency)

    paginator = Paginator(queryset, page_size)
    try:
        paginated_blocks = paginator.page(page)
    except EmptyPage:
        return []

    serializer = BlockSerializer(paginated_blocks, many=True)

    return serializer.data


@blocks_router.get("/{block_id}", response_model=BlockSchema, dependencies=[Depends(get_current_user)])
def get_block_by_id(block_id: int):
    """
    Get block details by block ID.
    """
    try:
        block = Block.objects.get(id=block_id)
        serializer = BlockSerializer(block)
        return serializer.data
    except Block.DoesNotExist:
        raise HTTPException(status_code=404, detail="Block not found")


@blocks_router.get("/{currency}/{block_number}", response_model=BlockSchema, dependencies=[Depends(get_current_user)])
def get_block_by_currency_and_number(currency: str, block_number: int, ):
    """
    Get block details by currency and block number.
    """
    try:
        block = Block.objects.get(currency__name=currency, block_number=block_number)
        serializer = BlockSerializer(block)
        return serializer.data
    except Block.DoesNotExist:
        raise HTTPException(status_code=404, detail="Block not found")
