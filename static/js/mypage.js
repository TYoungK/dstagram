let follow_modal=document.getElementById('follow-modal');
let folllow_modal_header=document.getElementById('follow-modal-header');
let user_config_modal=document.getElementById('user-config-modal');
function disable_on_click() {
    var element = document.getElementById('submit-btn');
    element.setAttribute("disabled", "disabled");
}
function getFollowers(user_tag){
    let xhr = new XMLHttpRequest();
    xhr.onload = ()=>{
        if (xhr.status === 200) {
        followers = JSON.parse(xhr.responseText);
        $('#follow_list').html('');
        for(var follower of followers){
            $('#follow_list').append(
                '<li>'+
                '<a href="/mypage/' + follower.tag + '" class="flex items-center p-3 text-base font-bold text-gray-900 bg-gray-50 rounded-lg hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white z-[60]">'+
                '<img class="w-10 h-10 rounded-full" src='+ follower.profile_pic +'>'+
                '<span class="flex-1 ml-3 whitespace-nowrap">'+
                follower.tag+
                '</span>'+
                '</a>'+
                '</li>'
                );
        }
        
        folllow_modal_header.innerHTML = "팔로워";
        follow_modal.classList.replace('hidden', 'flex');
    }
    };
    xhr.open('GET', '/follower/' + user_tag);
    xhr.send();
}

function getFollowings(user_tag){
    let xhr = new XMLHttpRequest();
    xhr.onload = ()=>{
        if (xhr.status === 200) {
        followers = JSON.parse(xhr.responseText);
        $('#follow_list').html('');
        for(var follower of followers){
            $('#follow_list').append(
                '<li>'+
                '<a href="/mypage/' + follower.tag + '" class="flex items-center p-3 text-base font-bold text-gray-900 bg-gray-50 rounded-lg hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">'+
                '<img class="w-10 h-10 object-cover rounded-full p-1" src='+ follower.profile_pic +'>'+
                '<span class="flex-1 ml-3 whitespace-nowrap">'+
                follower.tag+
                '</span>'+
                '</a>'+
                '</li>'
                );
        }
        
        follow_modal_header.innerHTML = "팔로잉";
        follow_modal.classList.replace('hidden', 'flex');
    }
    };
    xhr.open('GET', '/following/' + user_tag);
    xhr.send();
}

function hideFollowModal(){
    modal.classList.replace('flex', 'hidden');
}

function showConfigModal(){
    user_config_modal.classList.replace('hidden', 'flex');
}

function hideConfigModal(){
    user_config_modal.classList.replace('flex', 'hidden');
}