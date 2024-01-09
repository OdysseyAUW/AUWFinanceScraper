from pydantic import BaseModel
import pandas as pd

class Stock(BaseModel):
    data: pd.DataFrame
    last: str
    first: str

    class Config: 
        arbitrary_types_allowed = True