
poetry:
	poetry install

buildozer-android:
	poetry run buildozer android debug deploy

buildozer-requirements:
	sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

buildozer-cleanup:
	rm -rf .buildozer
