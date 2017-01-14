from os.path import join

from automated_sla_tool.src.Outlook import Outlook


def get_email(report, get='Voice Mail Data'):
    vm_data = report.settings(get)
    if not vm_data:
        print('No settings for {report}'.format(report=report.__class__.__name__))
    else:
        rtn_data = {}
        try:
            f_fmt_info = vm_data.get('File Fmt Info', None)
            f_path = join(
                report.src_doc_path,
                f_fmt_info['f_fmt'].format(file_fmt=report.dates.strftime(f_fmt_info['string_fmt']),
                                           f_ext=f_fmt_info['f_ext'])
            )
        except TypeError:
            print('Incorrect email settings for {report} {type} file path'.format(report=report.__class__.__name__,
                                                                                  type=get))
        else:
            try:
                rtn_data = _read_f_data(f_path)
            except FileNotFoundError:
                pass
                # rtn_data = _make_vm_data()  # this should probably get something from the parent
                _write_f_data(rtn_data, f_path)
        return rtn_data


def _read_f_data(f_path):
    rtn_stuff = {}
    with open(f_path) as f:
        for item in f.readlines():
            row_name, *args = item.strip().split(',')
            line = rtn_stuff.get(row_name, [])
            line.extend([item for item in args])
            rtn_stuff[row_name] = line
    return rtn_stuff


def _write_f_data(data, f_path):
    with open(f_path, 'w') as f:
        for row_name, row_data in data.items():
            f.write(
                '{row_name}, {row_data}'.format(row_name=row_name,
                                                row_data=','.join(row_data))
            )


class EmailHunter(Outlook):
    def __init__(self):
        super().__init__()
        pass
