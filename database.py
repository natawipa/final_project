import csv, os

class Database:
    def __init__(self):
        self.tables = []

    def import_csv(self, csv_file_name):
        table_name = csv_file_name.split('.')[0]
        with open(csv_file_name, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)
            self.upsert(Table(table_name, data))
            return self

    def write(self, table):
        self.upsert(table)
        with open(f'{table.table_name}.csv', 'w', newline='') as file:
            fieldnames = []
            if len(table.table_data) != 0:
                fieldnames = table.table_data[0].keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in table.table_data:
                writer.writerow(row)
        return self

    def table(self, table_name):
        for table in self.tables:
            if table.table_name == table_name:
                return table
        return None

    def remove_table(self, table_name):
        table = self.table(table_name)
        if table is not None:
            self.tables.remove(table)
        return self

    def upsert(self, table):
        if self.table(table.table_name) is not None:
            self.remove_table(table.table_name)
        self.tables.append(table)
        return self


class Table:
    def __init__(self, table_name, table_data):
        self.table_name = table_name
        self.table_data = table_data

    def __str__(self):
        return f"Table {self.table_name}:\n{str(self.table_data)}"

    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for row in self.table_data:
            if condition(row):
                filtered_table.table_data.append(row)
        if len(filtered_table.table_data) == 0:
            return None
        return filtered_table

    def update(self, data, filter=None):
        if filter is not None:
            for row in self.table_data:
                if all(row[key] == filter[key] for key in filter):
                    row.update(data)
        return self

    def insert(self, data):
        self.table_data.append(data)
        return self

    def delete(self, condition):
        self.table_data = [row for row in self.table_data if not condition(row)]
        return self

    def select(self, attributes_list):
        selected_table = Table(self.table_name + '_selected', [])
        for row in self.table_data:
            dict_temp = {}
            for key in row:
                if key in attributes_list:
                    dict_temp[key] = row[key]
            selected_table.table_data.append(dict_temp)
        return selected_table
