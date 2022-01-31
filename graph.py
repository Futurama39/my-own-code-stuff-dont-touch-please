import pandas as pd
import table
pd.options.plotting.backend = "plotly"


def main(df: pd.DataFrame) -> None:
    fig = df.plot.line()
    while True:
        i = 0
        try:
            file_cand = f'out{i}.html'
            fig.write_html(file_cand)
            exit()
        except FileExistsError:
            i += 1


if __name__ == '__main__':
    df = table.main()
    main(df)
