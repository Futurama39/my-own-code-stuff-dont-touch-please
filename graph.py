import pandas as pd
import table
import os

pd.options.plotting.backend = "plotly"


def search_int(ext: str) -> int:
    i = 0
    while True:
        file_cand = f"out{i}.{ext}"
        if not os.path.isfile(file_cand):
            return i
        else:
            i += 1


def main(df: pd.DataFrame) -> None:
    fig = df.plot.line()
    match table.CONF.export:
        case 0:  # html_page
            name = f'out{search_int("html")}.html'
            fig.write_html(name)
        case 1:  # direct plotly window
            fig.show()
        case 2:  # csv export
            fig.to_csv(f'out{search_int("csv")}.csv')


if __name__ == "__main__":
    df = table.main()
    main(df)
