#!/bin/bash

# Predefined array of tags
declare -a ALL_TAGS=("default" "classic" "flat" "void")  # Add or remove tags as needed

# Flags
BUILD=false
RUN=false
ALL=false
DEBUG=false
MOUNT=false
WSL=false
TAG=""

# Usage message
usage() {
  echo "Usage: $0 [--build] [--run] [--all] [--debug] [--mount] [--wsl] [tag_name]"
  echo "Options:"
  echo "  --build   Build the Docker image for the given tag."
  echo "  --run     Run the Docker image for the given tag."
  echo "  --all     Act on all tags. Use with --build or --run."
  echo "  --debug   Pass a debug flag to the docker build."
  echo "  --mount   Mount /data directory inside image to /tmp/(image+tag) on host."
  echo "  --wsl     Use '--network host' option for Docker run (for WSL compatibility)."
  echo "  tag_name  Specific tag to build/run (e.g., classic)."
  echo "            If omitted and --all isn't used, this defaults to 'classic'."
}

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case "$1" in
    --entrypoint)
      ENTRYPOINT=true
      source /tmp/set_env.sh

      # Execute the original command
      /start

      exit 0  # Exit after running entrypoint logic
      ;;
    --build)
      BUILD=true
      shift
      ;;
    --run)
      RUN=true
      shift
      ;;
    --all)
      ALL=true
      shift
      ;;
    --debug)
      DEBUG=true
      shift
      ;;
    --mount)
      MOUNT=true
      shift
      ;;
    --wsl)
      WSL=true
      shift
      ;;
    -*)
      echo "Unknown option: $1"
      usage
      exit 1
      ;;
    *)
      TAG="$1"
      shift
      ;;
  esac
done

# Default behavior is to build and run
if ! $BUILD && ! $RUN; then
  BUILD=true
  RUN=true
fi

# Default tag is 'default'
if [ -z "$TAG" ] && ! $ALL; then
  TAG="default"
fi

# Build logic
if $BUILD; then
  if $ALL; then
    for t in "${ALL_TAGS[@]}"; do
      echo "Building image with tag: $t"
      if $DEBUG; then
        docker build --build-arg IMG_TAG="$t" --build-arg DEBUG=true -t ghcr.io/portalhubyt/template_server:"$t" .
      else
        docker build --build-arg IMG_TAG="$t" -t ghcr.io/portalhubyt/template_server:"$t" .
      fi
    done
  else
    echo "Building image with tag: $TAG"
    if $DEBUG; then
      docker build --build-arg IMG_TAG="$TAG" --build-arg DEBUG=true -t ghcr.io/portalhubyt/template_server:"$TAG" .
    else
      docker build --build-arg IMG_TAG="$TAG" -t ghcr.io/portalhubyt/template_server:"$TAG" .
    fi
  fi
fi

# Run logic
if $RUN; then
  NETWORK_FLAG=""
  if $WSL; then
    NETWORK_FLAG="--network host"
  fi

  # If --all is not used, just use the single specified TAG in our loop
  TARGET_TAGS=("${TAG}")
  if $ALL; then
    TARGET_TAGS=("${ALL_TAGS[@]}")
  fi

  for t in "${TARGET_TAGS[@]}"; do
    echo "Running container from image with tag: $t"
    
    # Set the mount path and volume flag based on the --mount flag
    VOLUME_FLAG=""
    if $MOUNT; then
      MOUNT_PATH="./server_data/$t"
      
      # Check if the folder exists; if not, create it
      if [ ! -d "$MOUNT_PATH" ]; then
        mkdir -p "$MOUNT_PATH"
      fi
      
      VOLUME_FLAG="-v $MOUNT_PATH:/data"
    fi
    
    docker run -it -p 25565:25565 $NETWORK_FLAG $VOLUME_FLAG ghcr.io/portalhubyt/template_server:"$t"
  done
fi


exit 0
