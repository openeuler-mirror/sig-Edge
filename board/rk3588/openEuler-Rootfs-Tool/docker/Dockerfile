From openeuler/openeuler:22.03

RUN sed -i "s/repo.openeuler.org/121.36.97.194/" /etc/yum.repos.d/openEuler.repo
RUN dnf update -y
RUN dnf install -y gstreamer1 gstreamer1-devel gstreamer1-plugins-base gstreamer1-plugins-good gstreamer1-plugins-bad-free

COPY libs/ /usr/lib64/
COPY include/ /usr/include/
