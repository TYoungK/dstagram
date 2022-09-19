console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
const pattern = new RegExp("^((http|https)\:\/\/)?[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\:\'\/\\\\+=&%\$#_]*)?$");

function validURL(str) {
    return pattern.test(str);
}

function create_protocol(str){
    if(!str.startsWith('http')){
        str = 'http://' + str
    }
    return str
}

function createLeftMessage(str){
    if(validURL(str)){
        return '<li class="flex items-center px-4"><div class="px-4 border w-fit max-w-[50%]">' + 
        '<a class="underline text-blue-600" href="' + create_protocol(str) + '" target="_blank">' + str + '</a></div></li>';
    }else{
        return '<li class="flex items-center px-4"><div class="px-4 border w-fit max-w-[50%]">' + str + '</div></li>';
    }
}

function createRightMessage(str){
    if(validURL(str)){
        return '<li class="flex items-center justify-end px-4"><div class="px-4 border w-fit max-w-[50%]">' + 
        '<a class="underline text-blue-600" href="' + create_protocol(str) + '" target="_blank">' + str + '</a></div></li>';
    }else{
        return '<li class="flex items-center justify-end px-4"><div class="px-4 border w-fit max-w-[50%]">' + str + '</div></li>';
    }
}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) return;
    chatSocket.send(JSON.stringify({
        "message": chatMessageInput.value,
    }));
    chatMessageInput.value = "";
};

let chatSocket = null;

function connect() {
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/");

    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);

        switch (data.type) {
            case "chat_catalog":
                var chatLogul = document.createElement("ul");
                for (var msg of data.messages){
                    if(msg.my_message){
                        chatLog.innerHTML += createRightMessage(msg.content);
                    }else{
                        chatLog.innerHTML += createLeftMessage(msg.content);
                    }
                    
                }
                chatLog.append(chatLogul);
                chatLog.parentElement.scrollTop = chatLog.parentElement.scrollHeight
                break;
            case "chat_message":
                if(roomName==data.user){
                    chatLog.innerHTML += createLeftMessage(data.message);
                }else{
                    chatLog.innerHTML += createRightMessage(data.message);
                }
                chatLog.parentElement.scrollTop = chatLog.parentElement.scrollHeight
                break;
            default:
                console.error("Unknown message type!");
                break;
        }

        // scroll 'chatLog' to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    };


    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}
connect();