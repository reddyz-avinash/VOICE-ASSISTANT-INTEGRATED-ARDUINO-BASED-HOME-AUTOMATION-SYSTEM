function bulbOn(){

fetch("/bulb/on");

}

function bulbOff(){

fetch("/bulb/off");

}

function fanOn(){

fetch("/fan/on");

}

function fanOff(){

fetch("/fan/off");

}

function updateStatus(){

fetch("/device/status")

.then(r=>r.json())

.then(data=>{

document.getElementById("bulb").innerHTML=data.bulb;

document.getElementById("fan").innerHTML=data.fan;

document.getElementById("time").innerHTML=data.time;

document.getElementById("date").innerHTML=data.date;

});

}

setInterval(updateStatus,1000);

function updateStatus(){

fetch("/device/status")

.then(response => response.json())

.then(data => {

document.getElementById("bulb").innerHTML = data.bulb;

document.getElementById("fan").innerHTML = data.fan;

document.getElementById("time").innerHTML = data.time;

document.getElementById("date").innerHTML = data.date;

if(data.connected){

document.getElementById("espStatus").innerHTML="🟢 Connected";

}else{

document.getElementById("espStatus").innerHTML="🔴 Disconnected";

}

let html="";

data.history.forEach(function(item){

html += "<p>"

+ item.time

+ " | "

+ item.source

+ " | "

+ item.command

+ "</p>";

});

document.getElementById("history").innerHTML = html;

});

}
let chat="";

data.chat.forEach(function(c){

chat+="<b>You:</b> "+c.user+"<br>";

chat+="<b>AI:</b> "+c.assistant+"<hr>";

});

document.getElementById("chatHistory").innerHTML=chat;
// ======================================
// AI CHAT
// ======================================

function askAI() {

    let question = document.getElementById("question").value.trim();

    if (question === "") {

        alert("Please enter a question.");

        return;

    }

    document.getElementById("answer").value = "Thinking...";

    fetch("/chat", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            message: question

        })

    })

    .then(response => response.json())

    .then(data => {

        document.getElementById("answer").value = data.reply;

    })

    .catch(error => {

        console.log(error);

        document.getElementById("answer").value =
        "Unable to connect to AI.";

    });

}