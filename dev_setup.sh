cd ..
git clone https://github.com/colmap/colmap
git clone https://github.com/brentyi/ceres-solver

sudo apt-get install git cmake ninja-build build-essential libboost-program-options-dev \
	libboost-filesystem-dev libboost-graph-dev libboost-system-dev libeigen3-dev libflann-dev \
	libfreeimage-dev libmetis-dev libgoogle-glog-dev libgtest-dev libsqlite3-dev libglew-dev \
	qtbase5-dev libqt5opengl5-dev libcgal-dev libceres-dev

cd ceres-solver
rm -rf build
mkdir build
cd build
cmake .. -DBUILD_TESTING=OFF -DBUILD_EXAMPLES=OFF
make -j
sudo make install

pip install opencv-python tqdm

if [ ! -f "/usr/local/bin/colmap" ]; then
	cd ../../colmap
	rm -rf build
	mkdir build
	cd build
	cmake .. -DCMAKE_CUDA_ARCHITECTURES=86 -G Ninja
	ninja
	sudo ninja install
fi
