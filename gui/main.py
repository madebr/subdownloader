#!/usr/bin/env python
# -*- coding: utf-8 -*-

##    Copyright (C) 2007 Ivan Garcia contact@ivangarcia.org
##    This program is free software; you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation; either version 2 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License along
##    with this program; if not, write to the Free Software Foundation, Inc.,
##    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.Warning

""" Create and launch the GUI """
import sys, re, os, traceback, tempfile
import webbrowser
import base64, zlib
#sys.path.append(os.path.dirname(os.path.dirname(os.getcwd())))

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, SIGNAL, QObject, QCoreApplication, \
                         QSettings, QVariant, QSize, QEventLoop, QString, \
                         QBuffer, QIODevice, QModelIndex,QDir, QFileInfo
from PyQt4.QtGui import QPixmap, QErrorMessage, QLineEdit, \
                        QMessageBox, QFileDialog, QIcon, QDialog, QInputDialog,QDirModel, QItemSelectionModel
from PyQt4.Qt import qDebug, qFatal, qWarning, qCritical

from subdownloader.gui.SplashScreen import SplashScreen, NoneSplashScreen

from subdownloader import * 
from subdownloader.OSDBServer import OSDBServer
from subdownloader.gui import installErrorHandler, Error, _Warning, extension


from subdownloader.gui.uploadlistview import UploadListModel, UploadListView
from subdownloader.gui.videotreeview import VideoTreeModel

from subdownloader.gui.main_ui import Ui_MainWindow
from subdownloader.gui.imdbSearch import imdbSearchDialog
from subdownloader.FileManagement import FileScan, Subtitle
from subdownloader.videofile import  *
from subdownloader.subtitlefile import *


import subdownloader.languages.Languages as languages

import logging
log = logging.getLogger("subdownloader.gui.main")

class Main(QObject, Ui_MainWindow): 
    def report_error(func):
        """ 
        Decorator to ensure that unhandled exceptions are displayed 
        to users via the GUI
        """
        def function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception, e:
                Error("There was an error calling " + func.__name__, e)
                raise
        return function
        
    def read_settings(self):
        settings = QSettings()
        self.window.resize(settings.value("mainwindow/size", QVariant(QSize(1000, 700))).toSize())
    
    def write_settings(self):
        settings = QSettings()
        settings.setValue("mainwindow/size", QVariant(self.window.size()))
    
    def close_event(self, e):
        self.write_settings()
        e.accept()
    
    def __init__(self, window, log_packets, options):
        QObject.__init__(self)
        Ui_MainWindow.__init__(self)
        
        self.key = '-1'
        self.log_packets = log_packets
        self.options = options
        self.setupUi(window)
        self.card = None
        self.uploadIMDB_list = []
        self.window = window
        window.closeEvent = self.close_event
        window.setWindowTitle(QtGui.QApplication.translate("MainWindow", "SubDownloader "+APP_VERSION, None, QtGui.QApplication.UnicodeUTF8))
        self.read_settings()
        
        #self.treeView.reset()
        window.show()
        self.splitter.setSizes([400, 1000])

        #SETTING UP FOLDERVIEW
        model = QDirModel(window)        
        model.setFilter(QDir.AllDirs|QDir.NoDotAndDotDot)
        self.folderView.setModel(model)
        
        settings = QSettings()
        path = settings.value("mainwindow/workingDirectory", QVariant(QDir.rootPath()))
        self.folderView.setRootIndex(model.index(QDir.rootPath()))
        #index = model.index(QDir.rootPath())

        self.folderView.header().hide()
        self.folderView.hideColumn(3)
        self.folderView.hideColumn(2)
        self.folderView.hideColumn(1)
        self.folderView.show()
        
        #Loop to expand the current directory in the folderview.
        log.debug('Current directory: %s' % path.toString())
        path = QDir(path.toString())
        while True:
            self.folderView.expand(model.index(path.absolutePath()))
            if not path.cdUp(): break
                    
        QObject.connect(self.folderView, SIGNAL("activated(QModelIndex)"), \
                            self.onFolderTreeClicked)
        QObject.connect(self.folderView, SIGNAL("clicked(QModelIndex)"), \
                            self.onFolderTreeClicked)

        #SETTING UP SEARCH_VIDEO_VIEW
        self.videoModel = VideoTreeModel(window)
        self.videoView.setModel(self.videoModel)
        QObject.connect(self.videoView, SIGNAL("activated(QModelIndex)"), self.onClickVideoTreeView)
        QObject.connect(self.videoView, SIGNAL("clicked(QModelIndex)"), self.onClickVideoTreeView)
        QObject.connect(self.videoModel, SIGNAL("dataChanged(QModelIndex,QModelIndex)"), self.subtitlesCheckedChanged)
        
        QObject.connect(self.buttonDownload, SIGNAL("clicked(bool)"), self.onButtonDownload)
        QObject.connect(self.buttonIMDB, SIGNAL("clicked(bool)"), self.onButtonIMDB)
        
        #SETTING UP UPLOAD_VIEW
        self.uploadModel = UploadListModel(window)
        self.uploadView.setModel(self.uploadModel)
        self.uploadModel._main = self #FIXME: This connection should be cleaner.

        #Resizing the headers to take all the space(50/50) in the TableView
        header = self.uploadView.horizontalHeader()
        header.setResizeMode(QtGui.QHeaderView.Stretch)
        
        QObject.connect(self.buttonUploadBrowseFolder, SIGNAL("clicked(bool)"), self.onUploadBrowseFolder)
        QObject.connect(self.uploadView, SIGNAL("activated(QModelIndex)"), self.onClickUploadViewCell)
        QObject.connect(self.uploadView, SIGNAL("clicked(QModelIndex)"), self.onClickUploadViewCell)
        
        QObject.connect(self.buttonUpload, SIGNAL("clicked(bool)"), self.onUploadButton)
        QObject.connect(self.buttonUploadUpRow, SIGNAL("clicked(bool)"), self.uploadModel.onUploadButtonUpRow)
        QObject.connect(self.buttonUploadDownRow, SIGNAL("clicked(bool)"), self.uploadModel.onUploadButtonDownRow)
        QObject.connect(self.buttonUploadPlusRow, SIGNAL("clicked(bool)"), self.uploadModel.onUploadButtonPlusRow)
        QObject.connect(self.buttonUploadMinusRow, SIGNAL("clicked(bool)"), self.uploadModel.onUploadButtonMinusRow)
        
        QObject.connect(self.buttonUploadFindIMDB, SIGNAL("clicked(bool)"), self.onButtonUploadFindIMDB)
        
        self.uploadSelectionModel = QItemSelectionModel(self.uploadModel)
        self.uploadView.setSelectionModel(self.uploadSelectionModel)
        QObject.connect(self.uploadSelectionModel, SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.onUploadChangeSelection)
        QObject.connect(self, SIGNAL("imdbDetected(QString,QString)"), self.onUploadIMDBNewSelection)
            
        
        
        #Fill Out the Filters Language SelectBoxes
        self.InitializeFilterLanguages()
        
        self.status_progress = QtGui.QProgressBar(self.statusbar)
        self.status_progress.setProperty("value",QVariant(0))
        
        self.status_progress.setOrientation(QtCore.Qt.Horizontal)
        self.status_label = QtGui.QLabel("v"+ APP_VERSION,self.statusbar)
        
        self.statusbar.insertWidget(0,self.status_label)
        self.statusbar.addPermanentWidget(self.status_progress,2)
        if not options.test:
            self.establish_connection()
            if self.OSDBServer.is_connected():
                data = self.OSDBServer.ServerInfo()
                self.status_label.setText("Users online: "+ str(data["users_online_program"]))
        QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        
        #FOR TESTING
        if options.test:
            #self.SearchVideos('/media/xp/pelis/')
            self.tabs.setCurrentIndex(2)
            pass

    def InitializeFilterLanguages(self):
        self.filterLanguageForVideo.addItem(QtGui.QApplication.translate("MainWindow", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.filterLanguageForTitle.addItem(QtGui.QApplication.translate("MainWindow", "All", None, QtGui.QApplication.UnicodeUTF8))
        for lang in languages.LANGUAGES:
            self.filterLanguageForVideo.addItem(QtGui.QApplication.translate("MainWindow", lang["LanguageName"], None, QtGui.QApplication.UnicodeUTF8), QVariant(lang["SubLanguageID"]))
            self.filterLanguageForTitle.addItem(QtGui.QApplication.translate("MainWindow", lang["LanguageName"], None, QtGui.QApplication.UnicodeUTF8), QVariant(lang["SubLanguageID"]))
            self.uploadLanguages.addItem(QtGui.QApplication.translate("MainWindow", lang["LanguageName"], None, QtGui.QApplication.UnicodeUTF8), QVariant(lang["SubLanguageID"]))
            
        self.filterLanguageForVideo.adjustSize()
        self.filterLanguageForTitle.adjustSize()
        self.uploadLanguages.adjustSize()
        QObject.connect(self.filterLanguageForVideo, SIGNAL("currentIndexChanged(int)"), self.onFilterLanguageVideo)
        QObject.connect(self.uploadLanguages, SIGNAL("language_updated(QString)"), self.onUploadLanguageDetection)
    
    def onFilterLanguageVideo(self, index):
        selectedLanguageName = self.filterLanguageForVideo.itemText(index)
        log.debug("Filtering subtitles by language : %s" % selectedLanguageName)
        self.videoModel.clearTree()
        self.videoView.expandAll()
        if selectedLanguageName != "All": #FIXME: Instead of using english words, we should use lang_codes
            selectedLanguageXX = languages.name2xx(selectedLanguageName)
            self.videoModel.setLanguageFilter(selectedLanguageXX)
        else:
            self.videoModel.setLanguageFilter(None)
        
        self.videoView.expandAll()
        
    def subtitlesCheckedChanged(self):
       subs = self.videoModel.getCheckedSubtitles()
       if subs:
           self.buttonDownload.setEnabled(True)
           self.buttonPlay.setEnabled(True)
       else:
           self.buttonDownload.setEnabled(False)
           self.buttonPlay.setEnabled(False)
           
    def videoSelectedChanged(self):
       subs = self.videoModel.getSelected()
       if subs:
           self.buttonIMDB.setEnabled(True)
       else:
           self.buttonDownload.setEnabled(False)
    
    def SearchVideos(self, path):
        #Scan recursively the selected directory finding subtitles and videos
        videos_found,subs_found = FileScan.ScanFolder(path,recursively = True,report_progress = self.progress)

        #Populating the items in the VideoListView
        self.videoModel.clearTree()
        self.videoView.expandAll()
        self.videoModel.setVideos(videos_found)
        self.videoView.setModel(self.videoModel)
        
        self.videoView.expandAll() #This was a solution found to refresh the treeView
        #Searching our videohashes in the OSDB database
        QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        if(videos_found):
            self.status("Asking Database...")
            #This effect causes the progress bar turn all sides
            #FIXME: We need to send a refresh signal.
            self.status_progress.setMinimum(0)
            self.status_progress.setMaximum(0)
            
            self.window.setCursor(Qt.WaitCursor)
            videoSearchResults = self.OSDBServer.SearchSubtitles("",videos_found)
            if(videoSearchResults):
                self.videoModel.clearTree()
                self.videoModel.setVideos(videoSearchResults)
                self.videoView.expandAll() #This was a solution found to refresh the treeView
            elif videoSearchResults == None :
                QMessageBox.about(self.window,"Error","Server is not responding. Please try again later")
            self.progress(100)
            self.status_progress.setFormat("Search finished")
        else:
            self.progress(100)
            self.status_progress.setFormat("No videos founded")
    
        self.window.setCursor(Qt.ArrowCursor)
        #TODO: check if the subtitle found is already in our folder.
        #self.OSDBServer.CheckSubHash(sub_hashes) 
        
    def onClickVideoTreeView(self, index):
        treeItem = self.videoModel.getSelectedItem(index)
        if type(treeItem.data) == VideoFile:
            video = treeItem.data
            if video.getMovieInfo():
                self.buttonIMDB.setEnabled(True)
        else:
            treeItem.checked = not(treeItem.checked)
            self.videoModel.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"),index, index)
            self.buttonIMDB.setEnabled(False)
        
    """What to do when a Folder in the tree is clicked"""
    def onFolderTreeClicked(self, index):
        if index.isValid():
            settings = QSettings()
            data = self.folderView.model().filePath(index)
            folder_path = unicode(data, 'utf-8')
            settings.setValue("mainwindow/workingDirectory", QVariant(folder_path))
            self.SearchVideos(folder_path)

    def onButtonIMDB(self, checked):
        video = self.videoModel.getSelectedItem().data
        movie_info = video.getMovieInfo()
        if movie_info:
            #QMessageBox.about(self.window,"WWW","Open website: http://www.imdb.com/title/tt%s" % movie_info["IDMovieImdb"])
            webbrowser.open( "http://www.imdb.com/title/tt%s"% movie_info["IDMovieImdb"], new=2, autoraise=1)
            
    def onButtonDownload(self, checked):
        #We download the subtitle in the same folder than the video
            subs = self.videoModel.getCheckedSubtitles()
            percentage = 100/len(subs)
            count = 0
            self.status("Connecting to download...")
            for sub in subs:
                self.progress(count,"Downloading subtitle... "+sub.getIdOnline())
                count += percentage
                destinationPath = os.path.join(sub.getVideo().getFolderPath(),sub.getFileName())
                log.debug("Downloading subtitle '%s'" % destinationPath)
                try:
                    videos_result = self.OSDBServer.DownloadSubtitles({sub.getIdOnline():destinationPath})
                except Exception, e: 
                    QMessageBox.about(self.window,"Error","Unable to download subtitle "+sub.getIdOnline())
                    traceback.print_exc(e)

            self.status("Subtitles downloaded succesfully.")
            self.progress(100)

    """Control the STATUS BAR PROGRESS"""
    def progress(self, val,msg = None):
        self.status_progress.setMaximum(100)
        self.status_progress.reset()
        if msg != None:
            self.status_progress.setFormat(msg + ": %p%")
        if val < 0:
            self.status_progress.setMaximum(0)
        else: 
            self.status_progress.setValue(val)
        QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
    
    def status(self, msg):
        self.status_progress.setMaximum(100)
        self.status_progress.reset()
        self.status_progress.setFormat(msg + ": %p%")
        self.progress(0)
        QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
    
    def establish_connection(self):
        self.window.setCursor(Qt.WaitCursor)
        self.status("Connecting to server") 
        try:
            self.OSDBServer = OSDBServer(self.options)
        except Exception, e: 
            traceback.print_exc(e)
            qFatal("Unable to connect to server. Please try later")
        self.progress(100)
        self.status_progress.setFormat("Connected")
        self.window.setCursor(Qt.ArrowCursor)
        
    #UPLOAD METHODS
    
    def onButtonUploadFindIMDB(self):
        dialog = imdbSearchDialog(self)
        dialog.show()
        ok = dialog.exec_()
        QCoreApplication.processEvents(QEventLoop.ExcludeUserInputEvents)
        
    def onUploadBrowseFolder(self):
        settings = QSettings()
        path = settings.value("mainwindow/workingDirectory", QVariant())
        directory=QtGui.QFileDialog.getExistingDirectory(None,"Select a directory",path.toString())
        if directory:
            settings.setValue("mainwindow/workingDirectory", QVariant(directory))
            directory =  str(directory.toUtf8())
            videos_found,subs_found = FileScan.ScanFolder(directory,recursively = False,report_progress = self.progress)
            log.info("Videos found: %i Subtitles found: %i"%(len(videos_found), len(subs_found)))
            self.uploadModel.emit(SIGNAL("layoutAboutToBeChanged()"))
            for row, video in enumerate(videos_found):
                self.uploadModel.addVideos(row, [ video])
                subtitle = Subtitle.AutoDetectSubtitle(video.getFilePath())
                if subtitle:
                    sub = SubtitleFile(False,subtitle) 
                    self.uploadModel.addSubs(row, [sub])
            self.uploadView.resizeRowsToContents()
            self.uploadModel.update_lang_upload()
            self.uploadModel.emit(SIGNAL("layoutChanged()"))

    def onUploadButton(self, clicked):
        result = self.uploadModel.verify()
        if not result["ok"]:
            QMessageBox.about(self.window,"Error",result["error_msg"])
            return
        else:
            log.debug("Compressing subtitle...")
            details = {}
            imdb_id = self.uploadIMDB.itemData(self.uploadIMDB.currentIndex())
            if imdb_id == QVariant(): #No IMDB
                QMessageBox.about(self.window,"Error","Please select an IMDB movie.")
                return
            else:
                details['IDMovieImdb'] = str(imdb_id.toString().toUtf8())
                lang_xxx = self.uploadLanguages.itemData(self.uploadLanguages.currentIndex())
                details['sublanguageid'] = str(lang_xxx.toString().toUtf8()) 
                details['movieaka'] = ''
                details['moviereleasename'] = str(self.uploadReleaseText.text().toUtf8()) 
                details['subauthorcomment'] = str(self.uploadComments.toPlainText().toUtf8()) 
                
                movie_info = {}
                movie_info['baseinfo'] = {'idmovieimdb': details['IDMovieImdb'], 'moviereleasename': details['moviereleasename'], 'movieaka': details['movieaka'], 'sublanguageid': details['sublanguageid'], 'subauthorcomment': details['subauthorcomment']}
             
                for i in range(self.uploadModel.getTotalRows()):
                    curr_sub = self.uploadModel._subs[i]
                    curr_video = self.uploadModel._videos[i]
                    if curr_sub : #Make sure is not an empty row with None
                        buf = open(curr_sub.getFilePath()).read()
                        curr_sub_content = base64.encodestring(zlib.compress(buf))
                        cd = "cd" + str(i)
                        movie_info[cd] = {'subhash': curr_sub.getHash(), 'subfilename': curr_sub.getFileName(), 'moviehash': curr_video.calculateOSDBHash(), 'moviebytesize': curr_video.getSize(), 'movietimems': curr_video.getTimeMS(), 'moviefps': curr_video.getFPS(), 'moviefilename': curr_video.getFileName(), 'subcontent': curr_sub_content}

                if self.OSDBServer.UploadSubtitlesGUI(movie_info):
                    QMessageBox.about(self.window,"Success","Subtitles succesfully uploaded. Thanks.")
                else:
                    QMessageBox.about(self.window,"Error","Problem while uploading...")
    
    def onUploadIMDBNewSelection(self, id, title):
        id = str(id.toUtf8())
        if not id in self.uploadIMDB_list:
            self.uploadIMDB_list.append(id)
            self.uploadIMDB.addItem("%s : %s" % (id, title), QVariant(id)) #The dataItem is the ID
            
        #Let's select the item with that id.
        index = self.uploadIMDB.findData(QVariant(id))
        if index :
            self.uploadIMDB.setCurrentIndex (index)
            return
            
    def onUploadLanguageDetection(self, lang_xxx):
        #Let's select the item with that id.
        index = self.uploadLanguages.findData(QVariant(lang_xxx))
        if index :
            self.uploadLanguages.setCurrentIndex (index)
            return
            
    def updateButtonsUpload(self):
        self.uploadView.resizeRowsToContents()
        selected = self.uploadSelectionModel.selection()
        if selected.count():
            self.uploadModel.rowSelected = selected.last().bottomRight().row()
            self.buttonUploadMinusRow.setEnabled(True)
            if self.uploadModel.rowSelected != self.uploadModel.getTotalRows() -1:
                self.buttonUploadDownRow.setEnabled(True)
            else:
                self.buttonUploadDownRow.setEnabled(False)
                
            if self.uploadModel.rowSelected != 0:
                self.buttonUploadUpRow.setEnabled(True)
            else:
                self.buttonUploadUpRow.setEnabled(False)
        else:
            self.uploadModel.rowSelected = None
            self.buttonUploadDownRow.setEnabled(False)
            self.buttonUploadUpRow.setEnabled(False)
            self.buttonUploadMinusRow.setEnabled(False)
            
    def onUploadChangeSelection(self, selected, unselected):
        self.updateButtonsUpload()
        
    def onClickUploadViewCell(self, index):
        row, col = index.row(), index.column()
        settings = QSettings()
        currentDir = settings.value("mainwindow/workingDirectory", QVariant())
        
        if col == UploadListView.COL_VIDEO:
            fileName = QFileDialog.getOpenFileName(None, "Select Video", currentDir.toString(), videofile.SELECT_VIDEOS)
            if fileName:
                settings.setValue("mainwindow/workingDirectory", QVariant(QFileInfo(fileName).absolutePath()))
                video = VideoFile(str(fileName.toUtf8())) 
                self.uploadModel.emit(SIGNAL("layoutAboutToBeChanged()"))
                self.uploadModel.addVideos(row, [video])
                subtitle = Subtitle.AutoDetectSubtitle(video.getFilePath())
                if subtitle:
                    sub = SubtitleFile(False,subtitle) 
                    self.uploadModel.addSubs(row, [sub])
                    self.uploadModel.update_lang_upload()
                self.uploadView.resizeRowsToContents()
                self.uploadModel.emit(SIGNAL("layoutChanged()"))
        else:
            fileName = QFileDialog.getOpenFileName(None, "Select Subtitle", currentDir.toString(), subtitlefile.SELECT_SUBTITLES)
            if fileName:
                settings.setValue("mainwindow/workingDirectory", QVariant(QFileInfo(fileName).absolutePath()))
                sub = SubtitleFile(False, str(fileName.toUtf8())) 
                self.uploadModel.emit(SIGNAL("layoutAboutToBeChanged()"))
                self.uploadModel.addSubs(row, [sub])
                self.uploadView.resizeRowsToContents()
                self.uploadModel.emit(SIGNAL("layoutChanged()"))
                self.uploadModel.update_lang_upload()
                


def main(options):
    
    from PyQt4.Qt import QApplication, QMainWindow
    
    log.debug("Building main dialog")
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.showMessage(QApplication.translate("subdownloader", "Building main dialog..."))
    window = QMainWindow()
    window.setWindowTitle(APP_TITLE)
    window.setWindowIcon(QIcon(":/icon"))
    installErrorHandler(QErrorMessage(window))
    QCoreApplication.setOrganizationName("IvanGarcia")
    QCoreApplication.setApplicationName(APP_TITLE)
    
    log.debug("Showing main dialog")
    Main(window,"", options)    
    
    return app.exec_()

#if __name__ == "__main__": 
#    sys.exit(main())
