from enum import Enum


class CriteriaFilters(Enum):
    AND = "and"
    OR = "or"
    LIMIT = "limit"
    PAGINATION = "pagination"


class Criteria:
    def __init__(self, fields):
        self.fields = fields
        self.clauses = []

    def add(self, clause):
        if clause[0] not in self.fields:
            raise ValueError(f"Invalid field: {clause[0]}")
        self.clauses.append(clause)
        return self

    def _and(self):
        self.clauses.append(CriteriaFilters.AND)
        return self

    def _or(self):
        self.clauses.append(CriteriaFilters.OR)
        return self

    def _limit(self, value: int):
        if value > 0:
            self.clauses.append(CriteriaFilters.LIMIT, "=", value)
        return self

    def _pagination(self, page: int, size: int):
        if page > 0 and size > 0:
            self.clauses.append(CriteriaFilters.PAGINATION, page, size)
        return self

    def __str__(self):
        return " ".join(str(clause) for clause in self.clauses)
