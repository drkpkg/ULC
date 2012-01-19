#!/usr/bin/env python
# coding: utf-8
import os
import commands
import sys

'''
Cocas por hacer:

    - Verificar entradas.
    - Leer archivos de configuración.
    - Manager de proyectos.
    - Desempaquetar el squashfs.
    - Xephir.
'''

class enter_chroot():
    def __init__(self,PATH,project_name):
        """ Custom live cd, Uremix Team
        self.RPATH -> Dirección de la ISO
        self.CDPATH -> Direccion de los archivos ya sincronizados
        self.DIRISO -> Lugar temporal donde estará la ISO montada
        self.SQUASHFS -> Lugar del sistema enjaulado
        self.INITRD -> Initrd nuevo"""    
        if((PATH!="")&(project_name!="")):
            self.NAME = project_name
            self.RPATH = PATH #path de la iso
            self.CDPATH = "/home/projects/"+project_name+"/future-iso/"
            self.DIRISO = "/home/projects/"+project_name+"/temp-iso/"
            self.CASPER = self.DIRISO+"casper/filesystem.squashfs"
            self.SQUASHFS = "/home/projects/"+project_name+"/filesystem/"
            self.INITRD = "/home/projects/"+project_name+"/initrd"

            whoami = commands.getoutput("/usr/bin/whoami")
            if (whoami!="root"):
                print "you need be root, not a wannabe :D"
            else:
                if os.path.exists(PATH):
                    self.create_jail(self.CDPATH)
                    #self.create_jail(self.RPATH)
                    self.create_jail(self.DIRISO)
                    self.create_jail(self.INITRD)
                    self.create_jail(self.SQUASHFS)
                    self.mount_iso(self.RPATH)
                    self.sync_iso()
                    #self.chroot(PATH)
                    self.dpack()
                    
    def cleaner(self):
        if(self.NAME!=""):
            os.system("rm -r "+"/home/projects/"+self.NAME)
        else:
            print "Tiene que crear un nuevo proyecto"
            
    def dpack(self):
        #print self.CASPER
        self.send_message("Desempaquetando el sistema de archivos SquashFS. Tal vez quieras ir a caminar un poco o comer un bocadillo que dices?")
        print os.system("unsquashfs -f -d"+" "+self.SQUASHFS+" "+self.CASPER)
        #print commands.getoutput("unsquashfs "+self.CASPER+" "+self.SQUASHFS)
        print "Desmontando el Archivo Iso montado. Ahora a trabajar."
        os.system("umount " + self.DIRISO)
        
    def chroot(self):
        """Inicia el chroot."""
        self.mount_primary()
        print "Entrando al sistema enjaulado."
        os.system("chroot "+self.RPATH)
    
    def mount_iso(self,ISO):
        try:
            #os.system("mkdir -p " + self.DIRISO)
            os.system("mount -o loop " + ISO +" "+self.DIRISO) 
            print "Todo correcto."
        except:
            print "La imagen Iso no existe!"
        
    def sync_iso(self):
        """Sincroniza los archivos de la Iso, por el momento solo ubuntu."""
        self.send_message("Iniciando sincronizacion de archivos dentro del cd. Esto puede tardar un tiempo.")
        os.system("rsync --exclude=/casper/filesystem.squashfs -a " +self.DIRISO+"* "+self.CDPATH) 
        
    def mount_primary(self):
        """Monta de manera automática lo necesario para que el sistema funcione."""
        os.system("mount --bind /dev/" + self.SQUASHFS + "/dev/")
        os.system("mount --bind /dev/shm" + self.SQUASHFS + "/dev/shm")
        os.system("mount --bind /dev/pts" + self.SQUASHFS + "/dev/pts")
        os.system("mount --bind /sys/" + self.SQUASHFS + "/sys/")
        os.system("mount --bind /proc/" + self.SQUASHFS + "/proc/")
        os.system("cp -f /etc/resolv.conf" + self.SQUASHFS + "/etc/resolv.conf")
        
    def create_jail(self,directory):
        """Crea los archivos necesarios, tambien sirve para crear otros."""
        os.system("mkdir -p "+directory)
        
    def send_message(self,text):
        return text
        
#if __name__ == '__main__':
    '''Esto solo es para probar'''
    '''path_iso = raw_input()
    name_proj = raw_input()
    enter_chroot(path_iso,name_proj)'''
