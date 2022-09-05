console.log("Sanity check from room.js.");

const roomName = JSON.parse(document.getElementById('roomName').textContent);

let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");

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
        console.log(data);

        switch (data.type) {
            case "chat_catalog":
                var chatLogul = document.createElement("ul");
                for (var msg of data.messages){
                    if(msg.my_message){
                        chatLog.innerHTML += 
                        '<li class="flex items-center justify-end px-4"><div class="px-4 border w-fit max-w-[50%]">' + msg.content + '</div></li>';
                    }else{
                        chatLog.innerHTML += 
                        '<li class="flex items-center px-4"><div class="px-4 border w-fit max-w-[50%]">' + msg.content + '</div></li>';
                    }
                    
                }
                chatLog.append(chatLogul);
                chatLog.parentElement.scrollTop = chatLog.parentElement.scrollHeight
                break;
            case "chat_message":
                console.log(roomName, data.user)
                if(roomName==data.user){
                    chatLog.innerHTML += 
                        '<li class="flex items-center px-4"><div class="px-4 border w-fit max-w-[50%]">' + data.message + '</div></li>';
                }else{
                    chatLog.innerHTML += 
                        '<li class="flex items-center justify-end px-4"><div class="px-4 border w-fit max-w-[50%]">' + data.message + '</div></li>';
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