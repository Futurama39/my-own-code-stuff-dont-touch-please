import pandas as pd
import table
pd.options.plotting.backend = "plotly"


def main(df: pd.DataFrame) -> None:
    fig = df.plot.line()
    fig.show()


if __name__ == '__main__':
    df = table.main()
    main(df)
