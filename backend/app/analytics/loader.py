 # load data từ DB → pandas
import pandas as pd
from sqlalchemy.orm import Session
from app.database import engine
from app.models import Interaction

def load_interactions():
    session = Session(bind=engine)

    rows = session.query(
        Interaction.user_id,
        Interaction.product_id,
        Interaction.type
    ).all()

    session.close()

    return pd.DataFrame(
        rows,
        columns=["user_id", "product_id", "type"]
    )
