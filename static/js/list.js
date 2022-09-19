let follow_modal = document.getElementById('share-modal');
let share_search = document.querySelector("#share_search_text");
let share_list = document.querySelector('#share_users_list');

const share_search_users = function(event){
    if(share_search.value != ''){
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = (e)=>{
        let req = e.target;
            if(req.readyState === XMLHttpRequest.DONE) {
                if(req.status === 200) {
                    var users = JSON.parse(req.responseText);
                    share_list.innerHTML = "";
                    if(users.length){
                        for(var user of users){
                            share_list.innerHTML +=
                                '<li class="flex">'+
                                '<a href="/mypage/' + user.tag + '" class="flex items-center w-full p-3 text-base font-bold text-gray-900 bg-gray-50 rounded-lg hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">'+
                                '<img class="w-10 h-10 rounded-full" src='+ user.profile_pic +'>'+
                                '<span class="flex-1 ml-3 whitespace-nowrap">'+
                                    user.tag+
                                '</span>'+
                                '</a>'+
                                '<a href="/chat/'+ user.tag +'" class="flex min-w-fit items-center border p-3">보내기</a>'+
                                '</li>';
                        }   
                    }
                    else{
                        share_list.innerHTML = "검색 결과가 없습니다."
                    }
                }
            }
        }
        // xhttp.open("GET", "{% url 'photo:search_user' user_tag='x'%}"+$(this).val(), true);
        xhttp.open("GET", "/search/"+ event.target.value, true);
        xhttp.send();
    }    
    else{
        share_list.innerHTML = '';
    }
};

share_search.addEventListener("propertychange",share_search_users);
share_search.addEventListener("change",share_search_users);
share_search.addEventListener("keyup",share_search_users);
share_search.addEventListener("paste",share_search_users);

function getFollowings(user_tag, post_id){
    let xhr = new XMLHttpRequest();
    xhr.onload = ()=>{
        if (xhr.status === 200) {
        followers = JSON.parse(xhr.responseText);
        share_list.innerHTML = '';
        for(var follower of followers){
            share_list.innerHTML +=
                '<li class="flex">'+
                '<a href="/mypage/' + follower.tag + '" class="flex items-center w-full p-3 text-base font-bold text-gray-900 bg-gray-50 rounded-lg hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">'+
                '<img class="w-10 h-10 object-cover rounded-full p-1" src='+ follower.profile_pic +'>'+
                '<span class="flex-1 ml-3 whitespace-nowrap">'+
                follower.tag+
                '</span>'+
                '</a>'+
                '<button class="flex min-w-fit items-center border p-3" onclick="connect(\'' + 
                follower.tag + '\',\'' + post_id + '\');">보내기</button>'+
                '</li>';
        }
        
        follow_modal.classList.replace('hidden', 'flex');
    }
    };
    xhr.open('GET', '/following/' + user_tag);
    xhr.send();
}

function hideFollowModal(){
    follow_modal.classList.replace('flex', 'hidden');
}


let chatSocket = null;

function connect(user_tag, post_id) {
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + user_tag + "/");

    chatSocket.onopen = function(e) {
        chatSocket.send(JSON.stringify({
            "message": window.location.protocol + "//" + window.location.host + "/detail/" + post_id,
        }))
        window.location.href = window.location.protocol + "//" + window.location.host + "/chat/" + user_tag
    }

    chatSocket.onmessage = function(e) {
        
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}