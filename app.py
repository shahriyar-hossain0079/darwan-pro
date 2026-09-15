
import os
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'darwan-secret'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

HTML = """ 
<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Darwan - LIVE Class + Student Voice</title>
<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Hind Siliguri', sans-serif}
body{background:#0f172a;color:white;}
.topbar{background:#1e293b;padding:12px 15px;display:flex;align-items:center;justify-content:space-between}
.logo{font-size:18px;font-weight:bold}
.btn{border:none;padding:10px 18px;border-radius:25px;font-weight:bold;cursor:pointer}
.btn-green{background:#22c55e;color:white;}
.btn-dark{background:#334155;color:#cbd5e1;}
.card{background:#1e293b;margin:15px;border-radius:15px;padding:15px;}
.input{width:100%;padding:12px;border-radius:10px;border:none;font-size:16px;margin:8px 0}
.row{display:flex;gap:10px;flex-wrap:wrap}
#livePage, #recordPage{display:none}
video{width:100%;border-radius:12px;background:black;max-height:400px}
.ask-btn{background:#ff9800;color:white;padding:12px 20px;border:none;border-radius:10px;font-size:16px;width:100%;margin-top:10px}
.req-box{background:#fff3cd;color:#333;padding:10px;margin:5px 0;border-radius:8px}
</style>
</head>
<body>
<div class="topbar">
<div class="logo">🔴 Darwan LIVE Pro</div>
<div id="userInfo"></div>
</div>
<div id="gatePage" class="card">
<h2>🔐 ID দিয়ে প্রবেশ করুন</h2>
<input id="studentId" class="input" placeholder="আপনার ID লিখুন (যেমন: 12345)">
<button class="btn btn-green" onclick="checkId()">প্রবেশ করুন</button>
</div>
<div id="examPage" class="card" style="display:none">
<h2>📝 ভর্তি পরীক্ষা</h2>
<p>২ টা প্রশ্নের উত্তর দিন</p>
<p>১. বাংলাদেশের রাজধানী কি?</p>
<input id="q1" class="input" placeholder="উত্তর">
<p>২. 2+2 = ?</p>
<input id="q2" class="input" placeholder="উত্তর">
<button class="btn btn-green" onclick="submitExam()">জমা দিন</button>
</div>
<div id="livePage" class="card">
<h2>🔴 LIVE ক্লাস চলছে</h2>
<div id="teacherRequests"></div>
<video id="localVideo" autoplay muted playsinline></video>
<video id="remoteVideo" autoplay playsinline style="display:none"></video>
<div class="row">
<button class="btn btn-green" onclick="startCamera()">📷 ক্যামেরা চালু + রেকর্ড চালু</button>
<button class="btn btn-dark" onclick="showRecord()">📁 রেকর্ড দেখুন</button>
</div>
<div id="studentPanel">
<button id="askBtn" class="ask-btn" onclick="askQuestion()">🎤 প্রশ্ন করতে চাই</button>
<p style="font-size:12px;text-align:center;margin-top:5px;color:#94a3b8">বাটন চাপলে স্যারের কাছে অনুরোধ যাবে</p>
</div>
</div>
<div id="recordPage" class="card">
<h2>📁 রেকর্ডেড ক্লাস</h2>
<div id="recordList"></div>
<button class="btn btn-dark" onclick="showLive()">🔙 Live এ ফিরে যান</button>
</div>
<script>
let isTeacher = false;
let currentStudentName = localStorage.getItem('darwan_name') || 'ছাত্র';
let records = JSON.parse(localStorage.getItem('records')||'[]');
const socket = io();
let studentMicStream = null;
let isTeacherMode = false;
function checkId(){
let id = document.getElementById('studentId').value;
if(!id){ alert('ID লিখুন'); return; }
currentStudentName = id;
localStorage.setItem('darwan_name', id);
if(id.toLowerCase().includes('teacher') || id=='admin' || id=='100'){
isTeacher = true;
isTeacherMode = true;
alert('স্যার, আপনি টিচার হিসেবে প্রবেশ করেছেন - ছাত্ররা প্রশ্ন করলে এখানে দেখতে পাবেন');
}
document.getElementById('gatePage').style.display='none';
document.getElementById('examPage').style.display='block';
}
function submitExam(){
let q1 = document.getElementById('q1').value.toLowerCase();
let q2 = document.getElementById('q2').value;
if((q1.includes('dhaka') || q1.includes('ঢাকা')) && q2=='4'){
document.getElementById('examPage').style.display='none';
document.getElementById('livePage').style.display='block';
document.getElementById('userInfo').innerText = currentStudentName + (isTeacher?' (Teacher)':'');
if(isTeacher){
document.getElementById('studentPanel').style.display='none';
}
}else{
alert('একটা ভুল হয়েছে, আবার চেষ্টা করুন');
}
}
async function startCamera(){
try{
let stream = await navigator.mediaDevices.getUserMedia({video:true, audio:true});
document.getElementById('localVideo').srcObject = stream;
}catch(e){
alert('ক্যামেরা চালু করতে Allow দিন');
}
}
function askQuestion(){
if(!studentMicStream){
navigator.mediaDevices.getUserMedia({audio:true}).then(stream=>{
studentMicStream = stream;
socket.emit('student-raise-hand', {name: currentStudentName});
document.getElementById('askBtn').innerText = '⏳ স্যারের অনুমতির অপেক্ষায়...';
document.getElementById('askBtn').style.background='#64748b';
}).catch(()=>{
alert('মাইক্রোফোন Allow করুন');
});
}
}
function allowStudent(name){
socket.emit('allow-student', {name: name});
let el = document.getElementById('req-'+name);
if(el) el.remove();
alert(name + ' কে অনুমতি দেওয়া হয়েছে');
}
socket.on('student-raise-hand', (data)=>{
if(isTeacher){
let box = document.getElementById('teacherRequests');
box.innerHTML += `<div id="req-${data.name}" class="req-box"> 📢 <b>${data.name}</b> প্রশ্ন করতে চায় <button onclick="allowStudent('${data.name}')" style="background:green;color:white;padding:5px 12px;border:none;border-radius:5px;margin-left:10px">Allow 🎤</button> </div>`;
}
});
socket.on('teacher-allowed', (data)=>{
if(data.name == currentStudentName){
alert('🎤 স্যার আপনাকে কথা বলার অনুমতি দিয়েছেন! এখন মাইক চালু আছে, প্রশ্ন করুন');
document.getElementById('askBtn').innerText = '🎤 মাইক চালু - কথা বলুন';
document.getElementById('askBtn').style.background='#22c55e';
}
});
function renderRecords(){
let list=document.getElementById('recordList');
if(records.length==0) return;
list.innerHTML='';
records.forEach((r,i)=>{
list.innerHTML+=`<div class="req-box">📌 ${r.name} - ${r.time}<br><video src="${r.url}" controls style="width:100%;margin-top:5px"></video></div>`;
});
}
function showLive(){
document.getElementById('livePage').style.display='block';
document.getElementById('recordPage').style.display='none';
}
function showRecord(){
document.getElementById('livePage').style.display='none';
document.getElementById('recordPage').style.display='block';
renderRecords();
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

@socketio.on('student-raise-hand')
def handle_raise(data):
    emit('student-raise-hand', data, broadcast=True)

@socketio.on('allow-student')
def handle_allow(data):
    emit('teacher-allowed', data, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
