# coding=utf-8
# Claus Hunsen, 2016
# hunsen@fim.uni-passau.de

import itertools
import logging
import os
import socket
import sys
import tempfile

from plumbum import local

# configure logging
logging.basicConfig(level=logging.INFO)


#
# HELPER FUNCTIONS
#

def get_container_path(mount, file=""):
    """Transforms path to a path inside the uchroot container."""
    absdir = os.path.abspath(str(mount))
    dirname = os.path.split(absdir)[-1]
    container_path = os.path.join("/mnt", dirname, file)
    return container_path

def get_configuration_name(conf, chunk = ""):
    conf = (chunk, ) + conf
    return "_".join(conf)


#
# PATHS
#

# basic information
DIR = os.path.dirname(os.path.realpath(__file__))
HOST = socket.gethostname()
PATH_ROOT = "/scratch/codeface"

# Codeface
PATH_ANALYSIS = os.path.join(PATH_ROOT, "codeface")
PATH_ANALYSIS_SCRIPT = "run.sh" # "run_test.sh"

# Codeface extraction
PATH_CODEFACE_EXTRACTION = os.path.join(PATH_ROOT, "codeface-extraction")
PATH_GITHUBWRAPPER =  os.path.join(PATH_ROOT, "GitHubWrapper")

# benchbuild + uchroot container
PATH_BENCHBUILD = os.path.join(PATH_ROOT, "benchbuild")
PATH_CONTAINER = os.path.join(PATH_ROOT, "container")
#PATH_CONTAINER_CODEFACE = os.path.join(PATH_CONTAINER, "2016-11-03_codeface.tar.bz2")
PATH_CONTAINER_CODEFACE = os.path.join(PATH_CONTAINER, "2018-03-02_codeface.tar.bz2")
# PATH_CONTAINER_UBUNTU = os.path.join(PATH_BENCHBUILD, "results", "codeface.oNm0L7r9", "container-in")


#
# SLURM
#

# node
CH_SLURM_ENV = ["-p", "anywhere", "-A", "anywhere", "--exclusive", "--mem=0", "--qos=verylong", "--time=0", "--constraint=zeus"]
#CH_SLURM_ENV = ["-p", "sphinx", "-A", "sphinx", "--exclusive"]

# notification email
USER = "hunsen" # "bockthom" "hunsen"
CH_MAIL = "{}@fim.uni-passau.de".format(USER)

# job parameters
CH_SLURM_JOB_NAME = "codeface"
CH_SLURM_PARAMS = ["-J", CH_SLURM_JOB_NAME, "--get-user-env"]
CH_SBATCH = os.path.join(PATH_ANALYSIS, "run-container-wrapper.sh")

# set job dependency to singleton (last of user's jobs)
CH_SLURM_DEPENDENCY = ["--dependency", "singleton"]  # run after all jobs of user
CH_SLURM_MAIL = ["--mail-type=END", "--mail-user=" + CH_MAIL]


#
#  ANALYSIS CONFIGURATIONS
#

# list of casestudies
CASESTUDIES = [
#    "busybox",
#    "openssl",
#    "sqlite",
#    "firefox",
#    "test",
#    "testmail",
#    "libressl",
#    "jailhouse",
#    "apache-http",
#    "git",
    "chromium",
#    "django",
#    "ffmpeg",
#    "gcc",
#    "linux",
#    "llvm",
#    "postgres",
#    "qemu",
#    "uboot",
#    "wine",
]

TAGGING = [
    "proximity",
    "feature"
]

# selection process (one or more of: releases, threemonth, testing)
SELECTION_PROCESS = "threemonth"

# construct all configurations
configurations = [element for element in itertools.product(CASESTUDIES, TAGGING)]
#configurations = [configurations[0]]


#
# ANALYSIS PATHS
#

## global paths
CODEFACE_DATA = "/scratch/codeface/codeface-data"
CODEFACE_DATA_CONTAINER = get_container_path(CODEFACE_DATA)

## container paths
CODEFACE_DATA_CONF = os.path.join(CODEFACE_DATA_CONTAINER, "configurations")
CODEFACE_DATA_CONF_CHUNK = os.path.join(CODEFACE_DATA_CONTAINER, "configurations", SELECTION_PROCESS)
CODEFACE_DATA_ML = os.path.join(CODEFACE_DATA_CONTAINER, "mailinglists", SELECTION_PROCESS)
CODEFACE_DATA_REPOS = os.path.join(CODEFACE_DATA_CONTAINER, "repos")
CODEFACE_DATA_RESULTS = os.path.join(CODEFACE_DATA_CONTAINER, "results", SELECTION_PROCESS)

## logs
CODEFACE_DATA_LOGS = os.path.join(CODEFACE_DATA, "logs", SELECTION_PROCESS) # slurm log
CODEFACE_DATA_LOGS_CONTAINER = os.path.join(CODEFACE_DATA_CONTAINER, "logs", SELECTION_PROCESS) # within container


#
# COMMAND
#

# run the command for each configuration
for configuration in configurations:

    CASESTUDY = configuration[0]

    # construct case-study-dependent parameters
    CONF_CODEFACE = os.path.join(CODEFACE_DATA_CONF, "codeface_{}_dvorak.conf".format(SELECTION_PROCESS))
    CONF_CASESTUDY = os.path.join(CODEFACE_DATA_CONF_CHUNK, "{}_{}.conf".format(configuration[0], configuration[1]))
    LOG_FILE_SLURM = os.path.join(CODEFACE_DATA_LOGS, get_configuration_name(configuration, chunk = SELECTION_PROCESS) + ".log")
    LOG_PATH_CODEFACE = os.path.join(CODEFACE_DATA_LOGS_CONTAINER, get_configuration_name(configuration, chunk = SELECTION_PROCESS))

    # construct configuration-dependent parameters
    TMP_FOLDER = tempfile.TemporaryDirectory(prefix = "codeface_container_", dir = "/local/codeface").name

    # sbatch wrapper
    sbatch = local["sbatch"][
        CH_SLURM_ENV,
        CH_SLURM_PARAMS,
        # CH_SLURM_DEPENDENCY,
        CH_SLURM_MAIL,
        "-o", LOG_FILE_SLURM,
        CH_SBATCH
    ]

    # container command
    cmd = sbatch["container",
                 # "--help",
                 "-i", "{}".format(PATH_CONTAINER_CODEFACE),
                 "-m", "{}".format(PATH_ANALYSIS), # FIXME sync this to cluster:/local/codeface/{tmp}/
                 "-m", "{}".format(PATH_CODEFACE_EXTRACTION),
                 "-m", "{}".format(CODEFACE_DATA), # FIXME write on cluster first, then sync result files
                 "-m", "{}".format(PATH_GITHUBWRAPPER),
                 "-t", TMP_FOLDER,
                 "run",
                 "--",
                 "/bin/bash",
                 get_container_path(PATH_ANALYSIS, PATH_ANALYSIS_SCRIPT),
                 TMP_FOLDER,
                 CASESTUDY,
                 CONF_CODEFACE,
                 CONF_CASESTUDY,
                 CODEFACE_DATA_REPOS,
                 CODEFACE_DATA_ML,
                 CODEFACE_DATA_RESULTS,
                 LOG_PATH_CODEFACE
    ]

    # call the command
    with local.cwd(PATH_BENCHBUILD):
        logging.info("Scheduling {} task".format(CH_SLURM_JOB_NAME))
        logging.info("-- configuration: {}".format(get_configuration_name(configuration, SELECTION_PROCESS)))
        logging.info("-- command: {}".format(cmd))
        #cmd()  # (cmd > CH_SLURM_OUTPUT)()
        print(''.join(x for x in cmd() if x.isdigit()))