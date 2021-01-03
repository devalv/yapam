#!/usr/bin/sh

PACKAGE_PREFIX="yapam"
PACKAGE_EXTENSION=".deb"

BUILD_DIR="yapamb"
DEBIAN_BUILD_DIR=${BUILD_DIR}"/DEBIAN"
DAV_UTILS_ARCH_NAME="master.zip"
DAV_UTILS_URL="https://github.com/devalv/utils/archive/${DAV_UTILS_ARCH_NAME}"
DAV_UTILS_EXTRACT_DIR="utils-master"
DAV_UTILS_DIR="dav_utils"

usage() {
  cat <<-EOF
  Example: ./make_binary -v 013
  Usage: make_binary [options]
  Options:
    -v,          specify binary version
    -h,          print this message
EOF
exit
}

build() {
    echo "Building package ${package_name}..."
    rm -rf ${BUILD_DIR} ${DAV_UTILS_EXTRACT_DIR} build/ dist/ ${DAV_UTILS_ARCH_NAME} && mkdir -p ${DEBIAN_BUILD_DIR}
    wget ${DAV_UTILS_URL} && unzip ${DAV_UTILS_ARCH_NAME}
    pyinstaller app.py -n ${PACKAGE_PREFIX} --add-data ${PACKAGE_PREFIX}:${PACKAGE_PREFIX} --add-data ${DAV_UTILS_EXTRACT_DIR}/${DAV_UTILS_DIR}:dav_utils -F
    mkdir -p ${BUILD_DIR}/usr/bin && cp -r dist/* ${BUILD_DIR}/usr/bin && cp control ${DEBIAN_BUILD_DIR}/
    dpkg-deb -b ${BUILD_DIR} ${package_name}
    echo "Removing garbage..."
    rm -rf ${BUILD_DIR} ${DAV_UTILS_EXTRACT_DIR} build/ dist/ ${DAV_UTILS_ARCH_NAME}
    echo "Done."
}

run() {
  package_name="${PACKAGE_PREFIX}-${version}${PACKAGE_EXTENSION}"
  build ${package_name}
  exit
}

while getopts ":hv:" option; do
   case ${option} in
      h) # display usage
         usage;;
      \?) # incorrect option
         echo "Error: Invalid option"
         usage;;
      v) # specify version for build
      version=$2; shift
        run ${version}
   esac
done

usage
