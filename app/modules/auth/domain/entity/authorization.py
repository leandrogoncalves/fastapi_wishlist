from pydantic import BaseModel


class Authorization(BaseModel):
    access_token: str
    token_type: str

    def to_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "token_type": self.token_type
        }