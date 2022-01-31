import pandas as pd
import table
import os
pd.options.plotting.backend = "plotly"


def main(df: pd.DataFrame) -> None:
    fig = df.plot.line()
    i = 0
    while True:
        file_cand = f'out{i}.html'
        if not os.path.isfile(file_cand):
            fig.write_html(file_cand)
            exit()
        else:
            i += 1


if __name__ == '__main__':
    df = table.main()
    main(df)
