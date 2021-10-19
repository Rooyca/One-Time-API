![PyPI - Python Version](https://img.shields.io/pypi/pyversions/FastAPI?logo=Python&style=for-the-badge)
![PyPI - Status](https://img.shields.io/pypi/status/FastAPI?logo=FastAPI&style=for-the-badge)
![PyPI - License](https://img.shields.io/pypi/l/FastAPI?style=for-the-badge)
# One-Time-API

![ONCE-LOGO](https://res.cloudinary.com/rooyca/image/upload/v1633230309/Blog/Imgs/Once-Post/screen_qkwm0e.png)

An API to send files with one unique code that will let you download your file ***without*** * let trace on any server.

## How to use

You can check my app on [heroku](https://just-once.herokuapp.com/) or you can run it yourself. 
Just clone this repo and install the packets with:
```bash
pip install -r requirements.txt
```
Then:
```bash
uvicorn app:app 
```
**Here comes the tricky part...** You will need an **Azure** and **Redis** account.

If you have one student email you could register in Azure for free and get a trial account with 12 months of duration. ([Here](https://thetechrim.com/how-to-create-free-edu-email/) is something that you can try if you don't have one).

And you could set one Redis DB [here](redislabs.com).

---

Well, once we have everything set let's make some requests. To post data you will need Curl, Python, Postman or whatever you want to use. We are gonna use our browser (Firefox) for now. 
**One thing to have in mind:**
1. There are just some types of files allow to upload (txt, pdf, png, jpg, jpeg, gif, rar, zip, gzip, mp3, mp4, 3gp, wav)

I would try to overcome those limitations in a future version. For now let's upload some files to our API:

If you visit http://127.0.0.1/8000/docs you would see something like this:

![END-POINTS](https://res.cloudinary.com/rooyca/image/upload/v1634602120/Images/fastapi_ifejy4.png)

Now let's try uploading a PDF:

![UPLOAD](https://res.cloudinary.com/rooyca/image/upload/v1634602120/Images/upload_a3zj8n.png)

When you press Excecute it should return some information about the file and one code of four digits that we are going to use to download our file.
***Sometimes it raise an Internal Server Error because a conflict with our local hour***

Now, let's go to our other endpoint:

![DOWN](https://res.cloudinary.com/rooyca/image/upload/v1634602120/Images/down_kpzuom.png)

If you try to download it from here you would received a lot of strings and things that are not quite your file, so to get our file we are going to use Curl. It's as easy as:

```bash
curl http://127.0.0.1:8000/download/{your-id} --output "name-of-your-file.pdf"
```
And that should be it.

Remember
----
Once we redeem our code and download the file (or just visualise it) the file is gone for ever, so make sure that you actually save it.

* This is NOT 100% secure because the server in witch it's been upload is Microsoft property and we all know how is our uncle Bill... So use it carefully or don't use it at all. (Checkout [p2p](https://en.wikipedia.org/wiki/Peer-to-peer) and [IPFS](https://ipfs.io/))
