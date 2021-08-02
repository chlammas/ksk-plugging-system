from openpyxl import load_workbook

def load_ksk(ksk_file_path: str, wirelist_file_path: str, ksk_col_number: int = 1) -> list:
    ksk_wb = load_workbook(ksk_file_path)
    ksk_sheet = ksk_wb.active
    derivatives = []
    data = []
    ksk_name = ksk_sheet[1][ksk_col_number].value
    for row in ksk_sheet:
        if (row[0].value):
            if row[ksk_col_number].value == 'X':
                # remove derivative version then add it to the list
                derivatives.append(row[0].value.split(' ')[0])

    wirelist_data = load_wire_list(wirelist_file_path)
    for derivative, connector, empty_cavity in wirelist_data:
        if derivative in derivatives:
            data.append((connector, empty_cavity))
    return ksk_name, data


def load_wire_list(file_path: str):
    wirelist_wb = load_workbook(file_path)
    wirelist_sheet = wirelist_wb.active
    data = []  # data = [(derivative, connector, cavity), ...]

    for row in list(wirelist_sheet)[1:]:  # row by row
        # row[0] : Derivative
        # row[1] : Wire
        # row[8] : Connector
        # row[9] : Cavity
        derivative = row[0].value.split(' ')[0]
        connector_id = row[8].value.strip()
        empty_cavity = row[9].value
        data.append((derivative, connector_id, empty_cavity))

    return data
