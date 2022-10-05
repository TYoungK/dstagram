let followings_modal=document.getElementById('user-list-modal');
let chat_search = document.querySelector("#chat_list_text");
let modal_users_list = document.querySelector('#modal-chat-users-list')

const chat_search_users = function(event){
    if(chat_search.value != ''){
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = (e)=>{
        let req = e.target;
            if(req.readyState === XMLHttpRequest.DONE) {
                if(req.status === 200) {
                    var users = JSON.parse(req.responseText);
                    modal_users_list.innerHTML = "";
                    if(users.length){
                        for(var user of users){
                            modal_users_list.innerHTML +=
                                '<li>'+
                                '<a href="/mypage/' + user.tag + '" class="flex items-center p-3 text-base font-bold text-gray-900 bg-gray-50 rounded-lg hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">'+
                                '<img class="w-10 h-10 rounded-full" src='+ user.profile_pic +'>'+
                                '<span class="flex-1 ml-3 whitespace-nowrap">'+
                                    user.tag+
                                '</span>'+
                                '</a>'+
                                '</li>';
                        }   
                    }
                    else{
                        modal_users_list.innerHTML = "검색 결과가 없습니다."
                    }
                }
            }
        }
        // xhttp.open("GET", "{% url 'photo:search_user' user_tag='x'%}"+$(this).val(), true);
        xhttp.open("GET", "/search/"+ event.target.value, true);
        xhttp.send();
    }    
    else{
        modal_users_list.innerHTML = '';
    }
};

chat_search.addEventListener("propertychange",chat_search_users);
chat_search.addEventListener("change",chat_search_users);
chat_search.addEventListener("keyup",chat_search_users);
chat_search.addEventListener("paste",chat_search_users);

function getFollowings(user_tag){
    let xhr = new XMLHttpRequest();
    xhr.onload = ()=>{
        if (xhr.status === 200) {
        followings = JSON.parse(xhr.responseText);
        modal_users_list.innerHTML = "";
        for(var following of followings){
            modal_users_list.innerHTML +=
                '<li>'+
                '<a href="/chat/' + following.tag + '" class="flex items-center p-3 text-base font-bold text-gray-900 bg-gray-50 rounded-lg hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">'+
                '<img class="w-10 h-10 object-cover rounded-full p-1" src='+ following.profile_pic +'>'+
                '<span class="flex-1 ml-3 whitespace-nowrap">'+
                following.tag+
                '</span>'+
                '</a>'+
                '</li>'
                ;
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
