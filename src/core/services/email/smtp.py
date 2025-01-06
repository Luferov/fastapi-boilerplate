import smtplib
import ssl
from pathlib import Path
from typing import Self

from src.settings import Settings


class SMTPEmailService:
    """
    Сервис для оправки email с помощью протокола SMTP.
    """

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def send(self: Self, to_email: str, message: str) -> None:
        """
        Отправляем email.
        """
        context = ssl.create_default_context()
        local_smtp = Path(self.settings.base_dir) / 'users' / 'smtp' / 'certs' / 'cert.pem'
        if Path(local_smtp).is_file():
            context.load_verify_locations(cafile=local_smtp)
        with smtplib.SMTP(self.settings.smtp.host, self.settings.smtp.port) as server:
            server.starttls(context=context)
            server.login(self.settings.smtp.user, self.settings.smtp.password)
            server.sendmail(self.settings.smtp.user, to_email, message)
