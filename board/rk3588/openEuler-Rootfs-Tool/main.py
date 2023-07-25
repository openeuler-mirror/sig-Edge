#!/usr/bin/env python3

import os
import json
import re
import shutil
import subprocess
import datetime
import uuid
import os.path as path

ROOTFS_MOUNT_POINT = "rootfs_mnt"
CONFIG_FILE = "config.json"
DATE_FORMART = "%Y-%m-%d_%H:%M:%S"
ROOTFS_RELEASE_FILE = "rootfs-release"


def setup_repo_file(config):

    # Clean the repo directory 
    repo_dir_path = "/etc/yum.repos.d"
    if os.path.exists(repo_dir_path):
        shutil.rmtree(repo_dir_path)
    os.mkdir(repo_dir_path)

    # If defined Custom Repo, use the repo file
    # Or create the repo file with templet
    if config["CustomRepoEnable"]:
        repo_file = config["CustomRepoFile"]
        shutil.copy(repo_file,repo_dir_path)
        return

    repo_templet_file = "openeuler_templet.repo"

    if config["MirrorRepoEnable"]:
        repo_url = config["MirrorRepoSource"]
    else:
        repo_url = "repo.openeuler.org"

    target_verison = config["TargetVersion"]

    # Create the target repo file
    with open(repo_templet_file, 'r') as file:
        data = file.read()
        data = data.replace("{repo_url}", repo_url)
        data = data.replace("{target_version}", target_verison)

    with open(path.join(repo_dir_path,"openEuler.repo"), 'w') as file:
        file.write(data)

def generate_rootfs_release(config):
    target = {}

    target["date"] = datetime.datetime.now().strftime(DATE_FORMART)
    target["git"] = subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()
    target["uuid"] = str(uuid.uuid1())
    target["config"] = config

    with open(ROOTFS_RELEASE_FILE, "w") as fd :
        json.dump(target,fd, indent =4)


def get_package_name_list(rpmlistfile , remove_package_list) -> list:

    pattern = re.compile("^.+(?=-[\d|.|\w]+-)")

    with open(rpmlistfile,"r") as f:
        data = f.readlines()

    packageList = []

    for line in data:
        name = pattern.search(line).group()

        # Remove package form the list
        if any(filter(lambda x: x in name, remove_package_list)):
            continue

        packageList.append(name)
   
    return packageList

if __name__ =="__main__":

    with open(CONFIG_FILE) as fd:
        config = json.load(fd)

    rpmlist_file = config["SourceFile"]
    image_name = config["ImageName"]
    root_password = config["RootPassword"]
    extra_package_list = config["ExtraPackage"]
    remove_package_list = config["RemovePackage"]

    generate_rootfs_release(config)
    setup_repo_file(config)

    if(os.path.exists(ROOTFS_MOUNT_POINT)):
        shutil.rmtree(ROOTFS_MOUNT_POINT)

    os.mkdir(ROOTFS_MOUNT_POINT)

    packageList = get_package_name_list(rpmlist_file,remove_package_list)

    cmd =["dnf", "install", 
                "-y", 
                "--forcearch", "aarch64", 
                "--installroot", path.join(os.getcwd() , ROOTFS_MOUNT_POINT)]

    cmd = cmd + packageList + extra_package_list

    # Install Edge Package to Rootfs
    subprocess.run(cmd).check_returncode()
   
    # Create Ext4 Image File
    cmd = ["./create_image.sh", 
                image_name,
                ROOTFS_MOUNT_POINT,
                root_password ]
    subprocess.run(cmd).check_returncode()

