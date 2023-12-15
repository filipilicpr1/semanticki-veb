class Table:
    def __init__(self, *columns_in_table):
        if columns_in_table is None or len(columns_in_table) == 0:
            raise ValueError("Parameter cannot be null nor empty")

        self.columns = list(columns_in_table)
        self.rows = []

    def add_row(self, *values):
        if values is None:
            raise ValueError("Parameter cannot be null")

        if len(values) != len(self.columns):
            raise Exception("The number of values in a row does not match the number of columns.")

        self.rows.append(values)

    def __str__(self):
        table_string = []
        columns_length = self.get_columns_maximum_string_lengths()

        row_string_format = " | ".join(["{" + str(i) + ":<" + str(columns_length[i]) + "}" for i in range(len(self.columns))]) + " |"

        column_headers = row_string_format.format(*self.columns)
        results = [row_string_format.format(*row) for row in self.rows]

        maximum_row_length = max(0, max([len(row_string_format.format(*row)) for row in self.rows], default=0))
        maximum_line_length = max(maximum_row_length, len(column_headers))

        divider_line = "".join(["-" for _ in range(maximum_line_length)])
        divider = f" {divider_line} "

        table_string.append(divider)
        table_string.append('|'+column_headers)

        for row in results:
            table_string.append(divider)
            table_string.append('|'+row)

        table_string.append(divider)

        return "\n".join(table_string)

    def get_string(self):
        return str(self)

    def get_columns_maximum_string_lengths(self):
        columns_length = []

        for i in range(len(self.columns)):
            column_row = [self.columns[i]]
            max_length = 0

            for j in range(len(self.rows)):
                column_row.append(self.rows[j][i])

            for n in range(len(column_row)):
                length = len(str(column_row[n]))

                if length > max_length:
                    max_length = length

            columns_length.append(max_length)

        return columns_length
