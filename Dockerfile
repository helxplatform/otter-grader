FROM python:3.9.15-bullseye

SHELL ["/bin/bash", "-c"]

# Install some utilities along with LaTeX and supporting libs:
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y apt-utils build-essential cmake cron imagemagick jq libfreetype6-dev \
    libnlopt-dev libpng-dev libtiff5-dev libjpeg-dev libpoppler-cpp-dev libavfilter-dev \
    libharfbuzz-dev libfribidi-dev libmagick++-dev texlive-xetex texlive-fonts-recommended \
    texlive-plain-generic libcurl4-gnutls-dev libxml2-dev libssl-dev libgit2-dev texlive-lang-chinese \
    libxft-dev pandoc unzip vim wget ca-certificates

    # Install wkhtmltopdf:
RUN wget -O /tmp/wkhtmltopdf.deb https://github.com/wkhtmltopdf/packaging/releases\/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.bullseye_amd64.deb && \
    apt-get remove -y libfontconfig1 && \
    apt-get install -y libc-bin libfontconfig1-dev /tmp/wkhtmltopdf.deb && \

    # Install otter-grader:
    pip install otter-grader ipython nbconvert pdfkit pyPDF2==2.12.1 && \
    /usr/local/bin/otter --version && \
    PATH=$PATH:/usr/local/bin && \

    # Install ottergrader tutorial:
    mkdir -p otter-tutorial && \
    curl -L https://otter-grader.readthedocs.io/en/latest/_static/tutorial.zip -o otter-tutorial/tutorial.zip && \
    cd otter-tutorial && \
    /usr/bin/unzip ./tutorial.zip

# Take care of cron scripts
COPY scripts ./scripts
RUN chmod -R 755 scripts && \
    /usr/bin/crontab -u root scripts/sync_script.cron

ENTRYPOINT service cron start && /bin/bash
