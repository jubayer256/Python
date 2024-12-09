import sqlite3
from scripts.fileinfo import get_file_name


class DatabaseManagement:
    def __init__(self):
        self.db = sqlite3.connect("sdm.db", check_same_thread=False)
        self.cur = self.db.cursor()
        self._create_table()

    def _create_table(self):
        query = """
            create table download_record(
                id integer primary key,
                name varchar(100),
                url varchar(500),
                dir varchar(500),
                size int,
                downloaded int,
                status varchar(20),
                download_url varchar(200)
            );
        """
        check_query = "SELECT name FROM sqlite_master WHERE type='table' AND name='download_record';"
        if self.cur.execute(check_query).fetchone():
            return
        self.cur.execute(query)
        self.db.commit()

    def insert_record(self, name, u, d, s, download_url):
        query = """
            insert into download_record(name, url, dir, size, downloaded, status, download_url)
            values('{}', '{}', '{}', {}, {}, 'pending', '{}');
        """.format(name, u, d, s, 0, download_url)
        self.cur.execute(query)
        self.db.commit()

    def is_exists(self, url):
        if self.cur.execute("select 1 from download_record where url='{}'".format(url)).fetchone():
            return True
        else:
            return False

    def get_records(self, url):
        return self.cur.execute("select * from download_record where download_url='{}'".format(url)).fetchall()[0]

    def update_record(self, d, p, u):
        query = """
            update download_record
            set
            downloaded = {},
            status = '{}'
            where url = '{}';
        """.format(d, p, u)
        self.cur.execute(query)
        self.db.commit()

    def update_status(self, u, p):
        query = """
            update download_record
            set
            status = '{}'
            where url = '{}'; 
        """.format(p, u)
        self.cur.execute(query)
        self.db.commit()

    def delete_record(self, u):
        self.cur.execute("delete from download_record where url='{}'".format(u))
        self.db.commit()

    def all_records(self):
        return self.cur.execute("select * from download_record").fetchall()

    def repair_download(self):
        self.cur.execute("update download_record set status='pending' where status='downloading'")
        self.db.commit()

    def update_to_pending(self):
        self.cur.execute("update download_record set status='pending' where status='downloading'")
        self.db.commit()

    def remove_record(self, u):
        self.cur.execute("delete from download_record where url='{}'".format(u))
        self.db.commit()

    def get_the_url(self, u):
        data= self.cur.execute("select * from download_record where download_url='{}'".format(u)).fetchone()[2]
        return data
