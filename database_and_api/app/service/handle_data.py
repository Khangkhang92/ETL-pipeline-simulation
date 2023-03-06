from config.logger import logger
import pandas as pd
import os
from config.settings import settings
from .base_service import BaseService
from .benchmark import time_benchmark, memory_benchmark
from config.extensions.exception_handler import NotFound
from config.logger import logger


class Handle_Data(BaseService):
    def _pre_read_excel(self, path: str) -> None:
        expected_column_names = [
            "indexId",
            "chartOpen",
            "chartHigh",
            "chartLow",
            "chartClose",
            "totalQtty",
            "totalValue",
            "dateTime",
            "date",
            "time",
        ]
        if not os.path.exists(path):
            raise NotFound(404001)
        try:
            etf = pd.read_excel(
                path, sheet_name=0, nrows=1, usecols=expected_column_names
            )
            del etf
        except ValueError as e:
            raise NotFound(404002, params=[str(e)])

    @time_benchmark
    def _excel_to_df(self) -> pd.DataFrame:
        cwd = os.getcwd()
        path = os.path.join(cwd, settings.EXCEL_PATH)
        self._pre_read_excel(path)
        etf = pd.read_excel(path, sheet_name=0)
        logger.info("reading excel file is complete!")
        return etf

    @time_benchmark
    def _change_time_frame(self, frame: str, etf: pd.DataFrame) -> pd.DataFrame:

        ohlc = {
            "chartOpen": "first",
            "chartHigh": "max",
            "chartLow": "min",
            "chartClose": "last",
            "totalQtty": "sum",
            "totalValue": "sum",
        }
        df = (
            etf.set_index(pd.DatetimeIndex(etf["dateTime"]))
            .groupby("indexId")
            .resample(frame)
            .apply(ohlc)
        )
        df = df.drop(df[df.chartOpen.isnull()].index).reset_index()
        df["time"] = pd.to_datetime(df["dateTime"]).dt.time
        df["date"] = pd.to_datetime(df["dateTime"]).dt.date
        return df

    def _save_index_name(self, etf) -> list:
        list_index = etf["indexId"].unique().tolist()
        ds = pd.DataFrame({"index_id": list_index})
        self._save_todb("index_name", ds, upsert=True)

    @time_benchmark
    def _save_frame_m1(self, etf: pd.DataFrame) -> None:
        self._save_todb("index_frame_m1", etf, upsert=True)

    @time_benchmark
    def _save_frame_h1(self, frame: str, etf: pd.DataFrame) -> None:
        df = self._change_time_frame(frame, etf)
        del etf
        self._save_todb("index_frame_h1", df, upsert=True)

    def manual_etl_data(
        self,
    ) -> None:
        etf = self._excel_to_df()
        self._save_index_name(etf)
        self._save_frame_m1(etf)
        self._save_frame_h1(settings.TIMEFRAME, etf)


handle_data = Handle_Data()
