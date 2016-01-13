# step-1
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

auth_username = 'your_auth_username'
auth_password = 'your_auth_password'
project_name = 'your_project_name_or_id'

auth_url = 'https://keystone.dream.io/'
region_name = 'RegionOne'

provider = get_driver(Provider.OPENSTACK)
conn = provider(auth_username,
                auth_password,
                ex_force_auth_url=auth_url,
                ex_force_auth_version='2.0_password',
                ex_tenant_name=project_name,
                ex_force_service_region=region_name)

# step-2
images = conn.list_images()
for image in images:
    print(image)

# step-3
flavors = conn.list_sizes()
for flavor in flavors:
    print(flavor)

# step-4
image_id = '90d5e049-aaed-4abc-aa75-60c2b1ed6516'
image = conn.get_image(image_id)
print(image)

# step-5
flavor_id = '100'
flavor = conn.ex_get_size(flavor_id)
print(flavor)

# step-6
instance_name = 'testing'
testing_instance = conn.create_node(name=instance_name, image=image, size=flavor)
print(testing_instance)

# step-7
instances = conn.list_nodes()
for instance in instances:
    print(instance)

# step-8
conn.destroy_node(testing_instance)

# step-9
print('Checking for existing SSH key pair...')
keypair_name = 'demokey'
pub_key_file = '~/.ssh/id_rsa.pub'
keypair_exists = False
for keypair in conn.list_key_pairs():
    if keypair.name == keypair_name:
        keypair_exists = True

if keypair_exists:
    print('Keypair ' + keypair_name + ' already exists. Skipping import.')
else:
    print('adding keypair...')
    conn.import_key_pair_from_file(keypair_name, pub_key_file)

for keypair in conn.list_key_pairs():
    print(keypair)

# step-10
print('Checking for existing security group...')
security_group_name = 'all-in-one'
security_group_exists = False
for security_group in conn.ex_list_security_groups():
    if security_group.name == security_group_name:
        all_in_one_security_group = security_group
        security_group_exists = True

if security_group_exists:
    print('Security Group ' + all_in_one_security_group.name + ' already exists. Skipping creation.')
else:
    all_in_one_security_group = conn.ex_create_security_group(security_group_name, 'network access for all-in-one application.')
    conn.ex_create_security_group_rule(all_in_one_security_group, 'TCP', 80, 80)
    conn.ex_create_security_group_rule(all_in_one_security_group, 'TCP', 22, 22)

for security_group in conn.ex_list_security_groups():
    print(security_group)

# step-11
userdata = '''#!/usr/bin/env bash
curl -L -s https://git.openstack.org/cgit/stackforge/faafo/plain/contrib/install.sh | bash -s -- \
    -i faafo -i messaging -r api -r worker -r demo
'''

# step-12
print('Checking for existing instance...')
instance_name = 'all-in-one'
instance_exists = False
for instance in conn.list_nodes():
    if instance.name == instance_name:
        testing_instance = instance
        instance_exists = True

if instance_exists:
    print('Instance ' + testing_instance.name + ' already exists. Skipping creation.')
else:
    testing_instance = conn.create_node(name=instance_name,
                                        image=image,
                                        size=flavor,
                                        ex_keyname=keypair_name,
                                        ex_userdata=userdata,
                                        ex_security_groups=[all_in_one_security_group])
    conn.wait_until_running([testing_instance])

for instance in conn.list_nodes():
    print(instance)

# step-13
print('Checking for unused Floating IP...')
unused_floating_ip = None
for floating_ip in conn.ex_list_floating_ips():
    if not floating_ip.node_id:
        unused_floating_ip = floating_ip
        break

if not unused_floating_ip:
    pool = conn.ex_list_floating_ip_pools()[0]
    print('Allocating new Floating IP from pool: {}'.format(pool))
    unused_floating_ip = pool.create_floating_ip()

# step-14
if len(testing_instance.public_ips) > 0:
    print('Instance ' + testing_instance.name + ' already has a public ip. Skipping attachment.')
else:
    conn.ex_attach_floating_ip_to_node(testing_instance, unused_floating_ip)

# step-15
print('The Fractals app will be deployed to http://%s' % unused_floating_ip.ip_address)
