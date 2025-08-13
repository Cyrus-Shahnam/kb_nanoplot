FROM kbase/sdkpython:3.8.0

LABEL maintainer="ac.shahnam"

# Install system dependencies for Kaleido and plotting
RUN apt update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

    # libglib2.0-0 \
    # libgdk-pixbuf2.0-0 \
    # libxss1 \
    # libx11-xcb1 \
    # libatk1.0-0 \
    # libgtk-3-0 \
    # libgl1-mesa-glx \
    # fonts-liberation \
    # && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install NanoPlot and plotting Python dependencies
RUN pip install --upgrade pip && \
    pip install \
        "kaleido>=0.2.1" \
        plotly \
        matplotlib \
        seaborn \
        NanoPlot==1.46.0

# KBase SDK standard setup
COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module
RUN make all

ENTRYPOINT ["./scripts/entrypoint.sh"]
CMD []
