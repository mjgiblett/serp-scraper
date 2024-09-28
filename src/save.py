from datetime import datetime

from pandas import DataFrame, ExcelWriter

from src.constants import DATA_PATH


def save(data) -> None:
    df = DataFrame(data)
    writer_path = f"{DATA_PATH}{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.xlsx"
    with ExcelWriter(writer_path) as writer:
        df.to_excel(writer)
