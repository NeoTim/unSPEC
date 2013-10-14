Benchmarking Kernel Build Times
===============================


* Make a RAMDISK

  ::

     $ mkdir RAMDISK

     $ sudo mount -t ramfs none RAMDISK

     $ sudo chmod -R 777 RAMDISK  # ;(


* Get kernel tarball and build it


  ::

     $ cd RAMDISK

     $ wget https://www.kernel.org/pub/linux/kernel/v3.x/testing/linux-3.12-rc5.tar.xz

     $ tar -xJf linux-3.12-rc5.tar.xz

     $ cd linux-3.12-rc5

     $ cp kernel.config .config  # kernel.config is included in this folder

     $ time make -j2  > /dev/null

