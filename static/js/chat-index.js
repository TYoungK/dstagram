let followings_modal=document.getElementById('user-list-modal');
let chatSocket = null;

document.querySelector("#roomSelect").onchange = function() {
    let roomName = document.querySelector("#roomSelect").value.split(" (")[0];
    window.location.pathname = "chat/" + roomName + "/";
}

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
            case "chat_message":
                chatLog.value += data.message + "\n";
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

//---

function getFollowings(user_tag){
    let xhr = new XMLHttpRequest();
    xhr.onload = ()=>{
        if (xhr.status === 200) {
        followings = JSON.parse(xhr.responseText);
        $('#chat_users_list').html('');
        for(var following of followings){
            $('#chat_users_list').append(
                '<li>'+
                '<a href="/chat/' + following.tag + '" class="flex items-center p-3 text-base font-bold text-gray-900 bg-gray-50 rounded-lg hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">'+
                '<img class="w-10 h-10 object-cover rounded-full p-1" src='+ following.profile_pic +'>'+
                '<span class="flex-1 ml-3 whitespace-nowrap">'+
                following.tag+
                '</span>'+
                '</a>'+
                '</li>'
                );
        }
        
        followings_modal.classList.replace('hidden', 'flex');
    }
    };
    xhr.open('GET', '/following/' + user_tag);
    xhr.send();
}

function hideFollowModal(){
    followings_modal.classList.replace('flex', 'hidden');
}
