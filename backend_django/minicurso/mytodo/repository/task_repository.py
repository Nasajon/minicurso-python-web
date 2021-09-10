import uuid

from nsj_gcf_utils.abstract_repository import AbstractRepository
from typing import Any, Dict


class TaskRepository(AbstractRepository):

    def find_by_id(self, id: str):
        sql = """
        select
            id,
            description,
            priority,
            complexity,
            created_at,
            finished_at,
            (extract(epoch from time)/3600)::int as time,
            status
        from
            task
        where
            id = :id
        """

        return self.fetchOne(sql, {'id': id})

    def list(self, status: bool = False):
        sql = """
        select
            id,
            description,
            priority,
            complexity,
            created_at,
            finished_at,
            (extract(epoch from time)/3600)::int as time,
            status
        from
            task
        where
            status = :status
        order by
            created_at desc
        """

        return self.fetchAll(sql, {'status': status})

    def insert_new(self, task: Dict[str, Any]):
        sql = """
        insert into task (
            id, description,
            priority, complexity )
        values (
            :id, :description,
            :priority, :complexity )
        """

        id = str(uuid.uuid4())

        count = self.execute(
            sql, {
                'id': id,
                'description': task['description'],
                'priority': task['priority'],
                'complexity': task['complexity']
            }
        )

        if count <= 0:
            raise Exception(f'Error inserting new task ({id}): {task}')

    def update(self, id: str, task: Dict[str, Any]):
        sql = """
        update task set
            description=:description, priority=:priority, complexity=:complexity, created_at=:created_at
        where
            id = :id
        """

        return self.execute(sql, {
            'id': id,
            'description': task['description'],
            'priority': task['priority'],
            'complexity': task['complexity'],
            'created_at': task['created_at']
        })

    def get_status(self, id: str):
        sql = """
        select
            status
        from
            task
        where
            id = :id
        """

        return self.fetchOne(sql, {'id': id})

    def update_status(self, id: str, status: bool):
        current_status = self.get_status(id)['status']

        if status == current_status:
            return 0
        elif status and not current_status:
            sql = """
            update task set
                status=true, finished_at=now(), time=now()-created_at
            where
                id = :id
                and not status
            """
        elif not status and current_status:
            sql = """
            update task set
                status=false, finished_at=null, time=null
            where
                id = :id
                and status
            """
        else:
            raise Exception(f'Inconsistent status {status} - {current_status}')

        self.execute(sql, {'id': id})

        return 0
