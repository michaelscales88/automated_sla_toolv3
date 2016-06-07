def valid_input(column_position, row, ws, input_type):
    # Utility function for validating cells from each ws
    if input_type == 'N':
        try:
            return_value = int(ws['%s%d' % (column_position, row)].value)
        except TypeError:
            return_value = 0
        except ValueError:
            try:
                return_value = ws['%s%d' % (column_position, row)].value
                h, m, s = [int(float(i)) for i in return_value.split(':')]
            except TypeError:
                return_value = 0
            except ValueError:
                return_value = 0
            else:
                return_value = (3600 * int(h)) + (60 * int(m)) + int(s)
    elif input_type == 'B':
        return_value = ws['%s%d' % (column_position, row)].value
    elif input_type == 'S':
        return_value = str(ws['%s%d' % (column_position, row)].value)
    else:
        raise ValueError("Invalid input type in valid_input")
    return return_value
