import time

import pytest

from base.apiutil import Api
from common.readyaml import get_yaml, ReadAndWriteYaml
from common.send_request import SendRequest
from conf.operateconf import OperateConf



class TestGoods:
    @pytest.mark.run(order=5)
    @pytest.mark.parametrize('baseInfo,testcase',get_yaml('./testcase/Goods/goods.yaml'))
    def test_goods1(self,baseInfo,testcase):
        Api().specification_yaml(baseInfo,testcase)

    @pytest.mark.run(order=6)
    @pytest.mark.parametrize('baseInfo,testcase', get_yaml('./testcase/Goods/getGoodsDetail.yaml'))
    def test_goods2(self, baseInfo,testcase):
        Api().specification_yaml(baseInfo,testcase)

    @pytest.mark.run(order=7)
    @pytest.mark.parametrize('baseInfo,testcase', get_yaml('./testcase/Goods/commit_order.yaml'))
    def test_goods3(self, baseInfo, testcase):
        Api().specification_yaml(baseInfo, testcase)


    @pytest.mark.run(order=8)
    @pytest.mark.parametrize('baseInfo,testcase', get_yaml('./testcase/Goods/order_pay.yaml'))
    def test_goods4(self, baseInfo, testcase):
        Api().specification_yaml(baseInfo, testcase)

    @pytest.mark.run(order=9)
    @pytest.mark.parametrize('baseInfo,testcase', get_yaml('./testcase/Goods/add_to_shopping_trolley.yaml'))
    def test_goods5(self, baseInfo, testcase):
        Api().specification_yaml(baseInfo, testcase)

    @pytest.mark.run(order=10)
    @pytest.mark.parametrize('baseInfo,testcase', get_yaml('./testcase/Goods/delete_shopping_trolley_goods.yaml'))
    def test_goods6(self, baseInfo, testcase):
        Api().specification_yaml(baseInfo, testcase)

    @pytest.mark.run(order=11)
    @pytest.mark.parametrize('baseInfo,testcase', get_yaml('./testcase/Goods/proofread_goods_order_status.yaml'))
    def test_goods7(self, baseInfo, testcase):
        Api().specification_yaml(baseInfo, testcase)

    @pytest.mark.run(order=12)
    @pytest.mark.parametrize('baseInfo,testcase', get_yaml('./testcase/Goods/proofread_logistics_status.yaml'))
    def test_goods8(self, baseInfo, testcase):
        Api().specification_yaml(baseInfo, testcase)

    @pytest.mark.run(order=13)
    @pytest.mark.parametrize('baseInfo,testcase', get_yaml('./testcase/Goods/proofread_goods_store.yaml'))
    def test_goods9(self, baseInfo, testcase):
        Api().specification_yaml(baseInfo, testcase)










