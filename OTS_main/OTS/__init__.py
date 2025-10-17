import sys

if sys.version_info.major == 3:
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except ImportError:
        # Only warn if you're actually using MySQL
        import warnings
        warnings.warn("PyMySQL not installed — MySQL connections may not work.")
