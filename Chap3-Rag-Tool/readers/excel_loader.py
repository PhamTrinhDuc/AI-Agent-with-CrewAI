import pandas  as pd
import itertools
from pathlib import Path
from typing import Any, List, Optional, Union
from llama_index.core.readers.base import BaseReader
from llama_index.core import Document



class PandasExcelReader(BaseReader):
    r"""Pandas-based CSV parser.

    Parses CSVs using the separator detection from Pandas `read_csv` function.
    If special parameters are required, use the `pandas_config` dict.

    Args:

        pandas_config (dict): Options for the `pandas.read_excel` function call.
            Refer to https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html
            for more information. Set to empty dict by default,
            this means defaults will be used.

    """

    def __init__(self,
                 pandas_config: Optional[dict] = {}, 
                 row_joiner: str = "\n", 
                 col_joiner: str = " ",
                 *args: Any,
                 **kwargs: Any,) -> None:
        super().__init__(*args, **kwargs)
        self._pandas_config = pandas_config 
        self._row_joiner = row_joiner if row_joiner else "\n"
        self._col_joiner = col_joiner if col_joiner else " "

    def load_data(
            self, 
            file_path: Path,
            include_sheet_name: bool = False,
            sheet_name: Optional[Union[str, list]] = None,
            extra_info: Optional[dict] = None,
            **kwargs,
    ) -> List[Document]:
        """Parse file and extract values from a specific column.

        Args:
            file (Path): The path to the Excel file to read.
            include_sheetname (bool): Whether to include the sheet name in the output.
            sheet_name (Union[str, int, None]): The specific sheet to read from,
                default is None which reads all sheets.

        Returns:
            List[Document]: A list of`Document objects containing the
                values from the specified column in the Excel file.
        """

        try: 
            import pandas as pd
        except: 
            raise ImportError(
                    "install pandas using `pip3 install pandas` to use this loader"
                )
        if sheet_name is not None:
            sheet_name = (
                [sheet_name] if not isinstance(sheet_name, list) else sheet_name
            )

        dfs = pd.read_excel(file_path, sheet_name=sheet_name, **self._pandas_config)
        sheet_names = dfs.keys()
        df_sheets = []
        
        for sheet_name in sheet_names:
            sheet = []
            if include_sheet_name:
                sheet.append([sheet_name])
            dfs[sheet_name] = dfs[sheet_name].dropna(axis = 0, how = 'all')
            dfs[sheet_name].fillna("", inplace=True)
            sheet.extend(dfs[sheet_name].values.astype(str).tolist())
            df_sheets.append(sheet)
        
        # print(df_sheets)
        
        text_list = (
            itertools.chain.from_iterable(df_sheets)
        )

        # print(list(text_list))
        output = [
            Document(
                text=self._row_joiner.join(
                    self._col_joiner.join(sublist) for sublist in text_list
                ),
                metadata = extra_info or {}
            )
        ]
        return output
        
    
    def testing(self):
        path = "Chap3-Rag-Tool/data/demo/Financial_Sample.xlsx"
        output = self.load_data(file_path=path, include_sheet_name=True,
                                sheet_name=["Sheet2"])
        # print(output[:1])
