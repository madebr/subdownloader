# -*- coding: utf-8 -*-
# Copyright (c) 2017 SubDownloader Developers - See COPYING - GPLv3

import logging
import os
import re

from subdownloader import metadata
from subdownloader.FileManagement import get_extension, subtitlefile, videofile
from subdownloader.callback import ProgressCallback
from subdownloader.FileManagement import RecursiveParser

log = logging.getLogger('subdownloader.FileManagement.FileScan')


def AutoDetectNFOfile(videofolder):
    if os.path.isdir(videofolder):
        for filename in os.listdir(videofolder):
            if filename.endswith(".nfo"):
                nfo_content = open(os.path.join(videofolder, filename)).read()
                result = re.search(
                    'imdb\.\w+\/title\/tt(\d+)', nfo_content.lower())
                if result:
                    found_imdb_id = result.group(1)
                    log.debug("Found Imdb from NFO file , IMDB = %s" %
                              found_imdb_id)
                    return found_imdb_id
    return None

"""Scanning all the Video and Subtitle files inside a Folder/Recursive Folders"""
def scan_folder(folder_path, callback, recursively=True):
    log.debug('scan_folder(folder_path={folder_path}, callback=..., recursively={recursively})'.format(
        folder_path=folder_path, recursively=recursively))

    parser = RecursiveParser.RecursiveParser()

    files_found = parser.getRecursiveFileList(folder_path, videofile.VIDEOS_EXT)

    callback.set_range(0, 100)
    callback.update(0)

    videos_found = []
    # only work the video files if any were found
    if len(files_found):
        percentage = 100 / len(files_found)
        count = 0
        for i, filepath in enumerate(files_found):
            log.debug("Parsing %s ..." % filepath)
            if metadata.parse(filepath):
                videos_found.append(videofile.VideoFile(filepath))
            count += percentage

            # ,_("Parsing video: %s")% os.path.basename(filepath))
            callback.update(count)

    callback.update(0)

    # Scanning Subs
    files_found = parser.getRecursiveFileList(
        folder_path, subtitlefile.SUBTITLES_EXT)
    subs_found = []
    # only work the subtitles if any were found
    if len(files_found):
        callback.set_range(0, len(files_found))
        for i, filepath in enumerate(files_found):
            subs_found.append(
                subtitlefile.SubtitleFile(online=False, id=filepath))
            callback.update(i)  # ,_("Parsing sub: %s") % filepath)
    callback.finish()

    return videos_found, subs_found


def ScanSubtitlesFolder(folderpath, callback, recursively=True):

    # Let's reset the progress bar to 0%
    callback.update(0)
    # Scanning Subs
    parser = RecursiveParser.RecursiveParser()
    if recursively:
        files_found = parser.getRecursiveFileList(
            folderpath, subtitlefile.SUBTITLES_EXT)
    else:
        files_found = []
        for filename in os.listdir(folderpath):
            if os.path.isfile(os.path.join(folderpath, filename)) and get_extension(filename).lower() in subtitlefile.SUBTITLES_EXT:
                files_found.append(os.path.join(folderpath, filename))

    callback.set_range(0, len(files_found))
    subs_found = []
    # only work the subtitles if any were found
    if len(files_found):
        percentage = 100 / len(files_found)
        count = 0
        for i, filepath in enumerate(files_found):
            subs_found.append(
                subtitlefile.SubtitleFile(online=False, id=filepath))
            callback.update(i) #, _("Parsing sub: %s") % os.path.basename(filepath))
    callback.finish() #_("Finished hashing"))

    return subs_found
