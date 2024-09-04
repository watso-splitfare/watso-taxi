from domain.database import MySqlDatabase
from exceptions import query


class MySQLOwnerDao(MySqlDatabase):
    def find_owner_id_by_group_id(self, group_id) -> int:
        cursor = self.mysql_connection.cursor()
        sql = f'''
        SELECT owner_id
        FROM group_table
        WHERE id = {group_id}'''

        cursor.execute(sql)
        data = cursor.fetchone()

        if data is None:
            raise query.ResourceNotFound(
                msg=f'그룹 정보를 찾을 수 없습니다. id={group_id}'
            )

        cursor.close()
        owner_id = data[0]
        return owner_id
