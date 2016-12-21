if __name__ == '__main__':
    from automated_sla_tool.bin.mars_report2 import main
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    main()
