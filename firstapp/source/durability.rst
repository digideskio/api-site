===============
Make it durable
===============

.. todo:: https://github.com/apache/libcloud/pull/492

.. todo:: For later versions of the guide:  Extend the Fractals app to use Swift directly, and show the actual code from there.

.. todo:: Explain how to get objects back out again.

.. todo:: Large object support in Swift
          http://docs.openstack.org/developer/swift/overview_large_objects.html

This section introduces object storage.  DreamObjects uses softare
called Ceph. Ceph is open source software for creating redundant, scalable data
storage using clusters of standardized servers to store petabytes of
accessible data.  It is a long-term storage system for large amounts
of static data that can be retrieved, leveraged, and updated. Access
is via an API, not through a file-system like more traditional
storage.

There are a two key concepts to understand in the Object Storage
API. The Object Storage API is organized around two types of entities:

* Objects
* Containers

Similar to the Unix programming model, an object is a "bag of bytes"
that contains data, such as documents and images. Containers are used
to group objects.  You can make many objects inside a container, and
have many containers inside your account.

If you think about how you traditionally make what you store durable,
very quickly you should come to the conclusion that keeping multiple
copies of your objects on separate systems is a good way to do
that. However, keeping track of multiple copies of objects is a pain,
and building that into an app requires a lot of logic. Ceph
does this automatically for you behind-the-scenes. It will always work to ensure that there
are three copies of your objects (by default) at all times -
replicating them around the system in case of hardware failure,
maintenance, network outage or any other kind of breakage. This is
very convenient for app creation - you can just dump objects into
object storage and not have to care about any of this additional work
to keep them safe.


Using Object Storage to store fractals
--------------------------------------

The Fractals app currently uses the local filesystem on the instance
to store the images it generates. This is not scalable or durable, for
a number of reasons.

Because the local filesystem is ephemeral storage, if the instance is
terminated, the fractal images will be lost along with the
instance. Block based storage avoids that problem, but like local filesystems, it
requires administration to ensure that it does not fill up, and
immediate attention if disks fail.

The Object Storage service manages many of these tasks that normally
would require the application owner to manage them, and presents a
scalable and durable API that you can use for the fractals app,
without having to be concerned with the low level details of how the
objects are stored and replicated, and growing the storage pool. In
fact, Object Storage handles replication intrinsically, storing multiple
copies of each object and returning one of them on demand using the
API.

First, let's learn how to connect to the Object Storage endpoint:

.. only:: shade

    First you must install cloudfiles:

    .. code-block:: shell

        $ pip install python-cloudfiles

    Then you can authenticate to DreamObjects

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-1
        :end-before: step-2

.. only:: dotnet

    .. warning:: This section has not yet been completed for the .NET SDK.

.. only:: fog

    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-1
        :end-before: step-2

.. only:: jclouds

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-1
        :end-before: step-2

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-1
        :end-before: step-2


    .. warning::

        Libcloud 0.16 and 0.17 are afflicted with a bug that means
        authentication to a swift endpoint can fail with `a Python
        exception
        <https://issues.apache.org/jira/browse/LIBCLOUD-635>`_. If
        you encounter this, you can upgrade your libcloud version, or
        apply a simple `2-line patch
        <https://github.com/fifieldt/libcloud/commit/ec58868c3344a9bfe7a0166fc31c0548ed22ea87>`_.

    .. note:: Libcloud uses a different connector for Object Storage
              to all other OpenStack services, so a conn object from
              previous sections will not work here and we have to create
              a new one named :code:`swift`.

.. only:: pkgcloud

    .. warning:: This section has not yet been completed for the pkgcloud SDK.

.. only:: openstacksdk

    .. warning:: This section has not yet been completed for the OpenStack SDK.

.. only:: phpopencloud

    .. warning:: This section has not yet been completed for the
                 PHP-OpenCloud SDK.


To begin to store objects, we must first make a container.
We will generate a random name for it, because it must be unique:

.. only:: shade

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-2
        :end-before: step-3

.. only:: fog

    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-2
        :end-before: step-3

    You should see output such as:

    .. code-block:: ruby

        TBC

.. only:: jclouds

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-2
        :end-before: step-3

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-2
        :end-before: step-3

    You should see output such as:

    .. code-block:: python

        <Container: name=fractals, provider=OpenStack Swift>

You should now be able to see this container appear in a listing of
all containers in your account:

.. only:: fog

    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-3
        :end-before: step-4

    You should see output such as:

    .. code-block:: ruby

        TBC

.. only:: jclouds

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-3
        :end-before: step-4

.. only:: shade

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-3
        :end-before: step-4

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-3
        :end-before: step-4

    You should see output such as:

    .. code-block:: python

        [<Container: name=fractals, provider=OpenStack Swift>]

The next logical step is to upload an object. Find a photo of a goat
online, name it :code:`goat.jpg` and upload it to your container.
You can do that with the following code:

.. only:: fog

    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-4
        :end-before: step-5

.. only:: jclouds

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-4
        :end-before: step-5

.. code-block:: shell

    $ wget https://upload.wikimedia.org/wikipedia/commons/b/b2/Hausziege_04.jpg -O goat.jpg

.. only:: shade

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-4
        :end-before: step-5

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-4
        :end-before: step-5

List objects in your container to see if the upload
was successful, then download the file to verify the md5sum is the
same:

.. only:: fog

    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-5
        :end-before: step-6

    ::

       TBC


    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-6
        :end-before: step-7

    ::

        TBC

    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-7
        :end-before: step-8

    ::

        7513986d3aeb22659079d1bf3dc2468b

.. only:: jclouds

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-5
        :end-before: step-6

    ::

       Objects in fractals:
       SwiftObject{name=an amazing goat,
        uri=https://swift.some.org:8888/v1/AUTH_8997868/fractals/an%20amazing%20goat,
        etag=439884df9c1c15c59d2cf43008180048,
        lastModified=Wed Nov 25 15:09:34 AEDT 2015, metadata={}}

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-6
        :end-before: step-7

    ::

        Fetched: an amazing goat

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-7
        :end-before: step-8

    ::

        MD5 for file goat.jpg: 439884df9c1c15c59d2cf43008180048

.. only:: shade

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-5
        :end-before: step-6

.. only:: shade

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-6
        :end-before: step-7

.. only:: shade

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-7
        :end-before: step-8

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-5
        :end-before: step-6

    ::

       [<Object: name=an amazing goat, size=191874, hash=439884df9c1c15c59d2cf43008180048, provider=OpenStack Swift ...>]


    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-6
        :end-before: step-7

    ::

        <Object: name=an amazing goat, size=954465, hash=7513986d3aeb22659079d1bf3dc2468b, provider=OpenStack Swift ...>

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-7
        :end-before: step-8

    ::

        7513986d3aeb22659079d1bf3dc2468b


Finally, clean up by deleting the test object:

.. only:: fog

    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-8
        :end-before: step-9

.. only:: jclouds

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-8
        :end-before: step-10

.. only:: shade

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-8
        :end-before: step-9

.. only:: shade

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-9
        :end-before: step-10

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-8
        :end-before: step-9

    .. note:: You must pass in objects and not object names to the delete commands.

    Now, no more objects are available in the :code:`fractals` container.

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-9
        :end-before: step-10

    ::

        []

Back up the Fractals from the database on the Object Storage
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Back up the Fractals app images, which are currently stored inside the
database, on Object Storage.

Use the container from above to put the images in:

.. only:: fog

    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-10
        :end-before: step-11

.. only:: jclouds

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-10
        :end-before: step-11

.. only:: shade

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-10
        :end-before: step-11

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-10
        :end-before: step-11

Next, back up all existing fractals from the database to the swift container.
A simple loop takes care of that:

.. note:: Replace :code:`IP_API_1` with the IP address of the API instance.

.. only:: fog

    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-11
        :end-before: step-12

.. only:: jclouds

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-11
        :end-before: step-12

.. only:: shade

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-11
        :end-before: step-12

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-11
        :end-before: step-12

    ::

        <Object: name=025fd8a0-6abe-4ffa-9686-bcbf853b71dc, size=61597, hash=b7a8a26e3c0ce9f80a1bf4f64792cd0c, provider=OpenStack Swift ...>
        <Object: name=26ca9b38-25c8-4f1e-9e6a-a0132a7a2643, size=136298, hash=9f9b4cac16893854dd9e79dc682da0ff, provider=OpenStack Swift ...>
        <Object: name=3f68c538-783e-42bc-8384-8396c8b0545d, size=27202, hash=e6ee0cd541578981c294cebc56bc4c35, provider=OpenStack Swift ...>

    .. note:: Replace :code:`IP_API_1` with the IP address of the API instance.

    .. note:: The example code uses the awesome
              `Requests library <http://docs.python-requests.org/en/latest/>`_.
              Before you try to run the previous script, make sure that
              it is installed on your system.

Extra features
--------------

Delete containers
~~~~~~~~~~~~~~~~~

To delete a container, you must first remove all objects from the container.
Otherwise, the delete operation fails:

.. only:: fog

    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-12
        :end-before: step-13

.. only:: jclouds

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-12
        :end-before: step-13

.. only:: shade

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-12
        :end-before: step-13

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-12
        :end-before: step-13

.. warning:: It is not possible to restore deleted objects. Be careful.

Add metadata to objects
~~~~~~~~~~~~~~~~~~~~~~~

You can complete advanced tasks such as uploading an object with metadata, as
shown in following example. For more information, see the documentation for
your SDK.

.. only:: fog

    This option also uses a bit stream to upload the file, iterating bit
    by bit over the file and passing those bits to Object Storage as they come.
    Compared to loading the entire file in memory and then sending it, this method
    is more efficient, especially for larger files.

    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-13
        :end-before: step-14

.. only:: jclouds

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-13
        :end-before: step-14

.. only:: shade

    .. literalinclude:: ../samples/shade/durability.py
        :start-after: step-13
        :end-before: step-14

.. only:: libcloud

    This option also uses a bit stream to upload the file, iterating bit
    by bit over the file and passing those bits to Object Storage as they come.
    Compared to loading the entire file in memory and then sending it, this method
    is more efficient, especially for larger files.

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-13
        :end-before: step-14

.. todo:: It would be nice to have a pointer here to section 9.

.. only:: libcloud

    Large objects
    ~~~~~~~~~~~~~

    For efficiency, most Object Storage installations treat large objects
    (say, :code:`> 5GB`) differently than smaller objects.

    If you work with large objects, use the :code:`ex_multipart_upload_object`
    call instead of the simpler :code:`upload_object` call. The call splits
    the large object into chunks and creates a manifest so that the chunks can
    be recombined on download. Change the :code:`chunk_size` parameter, in
    bytes, to a value that your cloud can accept.

    .. literalinclude:: ../samples/libcloud/durability.py
        :start-after: step-14
        :end-before: step-15

.. only:: fog

    .. literalinclude:: ../samples/fog/durability.rb
        :start-after: step-14
        :end-before: step-15

.. only:: jclouds

    If you work with large objects, use the :code:`RegionScopedBlobStoreContext`
    class family instead of the ones used so far.

    .. note:: Large file uploads that use the :code:`openstack-swift` provider
              are supported in only jclouds V2, currently in beta. Also, the
              default chunk size is 64 Mb. Consider changing this as homework.

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java
        :start-after: step-14
        :end-before: step-15

.. only:: jclouds

    Complete code sample
    ~~~~~~~~~~~~~~~~~~~~

    This file contains all the code from this tutorial section. This
    class lets you view and run the code.

    Before you run this class, confirm that you have configured it for
    your cloud and the instance running the Fractals application.

    .. literalinclude:: ../samples/jclouds/Durability.java
        :language: java

Next steps
----------

You should now be fairly confident working with Object Storage. You
can find more information about the Object Storage SDK calls at:

.. only:: fog

    https://github.com/fog/fog/blob/master/lib/fog/openstack/docs/storage.md

.. only:: libcloud

    https://libcloud.readthedocs.org/en/latest/storage/api.html

Or, try one of these tutorial steps:

* :doc:`/block_storage`: Migrate the database to block storage, or use
  the database-as-a-service component.
* :doc:`/orchestration`: Automatically orchestrate your application.
* :doc:`/networking`: Learn about complex networking.
* :doc:`/advice`: Get advice about operations.
* :doc:`/craziness`: Learn some crazy things that you might not think to do ;)
