# One-Time-API

A simple API to send files with one unique code that will let you download your file without let trace on any server.

## How to use it

You can check my app on [heroku](https://just-once.herokuapp.com/) or if you prefer you could run the app from your machine,
you just need to clone this repository, install the packets with a simple:
```bash
pip install -r requirements.txt
```
After you run the API with:
```bash
python app.py
```
**Here comes the tricky part...**

You will need two more things:
1. Azure and a MongoDB account.
2. A "config.yaml" file to save your credentials.

Well, once we have everythin set it's importa to know that there are two endpoints: "/upload" and "/download/<id>". 
To post data you will need to make a request with curl, python, or postman, it's up to you. We are gonna use curl for now. 
**Two things to know:**
1. There is a Max Size of File of 16MB's.
2. There are some types of files allow to upload (txt, pdf, png, jpg, jpeg, gif, rar, zip, gzip, mp3, mp4, 3gp)

I would try to overcome those limitations in a future. Well, let's upload some file to our API:
```bash
curl -F "total_files=@namefile.txt" http://127.0.0.1:5000/upload
```
You should get a ID, save it, we'll be using it in a second to download our file. For that we have several options. We'll be using 
the easiest one, the browser. We just go to:
```bash
http://127.0.0.1:5000/download/<our id>
```
That would display the file in our browser, if we want to download it, we have to press "Ctrl+S", otherwise, if you reload the page the file
will be gone.

# Something to have in mind

I have been learning coding for about three months now, and this is my first real project. It will mean a lot to me if you could help me
to improve the API or the web itself. Because I'm pretty sure I had make several mistakes in the process... It doesn't matter if it's a litter
thing or a big one, please let me know. (I sure you have notice it that English isn't my first language so feel free to correct me)
