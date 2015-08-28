===============
Getting started
===============

Who should read this guide
~~~~~~~~~~~~~~~~~~~~~~~~~~

This guide is for software developers who want to deploy applications to
DreamCompute, which is based on OpenStack.

We assume that you're an experienced programmer who has not created a cloud
application in general or an OpenStack application in particular.

If you're familiar with OpenStack, this section teaches you how to program
with its components.

What you will learn
~~~~~~~~~~~~~~~~~~~

Deploying applications in a cloud environment can be very different from
deploying them in a traditional IT environment. This guide teaches you how to
deploy applications on OpenStack and some best practices for cloud application
development.

A general overview
~~~~~~~~~~~~~~~~~~

This tutorial shows two applications. The first application is a simple
fractal generator that uses mathematical equations to generate beautiful
`fractal images <http://en.wikipedia.org/wiki/Fractal>`_. We show you this
application in its entirety so that you can compare it to a second, more
robust, application.

The second application is an OpenStack application that enables you to:

* Create and destroy compute resources. These resources are virtual
  machine instances where the Fractals application runs.
* Make cloud-related architecture decisions such as turning
  functions into micro-services and modularizing them.
* Scale available resources up and down.
* Use Object and Block storage for file and database persistence.
* Use Orchestration services to automatically adjust to the environment.
* Customize networking for better performance and segregation.
* Explore and apply advanced OpenStack cloud features.

Choose your OpenStack SDK
~~~~~~~~~~~~~~~~~~~~~~~~~

Anyone with a programming background can easily read the code in this guide.
Although this guide focuses on a particular SDK, you can use other languages
and toolkits with the OpenStack cloud:

============== ============= ================================================================= ====================================================
Language        Name          Description                                                       URL
============== ============= ================================================================= ====================================================
Python         Libcloud      A Python-based library managed by the Apache Foundation.
                             This library enables you to work with multiple types of clouds.   https://libcloud.apache.org
Python         OpenStack SDK A Python-based library specifically developed for OpenStack.      https://github.com/stackforge/python-openstacksdk
Python         Shade         A Python-based library developed by OpenStack Infra team to       https://github.com/openstack-infra/shade
                             operate multiple OpenStack clouds.
Java           jClouds       A Java-based library. Like Libcloud, it's also managed by the     https://jclouds.apache.org
                             Apache Foundation and works with multiple types of clouds.
Ruby           fog           A Ruby-based SDK for multiple clouds.                             https://github.com/fog/fog/blob/master/lib/fog/openstack/docs/getting_started.md
node.js        pkgcloud      A Node.js-based SDK for multiple clouds.                          https://github.com/pkgcloud/pkgcloud
PHP            php-opencloud A library for developers using PHP to work with OpenStack clouds. http://php-opencloud.com/
.NET Framework OpenStack SDK A .NET-based library enables you to write C++ or C# code for      https://www.nuget.org/packages/openstack.net
               for Microsoft Microsoft applications.
               .NET
============== ============= ================================================================= ====================================================

For a list of available SDKs, see `Software Development Kits <https://wiki.openstack.org/wiki/SDKs>`_.

Other versions of this guide show you how to use the other SDKs and
languages to complete these tasks. If you're a developer for another toolkit
that you would like this guide to include, feel free to submit code snippets.
You can contact `OpenStack Documentation team <https://wiki.openstack.org/Documentation>`_
members for more information.

What you need
-------------

We assume that you already have access to DreamCompute. If so, you
have been assigned a project, sometimes called a tenant, which has a
maximum quota and for our purposes you will need to be able to create
at least six instances. Because the Fractals application runs in Ubuntu,
Debian, Fedora-based, and openSUSE-based distributions, you must create
instances that use one of these operating systems.

To interact with the cloud, you must also have

.. only:: dotnet

      `OpenStack Cloud SDK for Microsoft .NET 1.4.0.1 or later installed
      <https://www.nuget.org/packages/openstack.net>`_.

      .. note::

         To install the OpenStack .NET SDK, use the NeGet Package Manager that
         is included with Visual Studio and Xamarin Studio. You simply add a
         package named 'openstack.net' and the NeGet Package Manager
         automatically installs the necessary dependencies.

      .. warning::

         This document has not yet been completed for the .NET SDK.

.. only:: fog

      `fog 1.19 or higher installed
      <http://www.fogproject.org/wiki/index.php?title=FOGUserGuide#Installing_FOG>`_
      and working with ruby gems 1.9.

      .. warning::

         This document has not yet been completed for the fog SDK.

.. only:: jclouds

    `jClouds 1.8 or higher installed <https://jclouds.apache.org/start/install>`_.

    .. warning::

       This document has not yet been completed for the jclouds SDK.

.. only:: libcloud

  `libcloud 0.15.1 or higher installed
  <https://libcloud.apache.org/getting-started.html>`_.

.. only:: pkgcloud

      `pkgcloud 1.2 or higher installed
      <https://github.com/pkgcloud/pkgcloud#getting-started>`_.

     .. highlight:: javascript

.. only:: openstacksdk

    the OpenStack SDK installed.

    .. warning::

       This document has not yet been completed for the OpenStack SDK.

.. only:: phpopencloud

    `a recent version of php-opencloud installed <http://docs.php-opencloud.com/en/latest/>`_.

    .. warning::

       This document has not yet been completed for the php-opencloud SDK.

.. only:: shade

     `a recent version of shade library installed <https://pypi.python.org/pypi/shade/0.11.0>`_.

     .. note:: Before proceeding, install the latest version of shade.

Download the DreamCompute RC file from
https://dashboard.dreamcompute.com/project/access_and_security/api_access/openrc/
to obtain the following information.

* auth URL
* user name
* password
* project ID or name (projects are also known as tenants)
* cloud region

Be aware that the "auth URL" does not include the path. Your auth URL
should look like this.

.. code-block:: python

        https://keystone.dream.io/

How you'll interact with DreamCompute
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this tutorial, you interact with DreamCompute through the SDK that you
chose in "Choose your OpenStack SDK." This guide assumes that you know how
to run code snippets in your language of choice.

.. only:: fog

    .. literalinclude:: ../samples/fog/getting_started.rb
        :start-after: step-1
        :end-before: step-2

.. only:: libcloud

    To try it, add the following code to a Python script (or use an
    interactive Python shell) by calling :code:`python -i`.

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-1
        :end-before: step-2

.. only:: openstacksdk

    .. code-block:: python

      from openstack import connection
      conn = connection.Connection(auth_url="http://controller:5000/v3",
                                   user_name="your_auth_username",
                                   password="your_auth_password", ...)

.. only:: pkgcloud

    To try it, add the following code to a script (or use an
    interactive nodejs shell) by calling :code:`node`.

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-1
        :end-before: step-2

.. only:: dotnet

    To use the OpenStack .NET SDK, add the following code in the required
    namespace section.

    .. code-block:: c#

        using net.openstack.Core.Domain;
        using net.openstack.Core.Providers;
        using net.openstack.Providers.Rackspace;

    Because all service endpoints use the Identity Service for authentication
    and authorization, place the following code in the 'void Main()'
    entry-point function.

    .. literalinclude:: ../samples/dotnet/getting_started.cs
        :language: c#
        :dedent: 3
        :start-after: step-1
        :end-before: step-2


.. note:: Because the tutorial reuses the :code:`conn` object,
          make sure that you always have one handy.

.. only:: libcloud

    .. note:: If you receive the
              :code:`libcloud.common.types.InvalidCredsError: 'Invalid
              credentials with the provider'` exception when you run
              one of these API calls, double-check your credentials.

    .. note:: If your provider does not support regions, try a
              blank string ('') for the `region_name`.

.. only:: shade

    Use your credentials above to specify the cloud provider name,
    user name, password, project_name and region_name in the file
    :file:`~/.config/openstack/clouds.yml`.

    .. literalinclude:: ../samples/shade/clouds.yml
        :language: yaml

    .. note:: If you do use a public cloud `known by shade
              <http://git.openstack.org/cgit/openstack/os-client-config/tree/os_client_config/vendors>`_,
              you can avoid specifying :code:`auth_url:` and instead specify
              :code:`profile: $PROVIDER_NAME` in the clouds.yml file.

    .. literalinclude::  ../samples/shade/getting_started.py
        :start-after: step-1
        :end-before: step-2

Flavors and images
~~~~~~~~~~~~~~~~~~

To run your application, you must launch an instance. This instance serves as
a virtual machine.

To launch an instance, you choose a flavor and an image. The flavor represents
the size of the instance, including the number of CPUs and amount of RAM and
disk space. An image is a prepared OS installation from which you clone your
instance. When you boot instances in a public cloud, larger flavors can be
more expensive than smaller ones in terms of resources and monetary cost.

To list the images that are available in your cloud, run some API calls:

.. only:: fog

    .. literalinclude:: ../samples/fog/getting_started.rb
        :start-after: step-2
        :end-before: step-3

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-2
        :end-before: step-3

    This code returns output like this:

    .. code-block:: python

        <NodeImage: id=e81771c0-2944-405c-ba92-3deb0e1b4ce3, name=CentOS-7.0, driver=OpenStack  ...>
        <NodeImage: id=90d5e049-aaed-4abc-aa75-60c2b1ed6516, name=Ubuntu-14.04, driver=OpenStack  ...>
        <NodeImage: id=f044ae8f-e0e1-4fb4-baff-0363c19a6638, name=CoreOS, driver=OpenStack  ...>
        <NodeImage: id=2827d7cc-8cbb-4ce9-9b61-dadc2436144e, name=Fedora-20, driver=OpenStack  ...>
        <NodeImage: id=42a0101d-31c1-4c09-a70d-8f75f887ee27, name=Fedora-21, driver=OpenStack  ...>
        <NodeImage: id=683e165f-96b1-4ee5-8747-d15aade0dbff, name=CentOS-6.6, driver=OpenStack  ...>
        <NodeImage: id=de4d521b-6630-4361-8b9a-b2fa640cdfa0, name=CentOS-6.5, driver=OpenStack  ...>
        <NodeImage: id=5011c04a-f760-4dc5-9772-7e30d98647e6, name=Ubuntu-12.04-Precise, driver=OpenStack  ...>
        <NodeImage: id=b4efbc2a-6130-4f2e-b436-55a618c4de20, name=Debian-7.0-Wheezy, driver=OpenStack  ...>

.. only:: pkgcloud

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-2
        :end-before: step-3

    This code returns output like this:

    .. code-block:: none

        id: 6c7f5627-ca40-4781-ac34-4d9af53d4b29
        name: Fedora 22 - Updated
        created: 2015-08-17T03:53:17Z
        updated: 2015-08-17T04:53:12Z
        status: ACTIVE

        ...
        id: 2cccbea0-cea9-4f86-a3ed-065c652adda5
        name: Ubuntu 14.04
        created: 2015-08-13T02:25:10Z
        updated: 2015-08-13T02:43:38Z
        status: ACTIVE

.. only:: dotnet

    .. literalinclude:: ../samples/dotnet/getting_started.cs
        :language: c#
        :dedent: 3
        :start-after: step-2
        :end-before: step-3

    This code returns output like this:

    .. code-block:: none

        Image Id: dce1a289-2ad5-4aaa-a7a6-fe30adc2094e - Image Name: snap1
        Image Id: 97f55846-6ea5-4e9d-b437-bda97586bd0c - Image Name: cirros-0.3.4-x86_64-uec
        Image Id: 3e0e8270-0da4-4fec-bfc7-eeb763604cad - Image Name: cirros-0.3.4-x86_64-uec-ramdisk
        Image Id: 0b151382-d2f1-44d7-835b-6408bd523917 - Image Name: cirros-0.3.4-x86_64-uec-kernel

.. only:: shade

    .. literalinclude:: ../samples/shade/getting_started.py
        :language: python
        :start-after: step-2
        :end-before: step-3

    This code returns output like this:

    .. code-block:: none

        checksum: 750a56555d4ec7303f5dc33b007ff632
        container_format: bare
        created_at: '2014-07-14T19:02:15Z'
        direct_url:
        rbd://7e14670e-a6f8-445b-b632-4b79bafc4781/masseffect-images/b4efbc2a-6130-4f2e-b436-55a618c4de20/snap
        disk_format: raw
        file: /v2/images/b4efbc2a-6130-4f2e-b436-55a618c4de20/file
        id: b4efbc2a-6130-4f2e-b436-55a618c4de20
        min_disk: 10
        min_ram: 1024
        name: Debian-7.0-Wheezy
        owner: 0bacd8121bb548698f340455b38bf561
        protected: false
        schema: /v2/schemas/image
        size: 5242880000
        status: active
        tags: []
        updated_at: '2014-10-15T22:42:52Z'
        visibility: public


You can also get information about available flavors:

.. only:: fog

    .. literalinclude:: ../samples/fog/getting_started.rb
        :start-after: step-3
        :end-before: step-4

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-3
        :end-before: step-4

    This code returns output like this:

    .. code-block:: python

        <OpenStackNodeSize: id=100, name=subsonic, ram=1024, disk=80, bandwidth=None, price=0.0, driver=OpenStack, vcpus=1,  ...>
        <OpenStackNodeSize: id=200, name=supersonic, ram=2048, disk=80, bandwidth=None, price=0.0, driver=OpenStack, vcpus=1,  ...>
        <OpenStackNodeSize: id=300, name=lightspeed, ram=4096, disk=80, bandwidth=None, price=0.0, driver=OpenStack, vcpus=2,  ...>
        <OpenStackNodeSize: id=400, name=warpspeed, ram=8192, disk=80, bandwidth=None, price=0.0, driver=OpenStack, vcpus=4,  ...>
        <OpenStackNodeSize: id=500, name=hyperspeed, ram=16384, disk=80, bandwidth=None, price=0.0, driver=OpenStack, vcpus=8,  ...>
        <OpenStackNodeSize: id=600, name=ridiculous, ram=32768, disk=80, bandwidth=None, price=0.0, driver=OpenStack, vcpus=16,  ...>
        <OpenStackNodeSize: id=700, name=ludicrous, ram=65536, disk=80, bandwidth=None, price=0.0, driver=OpenStack, vcpus=32,  ...>
        <OpenStackNodeSize: id=800, name=plaid, ram=131072, disk=80, bandwidth=None, price=0.0, driver=OpenStack, vcpus=64,  ...>

.. only:: pkgcloud

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-3
        :end-before: step-4

    This code returns output like this:

    .. code-block:: none

        id: c46104de-d5fd-4567-ab0b-3dcfd117bd99
        name: m2.xlarge
        ram: 49152
        disk: 30
        vcpus: 12

        ...
        id: cba9ea52-8e90-468b-b8c2-777a94d81ed3
        name: m1.small
        ram: 2048
        disk: 20
        vcpus: 1

.. only:: dotnet

    .. literalinclude:: ../samples/dotnet/getting_started.cs
        :language: c#
        :dedent: 3
        :start-after: step-3
        :end-before: step-4

    This code returns output like this:

    .. code-block:: none

        Flavor Id: 1 - Flavor Name: m1.tiny
        Flavor Id: 2 - Flavor Name: m1.small
        Flavor Id: 3 - Flavor Name: m1.medium
        Flavor Id: 4 - Flavor Name: m1.large
        Flavor Id: 42 - Flavor Name: m1.nano
        Flavor Id: 5 - Flavor Name: m1.xlarge
        Flavor Id: 84 - Flavor Name: m1.micro

.. only:: shade

    .. literalinclude:: ../samples/shade/getting_started.py
        :language: python
        :start-after: step-3
        :end-before: step-4

    This code returns output like this:

    .. code-block:: none

        HUMAN_ID: true
        NAME_ATTR: name
        OS-FLV-DISABLED:disabled: false
        OS-FLV-EXT-DATA:ephemeral: 0
        disk: 80
        ephemeral: 0
        human_id: supersonic
        id: '200'
        is_public: true
        links:
        -   href:
            https://compute.dream.io:8774/v2/5d013ac5962749a49af7ff18c2fb228c/flavors/200
            rel: self
        -   href:
            https://compute.dream.io:8774/5d013ac5962749a49af7ff18c2fb228c/flavors/200
            rel: bookmark
        name: supersonic
        os-flavor-access:is_public: true
        ram: 2048
        swap: ''
        vcpus: 1

Your images and flavors will be different, of course.

Choose an image and flavor for your instance. You need about 1GB RAM, 1 CPU,
and a 1GB disk. This example uses the Ubuntu image with a small
flavor, which is a safe choice. In subsequent tutorial sections in
this guide, you must change the image and flavor IDs to correspond to
the image and flavor that you choose.

If the image that you want is not available in your cloud, you can usually
upload one depending on your cloud's policy settings. For information about
how to upload images, see
`obtaining images <http://docs.openstack.org/image-guide/content/ch_obtaining_images.html>`_.

Set the image and size variables to appropriate values for your cloud. We'll
use these variables in later sections.

First, tell the connection to get a specified image by using the ID of the
image that you picked in the previous section:

.. only:: fog

    .. literalinclude:: ../samples/fog/getting_started.rb
        :start-after: step-4
        :end-before: step-5

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-4
        :end-before: step-5

    This code returns output like this:

    .. code-block:: python

        <NodeImage: id=90d5e049-aaed-4abc-aa75-60c2b1ed6516, name=Ubuntu-14.04, driver=OpenStack  ...>

.. only:: pkgcloud

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-4
        :end-before: step-5

    This code returns output like this:

    .. code-block:: none

        id: 2cccbea0-cea9-4f86-a3ed-065c652adda5
        name: Ubuntu 14.04
        created: 2015-08-13T02:25:10Z
        updated: 2015-08-13T02:43:38Z
        status: ACTIVE

.. only:: dotnet

    .. literalinclude:: ../samples/dotnet/getting_started.cs
        :language: c#
        :dedent: 3
        :start-after: step-4
        :end-before: step-5

    This code returns output like this:

    .. code-block:: none

        Image Id: 97f55846-6ea5-4e9d-b437-bda97586bd0c - Image Name: cirros-0.3.4-x86_64-uec

.. only:: shade

    .. literalinclude:: ../samples/shade/getting_started.py
        :start-after: step-4
        :end-before: step-5

    This code returns output like this:

    .. code-block:: none

        checksum: da578dd59289a35a0ac7744a0bd85cf5
        container_format: bare
        created_at: '2014-10-27T22:05:37Z'
        direct_url:
        rbd://7e14670e-a6f8-445b-b632-4b79bafc4781/masseffect-images/c55094e9-699c-4da9-95b4-2e2e75f4c66e/snap
        disk_format: raw
        file: /v2/images/c55094e9-699c-4da9-95b4-2e2e75f4c66e/file
        id: c55094e9-699c-4da9-95b4-2e2e75f4c66e
        min_disk: 0
        min_ram: 0
        name: Ubuntu-14.04-Trusty
        owner: 0bacd8121bb548698f340455b38bf561
        protected: false
        schema: /v2/schemas/image
        size: 10737418240
        status: active
        tags: []
        updated_at: '2014-10-27T22:08:55Z'
        visibility: public


Next, choose which flavor you want to use:

.. only:: fog

    .. literalinclude:: ../samples/fog/getting_started.rb
        :start-after: step-5
        :end-before: step-6

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-5
        :end-before: step-6

    This code returns output like this:

    .. code-block:: python

        <OpenStackNodeSize: id=100, name=subsonic, ram=1024, disk=80, bandwidth=None, price=0.0, driver=OpenStack, vcpus=1,  ...>

.. only:: pkgcloud

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-5
        :end-before: step-6

    This code returns output like this:

    .. code-block:: none


        id: cba9ea52-8e90-468b-b8c2-777a94d81ed3
        name: m1.small
        ram: 2048
        disk: 20
        vcpus: 1

.. only:: dotnet

    .. literalinclude:: ../samples/dotnet/getting_started.cs
        :language: c#
        :dedent: 3
        :start-after: step-5
        :end-before: step-6

    This code returns output like this:

    .. code-block:: none

        Flavor Id: 2 - Flavor Name: m1.small

.. only:: shade

    Because shade accepts either the ID or name in most API calls, specify the
    name for the flavor:

    .. literalinclude:: ../samples/shade/getting_started.py
        :start-after: step-5
        :end-before: step-6

    This code returns output like this:

    .. code-block:: none

        HUMAN_ID: true
        NAME_ATTR: name
        OS-FLV-DISABLED:disabled: false
        OS-FLV-EXT-DATA:ephemeral: 0
        disk: 80
        ephemeral: 0
        human_id: subsonic
        id: '100'
        is_public: true
        links:
        -   href:
            https://compute.dream.io:8774/v2/5d013ac5962749a49af7ff18c2fb228c/flavors/100
            rel: self
        -   href:
            https://compute.dream.io:8774/5d013ac5962749a49af7ff18c2fb228c/flavors/100
            rel: bookmark
        name: subsonic
        os-flavor-access:is_public: true
        ram: 1024
        swap: ''
        vcpus: 1

Now, you're ready to launch the instance.

Launch an instance
~~~~~~~~~~~~~~~~~~

Use your selected image and flavor to create an instance.

.. note:: The following instance creation example assumes that you have a
          single-tenant network. If you receive the 'Exception: 400 Bad
          Request Multiple possible networks found, use a Network ID to be
          more specific' error, you have multiple-tenant networks. You
          must add a `networks` parameter to the call that creates the
          server. See :doc:`/appendix` for details.

Create the instance.

.. note:: Your SDK might call an instance a 'node' or 'server'.

.. only:: fog

    .. literalinclude:: ../samples/fog/getting_started.rb
        :start-after: step-6
        :end-before: step-7

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-6
        :end-before: step-7

    This code returns output like this:

    .. code-block:: python

        <Node: uuid=3c8fd6fc02916c26d75b5e9bfa53d8b1315671be, name=testing, state=PENDING, public_ips=[], private_ips=[], provider=OpenStack ...>

.. only:: openstacksdk

    .. code-block:: python

       args = {
           "name": "testing",
           "flavorRef": flavor,
           "imageRef": image,
       }
       instance = conn.compute.create_server(**args)

.. only:: pkgcloud

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-6
        :end-before: step-7

    This code returns output like this:

    .. code-block:: none

        0d7968dc-4bf4-4e01-b822-43c9c1080d77

.. only:: dotnet

    .. literalinclude:: ../samples/dotnet/getting_started.cs
        :language: c#
        :dedent: 3
        :start-after: step-6
        :end-before: step-7

    This code returns output like this:

    .. code-block:: none

        Instance Id: 4e480ef1-68f0-491f-b237-d9b7f500ef24 at net.openstack.Core.Domain.Link[]

.. only:: shade

    .. literalinclude:: ../samples/shade/getting_started.py
        :start-after: step-6
        :end-before: step-7

If you list existing instances:

.. only:: fog

    .. literalinclude:: ../samples/fog/getting_started.rb
        :start-after: step-7
        :end-before: step-8

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-7
        :end-before: step-8

.. only:: pkgcloud

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-7
        :end-before: step-8

.. only:: dotnet

    .. literalinclude:: ../samples/dotnet/getting_started.cs
        :language: c#
        :dedent: 3
        :start-after: step-7
        :end-before: step-8

.. only:: shade

    .. literalinclude:: ../samples/shade/getting_started.py
        :start-after: step-7
        :end-before: step-8


The new instance appears.

.. only:: libcloud

    .. code-block:: python

        <Node: uuid=3c8fd6fc02916c26d75b5e9bfa53d8b1315671be, name=testing, state=RUNNING, public_ips=[], private_ips=[], provider=OpenStack ...>

.. only:: openstacksdk

    .. code-block:: python

       instances = conn.compute.list_servers()
       for instance in instances:
           print(instance)

.. only:: pkgcloud

    .. code-block:: none

        ...
        id: '0d7968dc-4bf4-4e01-b822-43c9c1080d77',
        name: 'testing',
        status: 'PROVISIONING',
        progress: 0,
        imageId: '2cccbea0-cea9-4f86-a3ed-065c652adda5',
        adminPass: undefined,
        addresses: {},
        metadata: {},
        flavorId: '3',
        hostId: 'b6ee757ed678e8c6589ae8cce405eeded89ac914daec73e45a5c50b8',
        created: '2015-06-30T08:17:39Z',
        updated: '2015-06-30T08:17:44Z',
        ...

.. only:: dotnet

    .. code-block:: none

        Instance Id: 4e480ef1-68f0-491f-b237-d9b7f500ef24 at net.openstack.Core.Domain.Link[]

.. only:: shade

   .. code-block:: none

       HUMAN_ID: true
        NAME_ATTR: name
        OS-DCF:diskConfig: MANUAL
        OS-EXT-AZ:availability_zone: iad-1
        OS-EXT-STS:power_state: 1
        OS-EXT-STS:task_state: null
        OS-EXT-STS:vm_state: active
        OS-SRV-USG:launched_at: '2015-07-20T20:31:10.000000'
        OS-SRV-USG:terminated_at: null
        accessIPv4: ''
        accessIPv6: ''
        addresses:
            private-network:
            -   OS-EXT-IPS-MAC:mac_addr: fa:16:3e:60:f5:cd
                OS-EXT-IPS:type: fixed
                addr: 2607:f298:6050:4e14:f816:3eff:fe60:f5cd
                version: 6
            -   OS-EXT-IPS-MAC:mac_addr: fa:16:3e:60:f5:cd
                OS-EXT-IPS:type: fixed
                addr: 10.10.10.14
                version: 4
        config_drive: ''
        created: '2015-07-20T20:30:23Z'
        flavor:
            id: '100'
            links:
            -   href:
                https://compute.dream.io:8774/5d013ac5962749a49af7ff18c2fb228c/flavors/100
                rel: bookmark
        hostId: f71865b497e6fa71063e292b11846eb64b5a41cd5c00fbb7465b6a48
        human_id: testing
        id: 67ecebdc-daff-4d84-bd04-bc76c67b48ec
        image:
            id: c55094e9-699c-4da9-95b4-2e2e75f4c66e
            links:
            -   href:
                https://compute.dream.io:8774/5d013ac5962749a49af7ff18c2fb228c/images/c55094e9-699c-4da9-95b4-2e2e75f4c66e
                rel: bookmark
        key_name: null
        links:
        -   href:
            https://compute.dream.io:8774/v2/5d013ac5962749a49af7ff18c2fb228c/servers/67ecebdc-daff-4d84-bd04-bc76c67b48ec
            rel: self
        -   href:
            https://compute.dream.io:8774/5d013ac5962749a49af7ff18c2fb228c/servers/67ecebdc-daff-4d84-bd04-bc76c67b48ec
            rel: bookmark
        metadata: {}
        name: testing
        networks:
            private-network:
            - 2607:f298:6050:4e14:f816:3eff:fe60:f5cd
            - 10.10.10.14
        os-extended-volumes:volumes_attached: []
        progress: 0
        security_groups:
        -   name: default
        status: ACTIVE
        tenant_id: 5d013ac5962749a49af7ff18c2fb228c
        updated: '2015-07-20T20:31:10Z'
        user_id: bfd3dbf1c8a242cd90884408de547bb9

Before you continue, you must do one more thing.

Destroy an instance
~~~~~~~~~~~~~~~~~~~

Cloud resources such as running instances that you no longer use can cost
money. Destroy cloud resources to avoid unexpected expenses.

.. only:: fog

    .. literalinclude:: ../samples/fog/getting_started.rb
        :start-after: step-8
        :end-before: step-9

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-8
        :end-before: step-9

.. only:: pkgcloud

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-8
        :end-before: step-9

.. only:: dotnet

    .. literalinclude:: ../samples/dotnet/getting_started.cs
        :language: c#
        :dedent: 3
        :start-after: step-8
        :end-before: step-9

.. only:: shade

    .. literalinclude:: ../samples/shade/getting_started.py
        :start-after: step-8
        :end-before: step-9

If you list the instances again, the instance disappears.

Leave your shell open to use it for another instance deployment in this
section.

Deploy the application to a new instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that you know how to create and destroy instances, you can deploy the
sample application. The instance that you create for the application is
similar to the first instance that you created, but this time, we'll briefly
introduce a few extra concepts.

.. note:: Internet connectivity from your cloud instance is required
          to download the application.

When you create an instance for the application, you'll want to give it a bit
more information than you supplied to the bare instance that you just created
and destroyed. We'll go into more detail in later sections, but for now,
simply create the following resources so that you can feed them to the
instance:

* A key pair. To access your instance, you must import an SSH public key into
  OpenStack to create a key pair. OpenStack installs this key pair on the new
  instance. Typically, your public key is written to :code:`.ssh/id_rsa.pub`. If
  you do not have an SSH public key file, follow
  `these instructions <https://help.github.com/articles/generating-ssh- keys/>`_ first.
  We'll cover these instructions in depth in :doc:`/introduction`.

.. only:: fog

    .. warning:: This section has not been completed.

.. only:: libcloud

    In the following example, :code:`pub_key_file` should be set to
    the location of your public SSH key file.

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-9
        :end-before: step-10

    ::

       <KeyPair name=demokey fingerprint=aa:bb:cc... driver=OpenStack>

.. only:: pkgcloud

    In the following example, :code:`pub_key_file` should be set to
    the location of your public SSH key file.

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-9
        :end-before: step-10

.. only:: shade

    In the following example, :code:`pub_key_file` should be set to
    the location of your public SSH key file.

    .. literalinclude:: ../samples/shade/getting_started.py
        :start-after: step-9
        :end-before: step-10


* Network access. DreamCompute has a default security group that will
  work for our purposes. If you want, you can create another security
  group by following along below. This security group allows HTTP
  and SSH access. We'll go into more detail in :doc:`/introduction`.

.. only:: fog

    .. literalinclude:: ../samples/fog/getting_started.rb
        :start-after: step-10
        :end-before: step-11

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-10
        :end-before: step-11

.. only::  pkgcloud

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-10
        :end-before: step-11

.. only:: shade

    .. literalinclude:: ../samples/shade/getting_started.py
        :start-after: step-10
        :end-before: step-11

* User data. During instance creation, you can provide user data to OpenStack to
  configure instances after they boot. The cloud-init service applies the
  user data to an instance. You must pre-install the cloud-init service on your
  chosen image. We'll go into more detail in :doc:`/introduction`.

.. only:: fog

    .. warning:: This section has not been completed.

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-11
        :end-before: step-12

.. only:: pkgcloud

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-11
        :end-before: step-12

.. only:: shade

    .. literalinclude:: ../samples/shade/getting_started.py
        :start-after: step-11
        :end-before: step-12

Now, you can boot and configure the instance.

Boot and configure an instance
------------------------------

Use the image, flavor, key pair, and userdata to create an instance. After you
request the instance, wait for it to build.

.. only:: fog

    .. warning:: This section has not been completed.

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-12
        :end-before: step-13

.. only:: pkgcloud

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-12
        :end-before: step-13

.. only:: shade

    The shade framework can select and assign a free floating IP quickly

    .. literalinclude:: ../samples/shade/getting_started.py
        :start-after: step-12
        :end-before: step-13

When the instance boots, the `ex_userdata` variable value instructs the
instance to deploy the Fractals application.

Associate a floating IP for external connectivity
-------------------------------------------------

We'll cover networking in detail in :doc:`/networking`.

To see the application running, you must know where to look for it. By
default, your instance has outbound network access. To make your instance
reachable from the Internet, you need an IP address. By default in some cases,
your instance is provisioned with a publicly rout-able IP address. In this
case, you'll see an IP address listed under `public_ips` or `private_ips` when
you list the instances. If not, you must create and attach a floating IP
address to your instance.

.. only:: fog

    .. warning:: This section has not been completed.

.. only:: libcloud

    Use :code:`ex_list_floating_ip_pools()` and select the first floating IP
    address pool. Allocate this pool to your project and attach it to your
    instance.

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-13
        :end-before: step-14

    This code returns the floating IP address:

    ::

        <OpenStack_1_1_FloatingIpAddress: id=4536ed1e-4374-4d7f-b02c-c3be2cb09b67, ip_addr=203.0.113.101, pool=<OpenStack_1_1_FloatingIpPool: name=floating001>, driver=<libcloud.compute.drivers.openstack.OpenStack_1_1_NodeDriver object at 0x1310b50>>

    You can then attach it to the instance:

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-14
        :end-before: step-15


.. only:: pkgcloud

    Use :code:`getFloatingIps` to check for unused addresses, selecting the
    first one if available, otherwise use :code:`allocateNewFloatingIp` to
    allocate a new Floating IP to your project from the default address pool.

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-13
        :end-before: step-14

    This code returns the floating IP address:

    ::

        203.0.113.101

    You can then attach it to the instance:

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-14
        :end-before: step-15

.. only:: shade

    .. literalinclude:: ../samples/shade/getting_started.py
        :start-after: step-13
        :end-before: step-14


Run the script to start the deployment.

Access the application
----------------------

Deploying application data and configuration to the instance can take some
time. Consider enjoying a cup of coffee while you wait. After the application
deploys, you can visit the awesome graphic interface at the following link
by using your preferred browser.

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/getting_started.py
        :start-after: step-15

.. only:: pkgcloud

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
        :start-after: step-15

.. only:: shade

    .. literalinclude:: ../samples/shade/getting_started.py
        :start-after: step-15

.. note:: If you do not use floating IPs, substitute another IP address as appropriate

.. figure:: images/screenshot_webinterface.png
    :width: 800px
    :align: center
    :height: 600px
    :alt: screenshot of the webinterface
    :figclass: align-center

Next steps
~~~~~~~~~~

Don't worry if these concepts are not yet completely clear. In
:doc:`/introduction`, we explore these concepts in more detail.

* :doc:`/scaling_out`: Learn how to scale your application
* :doc:`/durability`: Learn how to use Object Storage to make your application durable
* :doc:`/block_storage`: Migrate the database to block storage, or use
  the database-as-a-service component
* :doc:`/orchestration`: Automatically orchestrate your application
* :doc:`/networking`: Learn about complex networking
* :doc:`/advice`: Get advice about operations
* :doc:`/craziness`: Learn some crazy things that you might not think to do ;)

.. todo:: List the next sections here or simply reference introduction.

Complete code sample
~~~~~~~~~~~~~~~~~~~~

The following file contains all of the code from this section of the
tutorial. This comprehensive code sample lets you view and run the code
as a single script.

Before you run this script, confirm that you have set your authentication
information, the flavor ID, and image ID.

.. only:: libcloud

    .. literalinclude:: ../samples/libcloud/getting_started.py
       :language: python

.. only:: pkgcloud

    .. literalinclude:: ../samples/pkgcloud/getting_started.js
       :language: javascript

.. only:: dotnet

    .. literalinclude:: ../samples/dotnet/getting_started.cs
       :language: c#

.. only:: shade

    .. literalinclude:: ../samples/libcloud/getting_started.py
       :language: python
