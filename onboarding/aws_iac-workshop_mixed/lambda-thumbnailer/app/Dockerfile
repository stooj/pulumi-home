FROM amazon/aws-lambda-nodejs:12
ARG FUNCTION_DIR="/var/task"

# Install tar and xz
RUN yum install tar xz unzip -y

# Install awscli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" -s
RUN unzip -q awscliv2.zip
RUN ./aws/install

# Install ffmpeg
RUN curl https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -o ffmpeg.tar.xz -s
RUN tar -xf ffmpeg.tar.xz
RUN mv ffmpeg-*-amd64-static/ffmpeg /usr/bin

# Create function directory
RUN mkdir -p ${FUNCTION_DIR}

# Copy handler function and package.json
COPY index.js ${FUNCTION_DIR}

# Set the CMD to your handler (couyld also be done as a parameter opverride
# outside of the Dockerfile)
CMD [ "index.handler" ]
