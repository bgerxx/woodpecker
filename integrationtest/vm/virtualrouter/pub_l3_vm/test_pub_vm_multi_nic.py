'''

@author: FangSun
'''


import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.test_util as test_util
from zstackwoodpecker.operations import net_operations as net_ops


test_stub = test_lib.lib_get_test_stub()
test_obj_dict = test_state.TestStateDict()


def test():

    pub_l3_vm, flat_l3_vm, vr_l3_vm = test_stub.generate_pub_test_vm(tbj=test_obj_dict)

    net_ops.attach_l3(flat_l3_vm.get_vm().vmNics[0].l3NetworkUuid, pub_l3_vm.get_vm().uuid)
    net_ops.attach_l3(vr_l3_vm.get_vm().vmNics[0].l3NetworkUuid, pub_l3_vm.get_vm().uuid)

    pub_l3_vm.check()
    pub_l3_vm.stop()
    pub_l3_vm.start()
    pub_l3_vm.check()

    pub_nic_l3uuid_list = (nic.l3NetworkUuid for nic in pub_l3_vm.get_vm().vmNics)
    assert flat_l3_vm.get_vm().vmNics[0].l3NetworkUuid in pub_nic_l3uuid_list
    assert vr_l3_vm.get_vm().vmNics[0].l3NetworkUuid in pub_nic_l3uuid_list

    pub_l3_vm.remove_nic([nic.uuid for nic in pub_l3_vm.get_vm().vmNics if nic.l3NetworkUuid == flat_l3_vm.get_vm().vmNics[0].l3NetworkUuid][0])
    pub_l3_vm.remove_nic([nic.uuid for nic in pub_l3_vm.get_vm().vmNics if nic.l3NetworkUuid == vr_l3_vm.get_vm().vmNics[0].l3NetworkUuid][0])
    assert len(pub_l3_vm.get_vm().vmNics) == 1



def env_recover():
    test_lib.lib_error_cleanup(test_obj_dict)
