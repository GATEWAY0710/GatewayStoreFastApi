from dependency_injector import containers, providers
from application.persistence.report_repo import ReportRepository as DefaultReportRepository
from application.persistence.sales_repo import SalesRepository as DefaultSalesRepository
from application.persistence.user_repo import UserRepository as DefaultUserRepository
from application.persistence.profile_repo import ProfileRepository as DefaultProfileRepository
from application.persistence.product_repo import ProductRepository as DefaultProductRepository
from application.persistence.stock_entry import StockEntryRepository as DefaultStockEntryRepository
from application.use_case.report_service import ReportService as DefaultReportService
from application.use_case.sales_service import SalesService as DefaultSalesService
from application.use_case.product_service import ProductService as DefaultProductService
from application.use_case.user_service import UserService as DefaultUserService
from application.use_case.profile_service import ProfileService as DefaultProfileService
from application.use_case.stock_entry import StockEntryService as DefaultStockEntryService
from infrastructure.payment import PaystackService
from infrastructure.persistence.report_repo import ReportRepository as ReportRepository
from infrastructure.persistence.sales_repo import SalesRepository as SalesRepository
from infrastructure.persistence.user_repo import UserRepository as UserRepository
from infrastructure.persistence.profile_repo import ProfileRepository as ProfileRepository
from infrastructure.persistence.product_repo import ProductRepository as ProductRepository
from infrastructure.persistence.stock_entry import StockEntryRepository as StockEntryRepository
from infrastructure.use_case.report_service import ReportService as ReportService
from infrastructure.use_case.Sales_service import SaleService as SalesService
from infrastructure.use_case.product_service import ProductService as ProductService
from infrastructure.use_case.user_service import UserService as UserService
from infrastructure.use_case.profile_service import ProfileService as ProfileService
from infrastructure.use_case.stock_entry import StockEntryService as StockEntryService


from typing import Callable
import logging
logger = logging.getLogger(__name__)

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    user_repo: Callable[[], DefaultUserRepository] = providers.Factory(UserRepository, logger=logger)
    user_service: Callable[[], DefaultUserService ] = providers.Factory(UserService, logger=logger, user_repo=user_repo)

    profile_repository: Callable[[], DefaultProfileRepository] = providers.Factory(ProfileRepository, logger=logger)
    profile_service: Callable[[], DefaultProfileService] = providers.Factory(ProfileService, logger=logger, profile_repository=profile_repository)

    product_repository: Callable[[], DefaultProductRepository] = providers.Factory(ProductRepository, logger=logger)
    product_service: Callable[[], DefaultProductService] = providers.Factory(ProductService, logger=logger, product_repository=product_repository)

    stock_entry_repository: Callable[[], DefaultStockEntryRepository] = providers.Factory(StockEntryRepository, logger=logger)
    stock_entry_service: Callable[[], DefaultStockEntryService] = providers.Factory(StockEntryService, logger=logger, stock_entry_repository=stock_entry_repository, product_repository=product_repository)

    paystack_service: Callable[[], PaystackService] = providers.Factory(PaystackService, logger=logger)

    sales_repository: Callable[[], DefaultSalesRepository] = providers.Factory(SalesRepository, logger=logger)
    sales_service: Callable[[], DefaultSalesService] = providers.Factory(SalesService, logger=logger, sale_repository=sales_repository, stock_repository= stock_entry_repository, product_repository=product_repository, paystack_service=paystack_service)

    report_repository: Callable[[], DefaultReportRepository] = providers.Factory(ReportRepository, logger=logger)
    report_service: Callable[[], DefaultReportService] = providers.Factory(ReportService, logger=logger, report_repository=report_repository)