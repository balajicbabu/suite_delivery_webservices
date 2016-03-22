import ftplib
import os
import sys
import test
import testData
import squish

def copy_to_ftp_server(local_manifest_file_path,ftp_delivery_path,ftp_vevo_host,ftp_vevo_user,ftp_vevo_password):
    test.log("copy_to_ftp_server started")
    test.log("local_manifest_file_path : " + local_manifest_file_path)
    test.log("ftp_delivery_path : " + ftp_delivery_path)
    squish.snooze(60)

    test.log("copying : "  + local_manifest_file_path + "to " +ftp_delivery_path)
    session = ftplib.FTP(ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
    file = open(local_manifest_file_path, 'rb')                  # file to send
    files = session.nlst()
    print files
    session.cwd(ftp_delivery_path)                   # Change working directory 
    session.storbinary('STOR status-manifest.xml', file)  # send the file using STOR command
    file.close()                                    # close file and FTP
    session.quit()
    test.log("copy_to_ftp_server finished")

    
def check_contents_in_ftp_server_and_download_manifest(ftp_delivery_path,ftp_vevo_host,ftp_vevo_user,ftp_vevo_password):
    test.log("check_contents_in_ftp_server_and_download_manifest")
    test.log("ftp_delivery_path : " + ftp_delivery_path)
    squish.snooze(60)

    files = []
    absolute_path = None
    squish.snooze(60)

    try:
        session = ftplib.FTP(ftp_vevo_host, ftp_vevo_user, ftp_vevo_password)
        print session
        session.cwd(ftp_delivery_path) # Change working directory 
        files = session.nlst()
        print files
        for filename in files:
            print filename
            #getting delivery.complete.lock file as soon as file transfer has been done(look for that as well)
            if(len(files) == 3 and filename == "manifest.xml"):
                print filename
                
                testdata = testData.create("shared", filename)
                print testdata
                #dataFile = open(testdata, "w")
                #local_filename = os.path.join('download_manifest', filename)
                absolute_path = os.path.abspath(testdata)
                print absolute_path
                file = open(testdata, 'wb')
                session.retrbinary('RETR %s' % filename, file.write)
                file.close()
            elif(len(files) > 3):
                test.fail("no of files in the FTP server are more than 3")
                test.log(len(files))

            elif(len(files) < 3):
                test.fail("no of files in the FTP server are less than 3")
                test.log(len(files))

        session.quit()
        return absolute_path 
    except Exception as e:
        test.fail("check_contents_in_ftp_server_and_download_manifest")
        print e
        s = str(e)
        print sys.exc_info()
        test.log(s)
           

