

import pytest

from base.apiutil import Api
from common.readyaml import get_yaml


# class TestLogin:
#     @pytest.mark.run(order=1)
#     @pytest.mark.parametrize('baseInfo,testcase',get_yaml('./testcase/User/add_user.yaml'))
#     def test_add_user(self,baseInfo,testcase):
#         Api().specification_yaml(baseInfo,testcase)
#
#     @pytest.mark.run(order=2)
#     @pytest.mark.parametrize('baseInfo,testcase', get_yaml('./testcase/User/delete_user.yaml'))
#     def test_delete_user(self, baseInfo, testcase):
#         Api().specification_yaml(baseInfo, testcase)
#
#     @pytest.mark.run(order=3)
#     @pytest.mark.parametrize('baseInfo,testcase', get_yaml('./testcase/User/query_user.yaml'))
#     def test_query_user(self, baseInfo, testcase):
#         Api().specification_yaml(baseInfo, testcase)
#
#     @pytest.mark.run(order=4)
#     @pytest.mark.parametrize('baseInfo,testcase', get_yaml('./testcase/User/update_user.yaml'))
#     def test_update_user(self, baseInfo, testcase):
#         Api().specification_yaml(baseInfo, testcase)