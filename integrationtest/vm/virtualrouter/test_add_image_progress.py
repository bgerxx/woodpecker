'''

New Integration test for add image progress.

@author: quarkonics
'''

import zstackwoodpecker.test_util as test_util
import zstackwoodpecker.test_lib as test_lib
import zstackwoodpecker.operations.volume_operations as vol_ops
import zstackwoodpecker.operations.resource_operations as res_ops
import zstackwoodpecker.zstack_test.zstack_test_image as zstack_image_header
import apibinding.inventory as inventory
import threading
import os
import time
_config_ = {
        'timeout' : 1800,
        'noparallel' : True
        }

new_image = None

def add_image(bs_uuid):
    global new_image
    image_option = test_util.ImageOption()
    image_option.set_name('test_add_image_progress')
    image_option.set_format('qcow2')
    image_option.set_mediaType('RootVolumeTemplate')
    image_option.set_url(os.environ.get('imageUrl_net'))
    image_option.set_backup_storage_uuid_list([bs_uuid])

    new_image = zstack_image_header.ZstackTestImage()
    new_image.set_creation_option(image_option)

    new_image.add_root_volume_template()

def test():
    global new_image
    bs_cond = res_ops.gen_query_conditions("status", '=', "Connected")
    bss = res_ops.query_resource_fields(res_ops.BACKUP_STORAGE, bs_cond, \
            None, fields=['uuid'])
    if not bss:
        test_util.test_skip("not find available backup storage. Skip test")

    if bss[0].type != inventory.CEPH_BACKUP_STORAGE_TYPE:
        if hasattr(inventory, 'IMAGE_STORE_BACKUP_STORAGE_TYPE') and bss[0].type != inventory.IMAGE_STORE_BACKUP_STORAGE_TYPE:
            test_util.test_skip("not find available imagestore or ceph backup storage. Skip test")

    thread = threading.Thread(target=add_image, args=(bss[0].uuid, ))
    thread.start()
    time.sleep(5)
    image_cond = res_ops.gen_query_conditions("status", '=', "Downloading")
    image = res_ops.query_resource_fields(res_ops.IMAGE, image_cond, \
            None, fields=['uuid'])

    progress = res_ops.get_task_progress(image[0].uuid)

    if int(progress.progress) < 0 or int(progress.progress) > 100:
        test_util.test_fail("Progress of task should be between 0 and 100, while it actually is %s" % (progress.progress))
    thread.join()
    new_image.delete()
    if test_lib.lib_get_image_delete_policy() != 'Direct':
        new_image.expunge()

    test_util.test_pass('Add image Progress Test Success')

#Will be called only if exception happens in test().
def error_cleanup():
    global new_image
    if new_image:
        new_image.delete()
        if test_lib.lib_get_image_delete_policy() != 'Direct':
            new_image.expunge()
