import tornado.web
import tornado.ioloop
import os
import subprocess
import shutil
#shutil.rmtree('/home/me/test') 
parent = os.getcwd()
os.chdir(parent)
class uploadHandler(tornado.web.RequestHandler):
    def post(self):
       
        files = self.request.files["videoFile"]
        for f in files:
            fh = open(f"upload/{f.filename}", "wb")
            fh.write(f.body)
            fh.close()
        out = os.path.splitext(f.filename)[0] + '.mp3'    
        subprocess.call(['ffmpeg', '-i', 'upload/'+f.filename , 'audio/'+out,'-y'])
        self.write(
        "<head><title>Mp4 -> Mp3</title></head><a href = '/audio/"+ out+"'alignment = 'right'><Button type = 'button'>Play now</Button></a><br><br><a href = '/audio/"+ out+"'alignment = 'right' download><Button type = 'button'>Download now</Button></a>")
      
    def get(self):
        self.render("index.html")
        try:
            shutil.rmtree(parent+'/upload')
            shutil.rmtree(parent+'/audio')
            os.mkdir('upload')
            os.mkdir('audio')  
        except FileExistsError:
            print("Already exist")
          

try:
    os.mkdir('upload')
    os.mkdir('audio')  
except FileExistsError:
    print("Already exist")     
if (__name__ == "__main__"):
    parent = os.getcwd()
    os.chdir(parent)
    
    
    app = tornado.web.Application([
        ("/", uploadHandler),
        ("/audio/(.*)", tornado.web.StaticFileHandler,  {'path': 'audio'})
    ])
    
    app.listen(8080)
    print("Listening on port 8080")
    print(os.getcwd())
    tornado.ioloop.IOLoop.instance().start()
  
