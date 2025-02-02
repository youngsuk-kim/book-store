from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Factory, Singleton

from app.auth.application.service.jwt import JwtService
from app.book.adapter.output.notification.book import CreateBookNotification
from app.book.adapter.output.persistence.repository_adapter import BookRepositoryAdapter
from app.book.adapter.output.persistence.sqlalchemy.book import BookSQLAlchemyRepo
from app.book.application.service.book import BookService
from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.adapter.output.persistence.sqlalchemy.user import UserSQLAlchemyRepo
from app.user.application.service.user import UserService
from celery_task.broker import CreateNotification


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(packages=["app"])

    user_repo = Singleton(UserSQLAlchemyRepo)
    user_repo_adapter = Factory(UserRepositoryAdapter, user_repo=user_repo)
    user_service = Factory(UserService, repository=user_repo_adapter)

    book_repo = Singleton(BookSQLAlchemyRepo)
    book_repo_adapter = Factory(BookRepositoryAdapter, book_repo=book_repo)
    book_service = Factory(BookService, repository=book_repo_adapter, user_repository=user_repo_adapter)
    book_notification = Singleton(CreateNotification)

    jwt_service = Factory(JwtService)
