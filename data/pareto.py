import pandas as pd

class ParetoAnalysis:
    def __init__(self, data):
        self.data = pd.DataFrame(data)
        self._remove_duplicates()

    def _remove_duplicates(self):
        if len(self.data.columns) > 1:
            self.data.drop_duplicates(inplace=True, subset=self.data.columns[0], keep='first')

    def pareto_analysis(self):
        num_columns = len(self.data.columns)
        if num_columns == 1:
            return self._one_column_pareto()
        elif num_columns == 3 or num_columns == 6:
            return self._pareto_with_costs()
        else:
            return self._pareto_from_dataframe()

    def _pareto_from_dataframe(self, column=None):
        df = self._select_columns()
        column = self._get_column(df, column)
        df = self._calculate_percentages(df, column)
        df = self._add_totals_line(df)
        return df

    def _select_columns(self):
        return self.data.iloc[:, :4] if len(self.data.columns) > 4 else self.data.iloc[:, :2]

    def _get_column(self, df, column):
        if isinstance(column, str):
            return df[column]
        elif isinstance(column, int):
            return df.columns[column]
        else:
            return df.columns[1]

    def _calculate_percentages(self, df, column):
        df['Relative Percentage'] = df[column] / df[column].sum() * 100
        df = df.sort_values(by=column, ascending=False)
        df['Cumulative Percentage'] = df['Relative Percentage'].cumsum()
        return df

    def _add_totals_line(self, df):
        totals_line = [df[x].sum() if (df[x].dtype in ['int64', 'float64']) and x != df.columns[-1] else "TOTAL" for x in df.columns]
        df.loc[-1] = totals_line
        return df

    def _one_column_pareto(self):
        df = pd.DataFrame(self.data)
        df['Values'] = df.groupby(df.columns[0])[df.columns[0]].transform('count')
        df.drop_duplicates(subset=df.columns[0], keep='first', inplace=True)
        self.data = df
        return self._pareto_from_dataframe()

    def _pareto_with_costs(self):
        df = pd.DataFrame(self.data)
        df['Total Cost'] = df[df.columns[1]] * df[df.columns[2]]
        df[df.columns[3]] = df['Total Cost']
        self.data = df
        return self._pareto_from_dataframe(3)

if __name__ == "__main__":
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    data = {"category": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
            "values": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            "costs": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "total cost": [10, 40, 90, 160, 250, 360, 490, 640, 810, 1000],
            "relative percentage": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "cumulative percentage": [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]}

    pareto = ParetoAnalysis(data)

    print(pareto.pareto_analysis())

    data = {"category": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
            "values": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            "relative percentage": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "cumulative percentage": [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]}

    pareto = ParetoAnalysis(data)

    print(pareto.pareto_analysis())