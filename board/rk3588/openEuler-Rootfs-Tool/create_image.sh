#!/bin/bash
set -e

OPENEULER_ROOTFS_IMG=$1

ROOTFS_DIR=$2

ROOT_PASSWORD=$3

echo Copy Overlay Files...
cp -rfp overlay/* ${ROOTFS_DIR}/
cp -rfp libs/* ${ROOTFS_DIR}/usr/lib64
cp -rfp include/* ${ROOTFS_DIR}/usr/include
cp -rfp rootfs-release ${ROOTFS_DIR}/etc

echo Setup Rootfs...
cat << EOF | chroot $ROOTFS_DIR

chmod +x /etc/rc.d/rc.local
echo "echo performance > /sys/class/devfreq/dmc/governor" >> /etc/rc.local

echo ${ROOT_PASSWORD} | passwd --stdin root

echo openEuler-rk3588 > /etc/hostname

EOF

echo Creating rootfs image...
if [ -f ${OPENEULER_ROOTFS_IMG} ]; then
    rm -f ${OPENEULER_ROOTFS_IMG}
fi
dd if=/dev/zero of=${OPENEULER_ROOTFS_IMG} bs=1M count=0 seek=6000
mkfs.ext4 -d ${ROOTFS_DIR} ${OPENEULER_ROOTFS_IMG}

echo Finishing.....
rm -rf ${ROOTFS_DIR}

e2fsck -p -f ${OPENEULER_ROOTFS_IMG}
resize2fs -M ${OPENEULER_ROOTFS_IMG}

echo Create ${OPENEULER_ROOTFS_IMG} Done!
