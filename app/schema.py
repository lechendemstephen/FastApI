from pydantic import BaseModel # type: ignore
from pydantic.networks import EmailStr # type: ignore
# pydantic models 
class Post(BaseModel): 
    title: str
    content: str
    published: bool = True

class User(BaseModel): 
    email: EmailStr 
    password: str

class UserOut(User): 
    id: int
    email: EmailStr
    
