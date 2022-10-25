//ajax 사용시 csrf 토큰 생성------
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//---------------------------------
$(document).ready(function(){
    //검색 기능
    $('#searching_text').on('focus',()=>{
        $('#search-modal').addClass('flex');
        $('#search-modal').removeClass('hidden');
    });
    $('#search-modal').on('click',()=>{
        $('#search-modal').removeClass('flex');
        $('#search-modal').addClass('hidden');
    });
    $('#searching_text').on('propertychange change keyup paste',function(){
        if($('#searching_text').val() != ''){
            let xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = (e)=>{
            let req = e.target;
                if(req.readyState === XMLHttpRequest.DONE) {
                    if(req.status === 200) {
                        var users = JSON.parse(req.responseText);
                        $('#search_list').html('');
                        if(users.length){
                            for(var user of users){
                                $('#search_list').append(
                                    '<li>'+
                                    '<a href="/mypage/' + user.tag + '" class="flex items-center p-3 text-base font-bold text-gray-900 bg-gray-50 rounded-lg hover:bg-gray-100 group hover:shadow dark:bg-gray-600 dark:hover:bg-gray-500 dark:text-white">'+
                                    '<img class="w-10 h-10 rounded-full" src='+ user.profile_pic +'>'+
                                    '<span class="flex-1 ml-3 whitespace-nowrap">'+
                                        user.tag+
                                    '</span>'+
                                    '</a>'+
                                    '</li>'
                                );
                            }   
                        }
                        else{
                            $('#search_list').append("검색 결과가 없습니다.")
                        }
                        
                        
                    }
                }
            }
            // xhttp.open("GET", "{% url 'photo:search_user' user_tag='x'%}"+$(this).val(), true);
            xhttp.open("GET", "/search/"+$(this).val(), true);
            xhttp.send();
        }    
        else{
            $('#search_list').html('');
        }
    });

    //다음 리스트 불러오기
    $('#load_next').on('click',function(){
        let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = (e)=>{
        let req = e.target;
        //console.log(req);
            if(req.readyState === XMLHttpRequest.DONE) {
                if(req.status === 200) {
                    //console.log(req);
                    let data = req.response;
                    // console.log(data);
                    let rows = $(data).find('.post');
                    // console.log(rows);
                    if(rows.length > 0){
                        for(var i=0;i<rows.length;i++){
                            document.querySelector('.posts').appendChild(rows[i]);
                        }
                        $(this).attr('data',Number($(this).attr('data'))+1);
                        setSplide(rows.length);
                        
                        if(rows.length< 9){
                            for(btn of document.querySelectorAll('#load_next')){
                                btn.remove();
                            }
                        }
                    }
                }
            }
        }
        var url = document.location.href.split('/');
        var csrftoken = {{ csrf_token }};
        if(url[1] == 'mypage'){
            xhttp.open("POST", 'mypage/' + url[2], true);
            xhttp.setRequestHeader("X-CSRFToken", csrftoken);
            xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhttp.send('page_num=' + (Number($(this).attr('data'))+1));
        }else{
            xhttp.open("POST", '', true);
            xhttp.setRequestHeader("X-CSRFToken", csrftoken);
            xhttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhttp.send('page_num=' + (Number($(this).attr('data'))+1));
        }
        
    });

});

function search_bar_toggle(){
    $('.search_box').toggleClass('search_box_open');
}

function like_photo(self,post_id){
    let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = (e)=>{
        let req = e.target;
            if(req.readyState === XMLHttpRequest.DONE) {
                if(req.status === 200) {
                    $(self).children('img').attr("src",like_img_url);
                    $(self).attr('onclick','unlike_photo(this,' + post_id + ')');
                    $('#like_count'+post_id).text(req.responseText + '명이 좋아합니다.');
                }
            }
        }
        // xhttp.open("GET", "{% url 'photo:search_user' user_tag='x'%}"+$(this).val(), true);
        xhttp.open("GET", "/like/"+post_id, true);
        xhttp.send();
}

function unlike_photo(self,post_id){
    let xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = (e)=>{
        let req = e.target;
            if(req.readyState === XMLHttpRequest.DONE) {
                if(req.status === 200) {
                    $(self).children('img').attr("src",unlike_img_url);
                    $(self).attr('onclick','like_photo(this,' + post_id + ')');
                    $('#like_count'+post_id).text(req.responseText + '명이 좋아합니다.');
                }
            }
        }
        // xhttp.open("GET", "{% url 'photo:search_user' user_tag='x'%}"+$(this).val(), true);
        xhttp.open("GET", "/unlike/"+post_id, true);
        xhttp.send();
}

function setSplide(cnt){
    var elms = document.getElementsByClassName( 'splide' );
    var start = 0
    if (document.getElementById('load_next')){
        start = (Number(document.getElementById('load_next').getAttribute('data'))-1)*9;
    }
    for (var i=start; i<start+cnt; i++){
        var splide = new Splide( elms[i] ).mount();
        if(splide.length<2){
            splide.options = {arrows:false};
        }
    }   
}
