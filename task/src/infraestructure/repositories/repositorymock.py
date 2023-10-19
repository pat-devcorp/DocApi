class RepositoryMock:
    def get(self, tablename: str, attrs: List[str]):
        return [{"ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c"}]

    def getByID(self, tablename: str, pk: str, id_val: str, attrs: List[str]):
        return {"ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c"}

    def update(self, tablename: str, pk: str, id_val: str, kwargs: dict):
        return {
            "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
            "description": "This is a ticket modified",
            "category": 1,
            "state": 1,
            "write_uid": "8888",
            "write_at": "2023-10-10 16:41:53",
            "create_uid": "9999",
            "create_at": "2023-10-10 16:41:53",
        }

    def create(self, tablename: str, kwargs: dict):
        return {
            "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
            "description": "This is a ticket modified",
            "category": 0,
            "state": 0,
            "write_uid": "7777",
            "write_at": "2023-10-10 16:41:53",
            "create_uid": "9999",
            "create_at": "2023-10-10 16:41:53",
        }