=============
Block Storage
=============

.. todo:: (For nick: Restructure the introduction to this chapter to
          provide context of what we're actually going to do.)

By default, data in OpenStack instances is stored on 'ephemeral'
disks. These stay with the instance throughout its lifetime, but when
the instance is terminated, that storage disappears -- along with all
the data stored on it. Ephemeral storage is allocated to a single
instance and cannot be moved to another instance.

In this section, we will introduce block storage. Block storage
(sometimes referred to as volume storage) provides you with access to
persistent storage devices. You interact with block storage by
attaching volumes to running instances, just as you might attach a USB
drive to a physical server. Volumes can be detached from one instance
and re-attached to another, and the data remains intact. Block
storage is implemented in OpenStack by the OpenStack Block Storage
(cinder) project.

One component of the Fractal app that cannot be allowed to fail is the
database server, which is used to keep track of all of the data about
fractals that have been created, including their storage location. So
while you may have configured the images to be stored in Object
Storage in the previous section, without the database we lose track of
where in Object Storage they are, and the parameters that were used to
create them.

Advanced users should consider how to remove the database from the
architecture altogether and replace it with metadata in the Object
Storage (then contribute these steps to :doc:`craziness`). Others
should read on to learn about how to work with block storage and move
the Fractal app database server to use it.

Basics
~~~~~~

Later on, we'll use a volume from the block storage service to provide
persistent storage for the Fractal app's database server, but first -
let's cover the basics, such as creating and attaching a block storage
device.

.. only:: dotnet

    .. warning:: This section has not yet been completed for the .NET SDK.

.. only:: fog

    .. warning:: This section has not yet been completed for the fog SDK.

.. only:: jclouds

    .. warning:: This section has not yet been completed for the jclouds SDK.

.. only:: pkgcloud

    .. warning:: This section has not yet been completed for the pkgcloud SDK.

.. only:: openstacksdk

    .. warning:: This section has not yet been completed for the OpenStack SDK.

.. only:: phpopencloud

    .. warning:: This section has not yet been completed for the
                 PHP-OpenCloud SDK.


As always, connect to the API endpoint:

.. only:: libcloud

    .. code-block:: python

      from libcloud.compute.types import Provider
      from libcloud.compute.providers import get_driver

        auth_username = 'your_auth_username'
        auth_password = 'your_auth_password'
        auth_url = 'http://controller:5000'
        project_name = 'your_project_name_or_id'
        region_name = 'your_region_name'

        provider = get_driver(Provider.OPENSTACK)
        connection = provider(auth_username,
                              auth_password,
                              ex_force_auth_url=auth_url,
                              ex_force_auth_version='2.0_password',
                              ex_tenant_name=project_name,
                              ex_force_service_region=region_name)

.. only:: shade

    .. literalinclude:: ../samples/shade/block_storage.py
        :language: python
        :start-after: step-1
        :end-before: step-2

To try it out, make a 1GB volume called :test'.

.. only:: libcloud

    .. code-block:: python

        volume = connection.create_volume(1, 'test')
        print(volume)

    ::

        <StorageVolume id=755ab026-b5f2-4f53-b34a-6d082fb36689 size=1 driver=OpenStack>

.. only:: shade

    .. literalinclude:: ../samples/shade/block_storage.py
        :language: python
        :start-after: step-2
        :end-before: step-3

.. note:: The parameter :code:`size` is in GigaBytes.

List all volumes to see if it was successful:

.. only:: libcloud

    .. code-block:: python

        volumes = connection.list_volumes()
        print(volumes)

    ::

        [<StorageVolume id=755ab026-b5f2-4f53-b34a-6d082fb36689 size=1 driver=OpenStack>]

.. only:: shade

    .. literalinclude:: ../samples/shade/block_storage.py
        :language: python
        :start-after: step-3
        :end-before: step-4

Now that you have created a storage volume, let's attach it to an
already running instance.


Using Block Storage for the Fractal database server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Firstly, we're going to need a new server for our dedicated database.
Start a new instance called :code:`app-database` using the image, flavor
and keypair you have been using since :doc:`/getting_started`.
We will also need a new security group to allow access to the database server
(for mysql, port 3306) from the network:

.. only:: libcloud

    .. code-block:: python

       db_group = connection.ex_create_security_group('database', 'for database service')
       connection.ex_create_security_group_rule(db_group, 'TCP', 3306, 3306)
       instance = connection.create_node(name='app-database',
                                         image=image,
                                         size=flavor,
                                         ex_keyname=keypair_name,
                                         ex_security_groups=[db_group])

.. only:: shade

    .. literalinclude:: ../samples/shade/block_storage.py
        :language: python
        :start-after: step-4
        :end-before: step-5

Using the unique identifier (UUID) for the volume, make a new volume
object, then use the server object from the previous snippet and
attach the volume to it at :code:`/dev/vdb`:

.. only:: libcloud

    .. code-block:: python

        volume = connection.ex_get_volume('755ab026-b5f2-4f53-b34a-6d082fb36689')
        connection.attach_volume(instance, volume, '/dev/vdb')

.. only:: shade

    .. literalinclude:: ../samples/shade/block_storage.py
        :language: python
        :start-after: step-5
        :end-before: step-6

Log in to the server to be able to run the following steps.

.. note:: Replace :code:`IP_SERVICES` with the IP address of the
          services instance and USERNAME to the appropriate username.

Now prepare the empty block device.

::

    $ ssh -i ~/.ssh/id_rsa USERNAME@IP_SERVICES
    # fdisk -l
    # mke2fs /dev/vdb
    # mkdir /mnt/database
    # mount /dev/vdb /mnt/database

.. todo:: Outputs missing, add attaching log from dmesg.

Stop the running MySQL database service and move the database files
from :file:`/var/lib/mysql` onto the new volume (temporary mounted at
:file:`/mnt/database`).

::

    # systemctl stop mariadb
    # mv /var/lib/mysql/* /mnt/database

Sync the filesystems and mount the new blockdevice now containing the
database files to :file:`/var/lib/mysql`.

::

    # sync
    # umount /mnt/database
    # rm -rf /mnt/database
    # echo "/dev/vdb /var/lib/mysql ext4 defaults  1 2" >> /etc/fstab
    # mount /var/lib/mysql

Finally start the previously stopped MySQL database service and check
if everything is working like expected.

::

    # systemctl start mariadb
    # mysql -ufaafo -ppassword -h localhost faafo -e 'show tables;'

Extras
~~~~~~

You can detach the volume and re-attach it elsewhere, or destroy the
volume with the below steps.

.. warning::
    The following operations are destructive and will result in data loss.

To detach and destroy a volume:

.. only:: libcloud

    .. code-block:: python

        connection.detach_volume(volume)

    ::

        True

    .. code-block:: python

        connection.destroy_volume(volume)

    .. note:: :code:`detach_volume` and :code:`destroy_volume` take a
              volume object, not a name.

.. only:: shade

    .. literalinclude:: ../samples/shade/block_storage.py
        :language: python
        :start-after: step-6
        :end-before: step-7

.. only:: libcloud

    There are also many other useful features, such as the ability to
    create snapshots of volumes (handy for backups):

    .. code-block:: python

        snapshot_name = 'test_backup_1'
        connection.create_volume_snapshot('test', name='test backup 1')

    .. todo:: Do we need a note here to mention that 'test' is the
              volume name and not the volume object?

    You can find information about these calls and more in the
    `libcloud documentation
    <http://ci.apache.org/projects/libcloud/docs/compute/drivers/openstack.html>`_.
