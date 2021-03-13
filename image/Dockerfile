FROM	alpine:latest
LABEL	maintainers="github.com/kajdev; github.com/nytelife26" \
	vendor="KAJdev & KCS Ltd." \
	description="A custom Alpine build for usage on Dockord."
RUN	echo -e "Initializing packages"; \
	apk add binutils findutils curl grep sed
WORKDIR	/home/sandbox
RUN	echo -e "Creating sandbox user"; \
	adduser -h /home/sandbox -s /bin/sh -D sandbox
ENV	HOME="/home/sandbox"
ENV	PATH="$PATH:$HOME:$HOME/.config/bin"
COPY	homeinstance/* .
CMD	["/bin/sh", "-c", "su - sandbox"]
