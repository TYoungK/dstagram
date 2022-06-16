let modal=document.getElementById('follow-modal');
let modal_header=document.getElementById('follow-modal-header');
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
        
        modal_header.innerHTML = "팔로워";
        modal.classList.replace('hidden', 'flex');
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
        
        modal_header.innerHTML = "팔로잉";
        modal.classList.replace('hidden', 'flex');
    }
    };
    xhr.open('GET', '/following/' + user_tag);
    xhr.send();
}

function hideModal(){
    modal.classList.replace('flex', 'hidden');
}