cd ..
git clone https://github.com/colmap/colmap

sudo apt-get install git cmake ninja-build build-essential libboost-program-options-dev \
	libboost-filesystem-dev libboost-graph-dev libboost-system-dev libeigen3-dev libflann-dev \
	libfreeimage-dev libmetis-dev libgoogle-glog-dev libgtest-dev libsqlite3-dev libglew-dev \
	qtbase5-dev libqt5opengl5-dev libcgal-dev libceres-dev

if [! -d "/usr/local/bin/colmap"]; then
	cd colmap
	rm -rf build
	mkdir build
	cd build
	cmake .. -DCMAKE_CUDA_ARCHITECTURES=86 -G Ninja
	ninja
	sudo ninja install
fi
