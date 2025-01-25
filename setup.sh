cd ..
git clone https://github.com/colmap/colmap

sudo apt install libunwind-dev -y

sudo apt-get install \
  git \
  cmake \
  ninja-build \
  build-essential \
  libboost-program-options-dev \
  libboost-filesystem-dev \
  libboost-graph-dev \
  libboost-system-dev \
  libeigen3-dev \
  libflann-dev \
  libfreeimage-dev \
  libmetis-dev \
  libgoogle-glog-dev \
  libgtest-dev \
  libsqlite3-dev \
  libglew-dev \
  qtbase5-dev \
  libqt5opengl5-dev \
  libcgal-dev \
  libceres-dev

sudo apt install cmake libgoogle-glog-dev libgflags-dev \
  libatlas-base-dev libeigen3-dev libsuitesparse-dev \
  libtbb2-dev

if [ ! -d "./ceres-solver-2.0.0/" ]; then
  wget http://ceres-solver.org/ceres-solver-2.0.0.tar.gz
  tar zxf ceres-solver-2.0.0.tar.gz
fi
sudo rm -r /usr/local/lib/cmake/Ceres
sudo rm -rf /usr/local/include/ceres
sudo rm /usr/local/lib/libceres*
cd ceres-solver-2.0.0
rm -rf build
mkdir build
cd build
cmake -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF ..
make -j
sudo make install

pip install opencv-python tqdm

if [ ! -f "/usr/local/bin/colmap" ]; then
  sudo rm -rf /usr/local/include/colmap
  sudo rm /usr/local/lib/libcolmap*
  cd ../../colmap
  rm -rf build
  mkdir build
  cd build
  cmake .. -DCMAKE_CUDA_ARCHITECTURES=86 -G Ninja
  ninja
  sudo ninja install
fi
