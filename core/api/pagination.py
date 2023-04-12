from rest_framework.pagination import LimitOffsetPagination

class StandartMoviePagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


class StandartDirectorPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100