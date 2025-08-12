import settings_helper as sh
import sql_helper as sqh


settings = sh.get_all_settings().get('default')
sqlite_client = sqh.SQL(settings['sqlite_url'])
postgres_client = sqh.SQL(settings['postgresql_url'])
mysql_client = sqh.SQL(settings['mysql_url'])
