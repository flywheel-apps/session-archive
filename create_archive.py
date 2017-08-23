import json
import os
import shutil

import flywheel

## SETUP
# Define variables
flywheel_basedir = os.environ['FLYWHEEL']
manifest_file = os.path.join(flywheel_basedir, 'manifest.json')
config_file = os.path.join(flywheel_basedir, 'config.json')
output_dir = os.path.join(flywheel_basedir, 'output')
container_name = '[flywheel/session-archive]'
print "%s starting..." % container_name
# Read in config file
if not os.path.exists(config_file):
    raise Exception('Config file (%s) does not exist' % config_file)
fp = open(config_file, 'r')
config_contents = json.loads(fp.read())
fp.close()
# Get apikey and session ID number from config file
api_key = str(config_contents['config']['api_key'])
session_id = str(config_contents['config']['session_id'])

## SDK
# Create client
fw = flywheel.Flywheel(api_key)

"""# Approach #1 -- get files that are attached to a session?
# Get sesssion using session_id
session = fw.get_session(session_id)
files = session.files
for f in files:
    filename = f.name
    fw.download_file_from_session(
            session_id,
            filename,
            os.path.join(tmp_dir, filename)
            )
"""

# Approach #2 -- get acquisitions within a session, then get all files within the acqs
print "Downloading files from session %s" % session_id
# Create tmpdir
dir_descript = 'session%s_archive' % session_id # TODO: suggestion for name?
tmp_dir = os.path.join('/', dir_descript)
os.mkdir(tmp_dir)
# TODO: will filenames be unique within a session?? who to ask?
acqs = fw.get_session_acquisitions(session_id)
for acq in acqs:
    for f in acq["files"]:
        filename = f["name"]
        fw.download_file_from_acquisition(
                acq["_id"], # acquisition id
                filename, # filename on flywheel instance
                os.path.join(tmp_dir, filename) # filename to be downloaded to outdir
                )

## Create Directory Structure
# TODO: Move files from tmp directory into outdir in correct structure
# need info about algorithm to get this going...
print "Creating directory structure"

## Zip up generated directory structure and move to output directory
# TODO: prefer .zip or tar.gz?
# https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
print "Creating zip archive"
shutil.make_archive(
        os.path.join(output_dir, dir_descript),
        'zip', # archive format (can also be tar, bztar, gztar)
        root_dir=tmp_dir, # root for archive - current working dir if None
        base_dir=tmp_dir  # start archiving from here - cwd if None too
        )

