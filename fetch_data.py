import pandas as pd

URL = "https://raw.githubusercontent.com/stan-dev/example-models/master/knitr/pool-binary-trials/baseball-hits-2006.csv"
FILE_OUT = "baseball-hits-2006.csv"

if __name__ == "__main__":
    print(f"Fetching data from {URL}")
    data = pd.read_csv(URL, comment="#")
    print(f"Writing data to {FILE_OUT}")
    data.to_csv(FILE_OUT)
