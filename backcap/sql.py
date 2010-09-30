# -*- coding: utf-8 -*-

# Backcap, a support module for community-driven django websites
# Copyright (C) 2010, Guillaume Libersat <guillaume@spreadband.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.db.models import aggregates, Sum
from django.db.models.sql import aggregates as sql_aggregates

# hack to allow default value for Sum()
class SumWithDefault(aggregates.Aggregate):
    name = 'SumWithDefault'

class SQLSumWithDefault(sql_aggregates.Sum):
    sql_template = 'COALESCE(%(function)s(%(field)s), %(default)s)'

setattr(sql_aggregates, 'SumWithDefault', SQLSumWithDefault)






