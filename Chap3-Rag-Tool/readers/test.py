from docx_loader import DocxReader
from excel_loader import PandasExcelReader

def main():
    # reader = DocxReader()
    # reader.test()

    reader = PandasExcelReader()
    reader.testing()

if __name__ == "__main__":
    main()