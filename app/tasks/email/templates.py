from email.message import EmailMessage

from pydantic import EmailStr

from app.settings import settings


class UserEmailMessage(EmailMessage):
    def __init__(self, email_to: EmailStr):
        super().__init__()
        self['From'] = settings.SMTP_USER
        self['To'] = email_to


class RegConfirmEmailMessage(UserEmailMessage):
    def __init__(self, email_to: EmailStr, confirmation_link: str):
        super().__init__(email_to)
        self.confirmation_link = confirmation_link

        self['Subject'] = 'Подтверждение регистрации'
        self.set_content(
            f"""
            <h3>Чтобы подтвердить почту для регистрации на сайте {settings.DOMAIN_URL}, перейдите по ссылке: {self.confirmation_link}</h3>
            """,
            subtype='html'
        )


class RemindConfirmEmailMessage(RegConfirmEmailMessage):
    def __init__(self, email_to: EmailStr, confirmation_link: str):
        super().__init__(email_to, confirmation_link)
        self.set_content(
            f"""
            <h3>Вы так и не завершили регистрацию на сайте {settings.DOMAIN_URL}. Перейдите по ссылке, 
            чтобы подтвердить почту: {self.confirmation_link}</h3>
            """,
            subtype='html'
        )
