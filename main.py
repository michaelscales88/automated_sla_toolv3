from automated_sla_tool.bin import MistrP

if __name__ == '__main__':
    from os import sys, path
    print(sys.path)
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    MistrP.main()