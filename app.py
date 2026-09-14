from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Darwan - LIVE Class</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family: 'Hind Siliguri', sans-serif;}
body{background:#0f172a;color:white;}
.topbar{background:#1e293b;padding:12px 15px;display:flex;align-items:center;gap:10px;position:sticky;top:0;}
.logo{font-size:18px;}
.btn{border:none;padding:10px 18px;border-radius:25px;font-weight:bold;cursor:pointer;font-size:14px;}
.btn-green{background:#22c55e;color:white;}
.btn-dark{background:#334155;color:#cbd5e1;}
.card{background:#1e293b;margin:15px;border-radius:15px;padding:15px;}
.input{width:100%;padding:12px;border-radius:10px;border:none;font-size:14px;margin-bottom:10px;color:#333;}
.row{display:flex;gap:10px;flex-wrap:wrap;}
.video-box{background:black;width:100%;height:220px;border-radius:15px;margin-bottom:10px;position:relative;overflow:hidden;}
video{width:100%;height:100%;object-fit:cover;}
.small-text{font-size:15px;margin-top:5px;}
#recordList{margin-top:10px;}
.rec-item{background:#0f172a;padding:8px;border-radius:8px;margin:5px 0;font-size:13px;}
</style>
</head>
<body>

<div class="topbar">
  <span class="logo">🔒 Darwan</span>
  <button class="btn btn-green" onclick="showLive()">LIVE ক্লাস</button>
  <button class="btn btn-dark" onclick="showRecord()">📼 রেকর্ড দেখো</button>
</div>

<div id="livePage">
  <div class="card">
    <input id="className" class="input" placeholder="ক্লাসের নাম: Class-10">
    <div class="row">
      <button class="btn btn-green" onclick="startClass()">ক্লাস শুরু + 🔴 রেকর্ড চালু</button>
    </div>
    <div class="row" style="margin-top:10px;">
      <button class="btn" style="background:#ef4444;color:white;" onclick="startRec()">🔴 রেকর্ড শুরু</button>
      <button class="btn btn-dark" onclick="stopRec()">⏹️ রেকর্ড শেষ ও সেভ</button>
    </div>
  </div>

  <div class="card">
    <div class="video-box">
      <video id="video" autoplay muted playsinline></video>
    </div>
    <p class="small-text" id="status">ক্যামেরা চালু করুন</p>
  </div>
</div>

<div id="recordPage" style="display:none;">
  <div class="card">
    <h3>📼 সেভ করা রেকর্ড</h3>
    <div id="recordList"><p style="color:#94a3b8;font-size:13px;">এখনো কোনো রেকর্ড নেই</p></div>
  </div>
</div>

<script>
let mediaRecorder;
let chunks=[];
let stream;
let records=[];

async function startClass(){
 let name=document.getElementById('className').value || 'Class-10';
 document.getElementById('status').innerText = name + ' - LIVE চলছে...';
 try{
   stream = await navigator.mediaDevices.getUserMedia({video:true,audio:true});
   document.getElementById('video').srcObject=stream;
   startRec();
 }catch(e){ alert('ক্যামেরা চালু করতে পারছি না: '+e); }
}

function startRec(){
 if(!stream){ alert('আগে ক্লাস শুরু করুন'); return; }
 chunks=[];
 mediaRecorder=new MediaRecorder(stream);
 mediaRecorder.ondataavailable=e=>chunks.push(e.data);
 mediaRecorder.onstop=saveRec;
 mediaRecorder.start();
 document.getElementById('status').innerText='🔴 রেকর্ড হচ্ছে...';
}

function stopRec(){
 if(mediaRecorder && mediaRecorder.state!='inactive'){
   mediaRecorder.stop();
   document.getElementById('status').innerText='✅ রেকর্ড সেভ হয়েছে';
 }
}

function saveRec(){
 let blob=new Blob(chunks,{type:'video/webm'});
 let url=URL.createObjectURL(blob);
 let name=document.getElementById('className').value || 'Class';
 let time=new Date().toLocaleString();
 records.push({url,name,time});
 renderRecords();
}

function renderRecords(){
 let list=document.getElementById('recordList');
 if(records.length==0) return;
 list.innerHTML='';
 records.forEach((r,i)=>{
   list.innerHTML+=`<div class="rec-item">📌 ${r.name} - ${r.time} <br><a href="${r.url}" download="${r.name}.webm" style="color:#22c55e;">⬇️ ডাউনলোড</a> | <a href="${r.url}" target="_blank" style="color:#38bdf8;">▶️ দেখো</a></div>`;
 });
}

function showLive(){
 document.getElementById('livePage').style.display='block';
 document.getElementById('recordPage').style.display='none';
}
function showRecord(){
 document.getElementById('livePage').style.display='none';
 document.getElementById('recordPage').style.display='block';
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
