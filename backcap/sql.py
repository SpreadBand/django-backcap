from django.db.models import aggregates, Sum
from django.db.models.sql import aggregates as sql_aggregates

# hack to allow default value for Sum()
class SumWithDefault(aggregates.Aggregate):
    name = 'SumWithDefault'

class SQLSumWithDefault(sql_aggregates.Sum):
    sql_template = 'COALESCE(%(function)s(%(field)s), %(default)s)'

setattr(sql_aggregates, 'SumWithDefault', SQLSumWithDefault)






