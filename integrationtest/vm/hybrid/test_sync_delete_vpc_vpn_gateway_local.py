'''

New Integration Test for hybrid.

@author: Legion
'''

import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.test_state as test_state
import zstackwoodpecker.operations.hybrid_operations as hyb_ops
import zstackwoodpecker.operations.resource_operations as res_ops
import time
import os

date_s = time.strftime('%m%d%S', time.localtime())
test_obj_dict = test_state.TestStateDict()
ks_inv = None
datacenter_inv = None

def test():
    global ks_inv
    global datacenter_inv
    datacenter_type = os.getenv('datacenterType')
    try:
        ks_inv = hyb_ops.add_aliyun_key_secret('test_hybrid', 'test for hybrid', os.getenv('aliyunKey'), os.getenv('aliyunSecret'))
    except:
        pass
    datacenter_list = hyb_ops.get_datacenter_from_remote(datacenter_type)
    regions = [ i.regionId for i in datacenter_list]
    for r in regions:
        if 'shanghai' in r:
            region_id = r
    datacenter_inv = hyb_ops.add_datacenter_from_remote(datacenter_type, region_id, 'datacenter for test')
    iz_list = hyb_ops.get_identity_zone_from_remote(datacenter_type, region_id)
    zone_id = iz_list[-1].zoneId
    hyb_ops.add_identity_zone_from_remote(datacenter_type, datacenter_inv.uuid, zone_id)
    hyb_ops.sync_vpc_vpn_gateway_from_remote(datacenter_inv.uuid)
    vpc_vpn_gw_local = hyb_ops.query_vpc_vpn_gateway_local()
    assert len(vpc_vpn_gw_local) > 0
    for gw in vpc_vpn_gw_local:
        hyb_ops.del_vpc_vpn_gateway_local(gw.uuid)
    vpc_vpn_gw_local_after = hyb_ops.query_vpc_vpn_gateway_local()
    assert len(vpc_vpn_gw_local_after) == 0
    test_util.test_pass('Sync Delete Vpc Vpn Gateway Local Test Success')

def env_recover():
    global datacenter_inv
    if datacenter_inv:
        hyb_ops.del_datacenter_in_local(datacenter_inv.uuid)

    global ks_inv
    if ks_inv:
        hyb_ops.del_aliyun_key_secret(ks_inv.uuid)

#Will be called only if exception happens in test().
def error_cleanup():
    global test_obj_dict
    test_lib.lib_error_cleanup(test_obj_dict)