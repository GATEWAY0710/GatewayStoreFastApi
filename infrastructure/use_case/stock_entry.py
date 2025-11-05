from logging import Logger
from uuid import UUID
from application.persistence.stock_entry import StockEntryRepository
from application.use_case.models.base_response import BaseResponse
from application.use_case.models.stock_entry import CreateStock, CreateStockResponse, ListStocks, UpdateStockResponse, \
    GetStockResponse, UpdateStock
from application.use_case.stock_entry import StockEntryService as DefaultStockEntryService
from domain.models import StockEntry
from infrastructure.persistence.product_repo import ProductRepository


class StockEntryService(DefaultStockEntryService):
    _logger: Logger
    _stock_entry_repository: StockEntryRepository
    _product_repository: ProductRepository

    def __init__(self, logger: Logger, stock_entry_repository: StockEntryRepository, product_repository: ProductRepository):
        self._logger = logger
        self._stock_entry_repository = stock_entry_repository
        self._product_repository = product_repository

    def create(self, product_name: str, stock_entry: CreateStock) -> BaseResponse:
        product_exist = self._product_repository.get_by_name(product_name)
        if product_exist is None:
            self._logger.warning(f"{product_name} does not exist in database")
            response = BaseResponse(status=False, message=f"{product_name} does not exist in database")
            response._status_code = 400
            return response
        stock_entry = StockEntry(product_id=product_exist.id, cost_price=stock_entry.cost_price, selling_price=stock_entry.selling_price, quantity=stock_entry.quantity, remaining_quantity=stock_entry.quantity)
        stock_entry = self._stock_entry_repository.create(stock_entry=stock_entry, product_name=product_name)
        if not stock_entry:
            self._logger.error(f"error adding {product_name} to database")
            response = BaseResponse(status=False, message=f"error adding {product_name} to database")
            response._status_code = 500
            return response
        self._logger.info(f"{product_name} added to database succesfully")
        response = CreateStockResponse(status=True, quantity=stock_entry.quantity, cost_price=stock_entry.cost_price, selling_price=stock_entry.selling_price)
        response._status_code = 200
        return response

    def update(self, id: UUID, stock_entry: UpdateStock) -> BaseResponse:
        stock_exist = self._stock_entry_repository.get(id=id)
        if not stock_exist:
            self._logger.warning(f"stock not in database")
            response = BaseResponse(status=False, message=f"stock not in database")
            response._status_code = 400
            return response

        stock_exist.cost_price = stock_entry.cost_price
        stock_exist.selling_price = stock_entry.selling_price

        stock_update = self._stock_entry_repository.update(id=stock_exist.id, stock_entry=stock_exist)
        if not stock_update:
            self._logger.error(f"error updating {stock_exist.id} in database")
            response = BaseResponse(status=False, message=f"error updating {stock_exist.id} in database")
            response._status_code = 500
            return response
        self._logger.info(f"{stock_exist.id} updated succesfully")
        response = UpdateStockResponse(status=True, cost_price=stock_exist.cost_price, selling_price=stock_exist.selling_price)
        response._status_code = 200
        return response

    def get(self, id: UUID) -> BaseResponse:
        stock_exist = self._stock_entry_repository.get(id=id)
        if not stock_exist:
            self._logger.warning(f"stock not in database")
            response = BaseResponse(status=False, message=f"stock not in database")
            response._status_code = 400
            return response

        self._logger.info(f"{stock_exist.id} retrieved succesfully")
        response = GetStockResponse(status=True, quantity=stock_exist.quantity, remaining_quantity=stock_exist.remaining_quantity, cost_price=stock_exist.cost_price, selling_price=stock_exist.selling_price, added_date=str(stock_exist.added_date))
        response._status_code = 200
        return response


    def list(self) -> BaseResponse:
        stock_entries = self._stock_entry_repository.list()
        entries = []
        for entry in stock_entries:
            stocks = GetStockResponse(status=True, quantity=entry.quantity, remaining_quantity=entry.remaining_quantity, cost_price=entry.cost_price, added_date=str(entry.added_date), selling_price=entry.selling_price)
            entries.append(stocks)
        self._logger.info(f"{len(entries)} stock entries retrieved succesfully")
        response = ListStocks(status=True, stocks=entries)
        response._status_code = 200
        return response
