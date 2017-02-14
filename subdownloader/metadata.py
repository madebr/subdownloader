# Copyright (c) 2017 SubDownloader Developers - See COPYING - GPLv3

import logging

log = logging.getLogger('subdownloader.modules.metadata')


class MetadataVideoTrack(object):
    """
    Instances of this class collect some metadata of a video track.
    Only metadata is stored. It is meant to be attached to an actual video.
    """
    def __init__(self, duration_ms, framerate):
        """
        Create a new MetadataVideoTrack instance.
        :param duration_ms: Duration of the video track (in milliseconds)
        :param framerate: Frame rate of the video track (in frames per second)
        """
        self.duration_ms = duration_ms
        self.framerate = framerate

# FIXME: add libmediainfodll?
# FIXME: add ffprobe? ffprobe -v quiet -print_format json -show_format -show_streams ${VIDEO}


class Metadata(object):
    """
    Instances of this class collect metadata of all the video tracks.
    """
    def __init__(self):
        """
        Create a mew Metadata instance.
        """
        self._videos = []

    def _add_metadata(self, metadata):
        """
        Private method to add a new MetadataVideoTrack instance
        :param metadata: metadata of a video track
        """
        self._videos.append(metadata)

    def nb_videotracks(self):
        """
        Return number of video tracks
        :return: number of video tracks as integer
        """
        return len(self._videos)

    def get_metadata(self):
        """
        Get metadata of all tracks
        :return: metadata of all tracks as a list
        """
        return self._videos

    def _parse_dummy(self, filepath):
        """
        Private function to pretend to parse video at filepath, but don't do anything actually.
        :param filepath: path of video to parse as string
        """
        pass

    def _parse_kaa_metadata(self, filepath):
        """
        Private function to parse video at filepath, using kaa framework.
        :param filepath: path of video to parse as string
        """
        parseRes = kaa.metadata.parse(filepath)
        if not parseRes:
            return
        for video in parseRes.video:
            self._add_metadata(
                MetadataVideoTrack(
                    duration_ms=1000 * parseRes.length,
                    framerate=video.fps
                )
            )

    def _parse_pymediainfo(self, filepath):
        """
        Private function to parse video at filepath, using pymediainfo framework.
        :param filepath: path of video to parse as string
        """
        parseRes = pymediainfo.MediaInfo.parse(filepath)
        for track in parseRes.tracks:
            if track.track_type == 'Video':
                self._add_metadata(
                    MetadataVideoTrack(
                        duration_ms=track.duration,
                        framerate=float(track.frame_rate)
                    )
                )

try:
    import kaa.metadata
    log.debug('Using kaa.metadata')
    # Not interested in any output of the metadata package
    logging.getLogger('metadata').setLevel(logging.CRITICAL)
    Metadata.parse = Metadata._parse_kaa_metadata
except ImportError:
    try:
        import pymediainfo
        log.debug('Using pymediainfo')
        Metadata.parse = Metadata._parse_pymediainfo
    except ImportError:
        Metadata.parse = Metadata._parse_dummy
        log.warning('Failed to import metadata module.')
        log.warning('This means you will be unable to automatically')
        log.warning('download or upload your subtitles with all details.')


def parse(filepath):
    """
    Parse video at filepath
    :param filepath: path of video to parse as string
    :return: Metadata Instance of the video
    """
    metadata = Metadata()
    metadata.parse(filepath)
    return metadata
