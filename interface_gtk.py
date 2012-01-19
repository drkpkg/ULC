#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pygtk
pygtk.require("2.0")
import gtk,gobject
import gtk.glade
import commands
import os
import livetools
from livetools import enter_chroot

class interface():
    def __init__(self):
        self.iso = ""
        self.tool = enter_chroot("","")
        self.gladefile = "interface.ui"
        self.wTree = gtk.glade.XML(self.gladefile,"main_window")
        self.wTree.get_widget("main_window").set_title(("Live CD Customization"))
        self.wTree.get_widget("main_window").set_icon_from_file("/usr/lib/uremix/uremixwelcome/uremix-icon.png") 
        self.wTree.get_widget("Biso").connect('clicked',self.window_search)
        self.wTree.get_widget("Bclose").connect('clicked',self.quit_window)
        self.wTree.get_widget("imagemenuitem5").connect('activate',self.quit_window)
        self.wTree.get_widget("imagemenuitem10").connect('activate',self.view_about)
        self.wTree.get_widget("Bclean").connect('clicked',self.limpiar)
        self.wTree.get_widget("Bchroot").connect('clicked',self.enter_root)
            
        self.wTree.get_widget("main_window").show_all()
    
    def view_about(self, signal):
        self.about = gtk.glade.XML(self.gladefile,"about_window")
        self.about.get_widget("about_window").show()
    
    def window_search(self,signal):
        filtro = gtk.FileFilter()
        filtro.add_mime_type("application/x-cd-image")
        self.window = gtk.glade.XML(self.gladefile,"directory_window")
        self.window.get_widget("directory_window").set_title(("Selección de ISO"))
        self.window.get_widget("combobox1").set_active(0)
        self.window.get_widget("chooser").set_filter(filtro)
        self.window.get_widget("Bcancel").connect('clicked',self.hide)
        self.window.get_widget("Bselect").connect('clicked',self.seliso)
        self.window.get_widget("directory_window").show()
    
    def seliso(self,signal):
        
        if(self.wTree.get_widget("entry2").get_text()!=""):
            self.iso=self.window.get_widget("chooser").get_filename()
            #self.hide(None)
            iso=self.iso.split("/")
            self.wTree.get_widget("entry1").set_text(iso[len(iso)-1])
            #print self.iso
            
            #Iniciando...
            #self.wTree.get_widget("evento").show()
            #self.wTree.get_widget("spinner").show()
            #self.wTree.get_widget("spinner").start()
        
            #Iniciando los procesos
            self.window.get_widget("directory_window").destroy()
            self.tool = enter_chroot(self.iso,self.wTree.get_widget("entry2").get_text())
            #txt=enter_chroot.send_message()
            #self.wTree.get_widget("label4").set_text(txt)
            
            #self.wTree.get_widget("spinner").stop()
            #self.wTree.get_widget("spinner").hide()
            #self.wTree.get_widget("evento").hide()
        
        else:
            print "No tiene nombre, abortando."
    
    def enter_root(self,signal):
         self.tool.chroot()
        
    def limpiar(self,signal):
         self.tool.cleaner()
        
    def hide(self,signal):
        self.window.get_widget("directory_window").destroy()
        
    def quit_window(self,signal):
        gtk.main_quit()
    
def main():
    gtk.main()
    return 0
    
if __name__ == "__main__":
    interface()
    main()

