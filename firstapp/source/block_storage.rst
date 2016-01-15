=============
Block Storage
=============

.. todo:: (For nick: Restructure the introduction to this chapter to
          provide context of what we're actually going to do.)

By default, data in OpenStack instances is stored on 'ephemeral'
disks. These disks remain with the instance throughout its lifetime.
When you terminate the instance, that storage and all the data stored
on it disappears. Ephemeral storage is allocated to a single instance
and cannot be moved to another instance.

This section introduces block storage, also known as volume storage,
which provides access to persistent storage devices. You interact with
block storage by attaching volumes to running instances just as you
might attach a USB drive to a physical server. You can detach volumes
from one instance and reattach them to another instance and the data
remains intact. The OpenStack Block Storage (cinder) project
implements block storage.

Though you might have configured Object Storage to store images, the
Fractal application needs a database to track the location of, and
parameters that were used to create, images in Object Storage. This
database server cannot fail.

If you are an advanced user, think about how you might remove the
database from the architecture and replace it with Object Storage
metadata, and then contribute these steps to :doc:`craziness`.

Otherwise, continue reading to learn how to work with, and move the
Fractal application database server to use, block storage.

Basics
~~~~~~

Later on, you will use a Block Storage volume to provide persistent
storage for the database server for the Fractal application. But
first, learn how to create and attach a Block Storage device.

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


Connect to the API endpoint:

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/block_storage.py
        :language: python
        :start-after: step-1
        :end-before: step-2

.. only:: shade

    .. literalinclude:: ../samples/shade/block_storage.py
        :language: python
        :start-after: step-1
        :end-before: step-2

To try it out, make a 1GB volume called :test'.

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/block_storage.py
        :language: python
        :start-after: step-2
        :end-before: step-3

    ::

        <StorageVolume id=755ab026-b5f2-4f53-b34a-6d082fb36689 size=1 driver=OpenStack>

.. only:: shade

    .. literalinclude:: ../samples/shade/block_storage.py
        :language: python
        :start-after: step-2
        :end-before: step-3

.. note:: The parameter :code:`size` is in gigabytes.

To see if the volume creation was successful, list all volumes:

.. only:: libcloud

     .. literalinclude:: ../samples/libcloud/block_storage.py
        :language: python
        :start-after: step-3
        :end-before: step-4

    ::

        [<StorageVolume id=755ab026-b5f2-4f53-b34a-6d082fb36689 size=1 driver=OpenStack>]

.. only:: shade

    .. literalinclude:: ../samples/shade/block_storage.py
        :language: python
        :start-after: step-3
        :end-before: step-4

Now that you have created a storage volume, let's attach it to an
already running instance.

Use Block Storage for the Fractal database server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You need a server for the dedicated database. Use the image, flavor, and
keypair that you used in :doc:`/getting_started` to launch an
:code:`app-database` instance.

You also need a security group to permit access to the database server (for
MySQL, port 3306) from the network:

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/block_storage.py
        :language: python
        :start-after: step-4
        :end-before: step-5

.. only:: shade

    .. literalinclude:: ../samples/shade/block_storage.py
        :language: python
        :start-after: step-4
        :end-before: step-5

Using the unique identifier (UUID) for the volume, make a new volume
object, then use the server object from the previous snippet and
attach the volume to it at :code:`/dev/vdb`:

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/block_storage.py
        :language: python
        :start-after: step-5
        :end-before: step-6

.. only:: shade

    .. literalinclude:: ../samples/shade/block_storage.py
        :language: python
        :start-after: step-5
        :end-before: step-6

Log in to the server to be able to run the following steps.

.. note:: Replace :code:`IP_SERVICES` with the IP address of the
          services instance and USERNAME to the appropriate user name.

Now prepare the empty block device.

::

    $ ssh -i ~/.ssh/id_rsa USERNAME@IP_SERVICES
    # fdisk -l
    # mke2fs /dev/vdb
    # mkdir /mnt/database
    # mount /dev/vdb /mnt/database

.. todo:: Outputs missing, add attaching log from dmesg.

Stop the running MySQL database service and move the database files from
:file:`/var/lib/mysql` to the new volume, which is temporarily mounted at
:file:`/mnt/database`.

::

    # systemctl stop mariadb
    # mv /var/lib/mysql/* /mnt/database

Sync the file systems and mount the block device that contains the database
files to :file:`/var/lib/mysql`.

::

    # sync
    # umount /mnt/database
    # rm -rf /mnt/database
    # echo "/dev/vdb /var/lib/mysql ext4 defaults  1 2" >> /etc/fstab
    # mount /var/lib/mysql

Finally, start the stopped MySQL database service and validate that everything
works as expected.

::

    # systemctl start mariadb
    # mysql -ufaafo -ppassword -h localhost faafo -e 'show tables;'

Extras
~~~~~~

You can detach the volume and reattach it elsewhere, or use the following
steps to delete the volume.

.. warning::
    The following operations are destructive and result in data loss.

To detach and delete a volume:

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/block_storage.py
        :start-after: step-6
        :end-before: step-7

    ::

        True

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

    .. literalinclude:: ../samples/libcloud/block_storage.py
        :language: python
        :start-after: step-7
        :end-before: step-8

    .. todo:: Do we need a note here to mention that 'test' is the
              volume name and not the volume object?

    You can find information about these calls and more in the
    `libcloud documentation
    <http://ci.apache.org/projects/libcloud/docs/compute/drivers/openstack.html>`_.
